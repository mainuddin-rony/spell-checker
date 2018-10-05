from collections import Counter
import pickle


def word_splitter(text):
    return text.lower().split(" ")



def get_the_corpus_counter(file_path):
    word_counter = Counter(word_splitter(open(file_path).read()))
    f = open('word_freq.pkl', 'wb')
    pickle.dump(word_counter, f)
    f.close()

def get_the_corpus(file_path):
    corpus =  word_splitter(open(file_path).read())
    f = open('corpus.pkl', 'wb')
    pickle.dump(corpus, f)
    f.close()