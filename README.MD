# Spell Checker
In this project I have implemented a [noisy channel based spelling correction system](https://web.stanford.edu/class/cs124/lec/spelling.pdf). 
## Requirements to run the program
You need to have `python 3.6` to run this project. You should create a virtual environment from the `requirement.txt` and then run `main.py` for starting the program.

*Remember* download `en` for `spacy` before running the program. You can run the following command to download it.
`python -m spacy download en`

After running the program, it will prompt for an input file path. Provide the input file path, then press enter to run the program. It will then generate `output.txt`. A simple input and output files are provided here. If there is a problem with `.pkl` files, remove them and then run the program again.

## Program Details
### Corpus
I have used the corpus that is publicly available at this [repository](https://github.com/jbhoosreddy/spellcorrect). This corpus has 81,344 distinct words, which together appear 50,51,960 times. 

### Language Model
I used bigram language model with laplace smoothing for this project. From the corpus, using NLTK package first I created a set of bigrams. Then I calculated the Conditional frequency distribution of these bigrams. From this distribution, I calculated the probability distribution from the frequency distribution where Laplacian distribution has been used to calculate the probability for a unknown word. 
My algorithm works well with bigram language model than the unigram model. It works better with trigram model, but computationally expensive. To make the process simple, I decided to use the bigram model.

### Edit Distance
I implemented both the Levenshtein edit distance and Damerau-Levenshtein edit distance algorithms. I considered insertion and deletion cost as 1 for the implementation. For this project I used Damerau-Levenshtein edit distance algorithm. I have also implemented another algorithm which returns the edit type between two strings. For example, the algorithm will return the edit type as transposition between ‘there’ and ‘three’.

### Computing Error Probability
To implement the noisy channel algorithm, we need to calculate the error probability of a mistaken word provided the correct word. For this, I wrote a function which will calculate the error probability from the confusion matrices of insertion, substitution, deletion and transposition. I collected the matrices from [here](https://github.com/jbhoosreddy/spellcorrect) to build the confusion matrix. The probability is calculated by the number of time insertion, deletion etc. take place in misspelled words divided by the number of time the correct pattern occur. For the correctly spelled word, I took the 𝛂 value as 0.95 for the error probability.

### Overflow of the project
The program takes a file path as an input. After reading the lines from the file, it processes it line by line. I applied spacy package to determine the parts of speech of the word. Each line is tokenized by spacy. If the word is number or punctuation, I skipped it for the spell checking. In the spell checking part, for each word a set of candidates is generated using the edit distance algorithm.  As the maximum number of error take place within 1 edit distance, I considered the words that fall in one edit distance only. If the word itself found in the corpus it is included in the candidate set. Then for each candidate word, I determined its edit type and then calculated the error probability. I kept track of the current word, its previous word and the next word for calculating language model probability. For each candidate word, the probability of the sequence(previous word, current word, next word) is calculated bigram language model. For calculating the probability of the sequence, the probability of the current word given the previous word and the probability of the next word given the current word are calculated and then multiplied to get the sequence probability. For each candidate the error probability and the language model probability is multiplied and then the score is sorted to get the best suitable word. Then the program generates an output.txt from the corrected tokens where each corrected word is placed inside the parentheses beside the wrong word. 

### Limitations
There are some limitations of my program. For calculating the sequence probability, for simplification it assumes that the previous and next word are correct. But in real scenario it might not happen. Another limitation for correctly spelled word, I considered the error probability as 0.95 which might not the ideal case. If the program could use more context (for example, trigram) it may produce better result. If I got more time, I will like to try trigram language model with Kneser Kney smoothing. I would also like to try better model for error probability of correctly typed word. 
