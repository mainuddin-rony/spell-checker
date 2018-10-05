"""Load The Confusion Matrix for Insertion, Substitution, Deletion and Transposition"""
import ast
import vocab_builder as vocab
import os
import pickle

f=open('addconfusion.data', 'r')
data=f.read()
f.close()
INSERT_MATRIX = ast.literal_eval(data)


f=open('subconfusion.data', 'r')
data=f.read()
f.close()
SUB_MATRIX = ast.literal_eval(data)


f=open('revconfusion.data', 'r')
data=f.read()
f.close()
TRANSPOSE_MATRIX = ast.literal_eval(data)


f=open('delconfusion.data', 'r')
data=f.read()
f.close()
DELETE_MATRIX = ast.literal_eval(data)

if os.path.exists('corpus.pkl'):
    f = open('corpus.pkl', 'rb')
    CORPUS = pickle.load(f)
    f.close()
else:
    vocab.get_the_corpus('corpus.data.txt')
    f = open('corpus.pkl', 'rb')
    CORPUS = pickle.load(f)
    f.close()


def calculate_channel_error_probability(x, y, distance_type):
    """Method to calculate channel model probability for errors."""
    corpus = ' '.join(str(x) for x in CORPUS)
    if distance_type == 'ins':
        if x == '#':
            return INSERT_MATRIX[x + y] / corpus.count(' ' + y)
        else:
            return INSERT_MATRIX[x + y] / corpus.count(x)
    if distance_type == 'sub':
        return SUB_MATRIX[(x + y)[0:2]] / corpus.count(y)
    if distance_type == 'trans':
        return TRANSPOSE_MATRIX[x + y] / corpus.count(x + y)
    if distance_type == 'del':
        return DELETE_MATRIX[x + y] / corpus.count(x + y)