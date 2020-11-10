import numpy as np
import pandas as pd
from collections import Counter
import re, regex, os
from carnatic import cparser
#np.random.seed(42)
def _get_bigrams(notations_file):
    notes = cparser._get_notes_from_file(notations_file)
    n = 2
    ngrams = zip(*[notes[i:] for i in range(n)])
    bigrams = [" ".join(ngram) for ngram in ngrams]
    return bigrams
def _predict_next_state(chord:str, bigrams:list):
    bigrams_with_current_chord = [bigram for bigram in bigrams if bigram.split(' ')[0]==chord]
    count_appearance = dict(Counter(bigrams_with_current_chord))
    for ngram in count_appearance.keys():
        count_appearance[ngram] = count_appearance[ngram]/len(bigrams_with_current_chord)
    options = [key.split(' ')[1] for key in count_appearance.keys()]
    probabilities = list(count_appearance.values())
    return np.random.choice(options, p=probabilities)

def generate_notes_from_corpus(corpus_files:list,starting_note:str, ending_note:str, length:int=32, save_to_file=None):
    """
    Generate note sequence of defined length from corpus text files
    @param corpus_files: List of corpus file paths that contain sequence of notes
    @param starting_note: Starting note (should be one of aarognam/avaroganam notes). Default=None
    @param ending_note: Ending note (should be one of aarognam/avaroganam notes). Default=None
    @param length: desired length of notes to be generated. 
            Note: Not always exact number of notes may be generated
    @param save_to_file: File name to which generated notes are to be written. Default=None
    """
    bigrams = []
    for notation_file in corpus_files:
        bigrams += _get_bigrams(notation_file)
    if not starting_note:
        starting_note = 'S'
    chord = starting_note
    chords = [starting_note]
    length -= 1
    if ending_note:
        length -= 1
    for n in range(length):
        chords.append(_predict_next_state(chord, bigrams))
        chord = chords[-1]
    if ending_note:
        chords.append(ending_note)
    #my_str = '\n'.join(' '.join(chords[i:i+line_break_at]) for i in range(0, len(chords), (line_break_at)))
    #print('markov','my_str\n',my_str)
    return chords # array # chords

if __name__ == '__main__':
    pass
