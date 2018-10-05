import edit_distance as ed
import vocab_builder as vocab
import spacy
import edit_distance as ed
import noisy_channel_probability as ncp
import language_model as lm
import os
import pickle

if os.path.exists('word_freq.pkl'):
    f = open('word_freq.pkl', 'rb')
    WORD_FREQ = pickle.load(f)
    f.close()
else:
    vocab.get_the_corpus_counter('corpus.data.txt')
    f = open('word_freq.pkl', 'rb')
    WORD_FREQ = pickle.load(f)
    f.close()

MAX_EDIT = 1 # considering the word of 1-edit distance for the candidates
nlp = spacy.load('en')

def generate_candidate_set(wrd):
    """

    :param wrd: str
    :return: sorted dictionary
    """
    candidates = dict()
    for item in WORD_FREQ:
        distance = ed.calculate_damerau_levenshtein_distance(wrd, item)
        if distance <= MAX_EDIT:
            candidates[item] = distance
    return sorted(candidates, key=candidates.get, reverse=False)


def process_input_lines(lines):
    """

    :param lines: list of sentences
    :return: list of tokens with correction
    """
    token_list = []
    for line in lines:
        org_doc = nlp(line)
        doc = nlp(line.lower())
        corrected_tokens = []
        doc_size = len(doc)
        prev_flag = True
        next_flag = True

        for index in range(doc_size):
            previous_wrd = "<s>"
            if index > 0:
                prev_idx = index - 1
                while (nlp(corrected_tokens[prev_idx])[0].pos_ == 'PUNCT' or nlp(corrected_tokens[prev_idx])[0].pos_  == 'SPACE') and prev_flag:
                    prev_idx = prev_idx - 1
                    if prev_idx < 0:
                        prev_flag = False

                if prev_idx >= 0:
                    previous = nlp(corrected_tokens[prev_idx])[0]
                    previous_wrd = previous.text

            current = doc[index]
            current_wrd = current.text

            nxt_wrd = "</s>"

            if index + 1 < doc_size:
                nxt_idx = index + 1
                while (next_flag and (doc[nxt_idx].pos_ == 'PUNCT' or doc[nxt_idx].pos_ == 'SPACE')):
                    nxt_idx += 1
                    if nxt_idx >= doc_size:
                        next_flag = False

                if nxt_idx < doc_size:
                    nxt = doc[nxt_idx]
                    nxt_wrd = nxt.text

            if current.pos_ == 'PUNCT' or current.pos_ == 'SPACE':
                token_list.append(org_doc[index].text)
                corrected_tokens.append(current_wrd)

            elif current.pos_ == "NUM" and 'd' in current.shape_:
                token_list.append(org_doc[index].text)
                corrected_tokens.append(current_wrd)

            # elif current.pos_ == "NOUN" and nlp(current.text.title())[0].pos_ == "PROPN":
            #     token_list.append(current_wrd)
            #     corrected_tokens.append(current_wrd)

            else:
                candidates = generate_candidate_set(current_wrd)
                nc_prob = {}
                ovarall_prob = {}
                for item in candidates:
                    if WORD_FREQ[item] >= 10:
                        edit = ed.identify_distance_type(item, current_wrd)
                        try:
                            if edit is None:
                                continue
                            else:
                                if  edit[0] == "None":
                                    nc_prob[item] = 0.95
                                if edit[0] == "ins":
                                    nc_prob[item] = ncp.calculate_channel_error_probability(edit[3][0], edit[3][1], 'ins')
                                if edit[0] == 'del':
                                    nc_prob[item] = ncp.calculate_channel_error_probability(edit[4][0], edit[4][1], 'del')
                                if edit[0] == 'trans':
                                    nc_prob[item] = ncp.calculate_channel_error_probability(edit[4][0], edit[4][1], 'trans')
                                if edit[0] == 'sub':
                                    nc_prob[item] = ncp.calculate_channel_error_probability(edit[3], edit[4], 'sub')
                        except KeyError as ex:
                            print(item)
                            continue

                if len(nc_prob) > 0:

                    for item in nc_prob:
                        channel_prob = nc_prob[item]
                        bigram_prob = lm.calculate_bigram_prob_seq(previous_wrd, current_wrd, nxt_wrd)
                        ovarall_prob[item] = channel_prob * bigram_prob * (10 ** 9)

                    ovarall_prob_list = sorted(ovarall_prob, key=ovarall_prob.get, reverse=True)
                    if current_wrd in ovarall_prob and ovarall_prob[ovarall_prob_list[0]] == ovarall_prob[current_wrd]:
                        token_list.append(current_wrd)
                        corrected_tokens.append(ovarall_prob_list[0])
                    else:
                        if len(ovarall_prob_list) == 0:
                            print("Item " + current_wrd)
                        else:
                            token_list.append(org_doc[index].text + " (" + ovarall_prob_list[0] + ")")
                            corrected_tokens.append(ovarall_prob_list[0])
                else:
                    token_list.append(org_doc[index].text)
                    corrected_tokens.append(current_wrd)

    return token_list