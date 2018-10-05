import vocab_builder as vocab
import nltk
import pickle
import os

if os.path.exists('corpus.pkl'):
    f = open('corpus.pkl', 'rb')
    CORPUS = pickle.load(f)
    f.close()
else:
    vocab.get_the_corpus('corpus.data.txt')
    f = open('corpus.pkl', 'rb')
    CORPUS = pickle.load(f)
    f.close()

if os.path.exists('cprob_2gram.pkl'):
    f = open('cprob_2gram.pkl', 'rb')
    cprob_2gram = pickle.load(f)
    f.close()
else:
    cfreq_2gram = nltk.ConditionalFreqDist(nltk.bigrams(CORPUS))
    cprob_2gram = nltk.ConditionalProbDist(cfreq_2gram, nltk.LaplaceProbDist)

    f = open('cprob_2gram.pkl', 'wb')
    pickle.dump(cprob_2gram, f)
    f.close()


# if os.path.exists('cprob_3gram.pkl'):
#     f = open('cprob_3gram.pkl', 'rb')
#     cprob_3gram = pickle.load(f)
#     f.close()
# else:
#     corpus_trigrams = nltk.trigrams(CORPUS)
#     condition_pairs = (((w0, w1), w2) for w0, w1, w2 in corpus_trigrams)
#     cfd_corpus = nltk.ConditionalFreqDist(condition_pairs)
#     cprob_3gram = nltk.ConditionalProbDist(cfd_corpus, nltk.LaplaceProbDist)
#
#     f = open('cprob_3gram.pkl', 'wb')
#     pickle.dump(cprob_3gram, f)
#     f.close()


def calculate_bigrm_probability(cur_word, prev_word):
    """
    :param cur_word: str
    :param prev_word: str
    :return: float
    """
    try:
        return cprob_2gram[prev_word].prob(cur_word)
    except ValueError as ex:
        return 0.0
#
# def calculate_trigrm_probability(cur_word, prev_word_list):
#     """
#
#     :param cur_word: str
#     :param prev_word_list: list of str
#     :return: float
#     """
#     try:
#         return cprob_3gram[prev_word_list[0], prev_word_list[1]].prob(cur_word)
#     except ValueError as ex:
#         return 0.0



def calculate_bigram_prob_seq(previous, current, nxt):
    """

    :param previous: str
    :param current: str
    :param nxt: str
    :return: float
    """
    return calculate_bigrm_probability(current, previous) * calculate_bigrm_probability(nxt, current)
