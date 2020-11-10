import numpy as np
import pandas as pd
from collections import Counter
import re, regex, os
from carnatic import cparser
#np.random.seed(42)
#def _get_bigrams(notes, width=1):
separator1 = " - "
separator2= " "
def _get_bigrams(notations_file, width=1):
    notes = cparser._get_notes_from_file(notations_file)
    n = width + 1
    bigrams = []
    for i in range(len(notes) - width):
        key = separator2.join(notes[i:i+width])
        next_note = notes[i+width:i+2*width]
        if len(next_note)==width:
            #print('key',key,'next_note',next_note)
            bigrams.append(key+separator1 + separator2.join(next_note))
    #print('bigrams',bigrams)
    return bigrams
def _predict_next_state(chord:str, bigrams:list):
    bigrams_with_current_chord = [bigram for bigram in bigrams if bigram.split(separator1)[0]==chord]
    if not bigrams_with_current_chord:
        return None
    #print('chord',chord,'bigrams_with_current_chord',bigrams_with_current_chord)
    count_appearance = dict(Counter(bigrams_with_current_chord))
    for ngram in count_appearance.keys():
        count_appearance[ngram] = count_appearance[ngram]/len(bigrams_with_current_chord)
    options = [key.split(separator1)[1] for key in count_appearance.keys()]
    probabilities = list(count_appearance.values())
    return np.random.choice(options, p=probabilities)

def generate_notes_from_corpus(corpus_files,starting_note=None, ending_note=None, length:int=32, width:int=4, save_to_file=None):
    """
    Generate note sequence of defined length from corpus text files
    @param corpus_files: List of corpus file paths that contain sequence of notes
    @param starting_note: Starting note (should be one of aarognam/avaroganam notes). Default=None
    @param ending_note: Ending note (should be one of aarognam/avaroganam notes). Default=None
    @param length: desired length of notes to be generated. 
            Note: Not always exact number of notes may be generated
    @param save_to_file: File name to which generated notes are to be written. Default=None
    @param width: integer. 1 means single note pair, 2 means two-note pair (SR RG GM), 4 means four note pair (SRGM RGMD) etc.
        Avoid specifying more than 4  
    """
    bigrams = []
    for notation_file in corpus_files:
        bigrams = _get_bigrams(notation_file, width=width)
    n = 0
    if not starting_note:
        starting_note = (np.random.choice([bigram.split(separator1)[0] for bigram in bigrams]))
    starting_note = ''.join(starting_note)
    chord = starting_note
    chords = [starting_note]
    #print('chords',chords,'starting Notes',starting_note,'ending_note',ending_note)
    n += width
    if ending_note:
        n += 2*width
    while (True):
        next_state = _predict_next_state(chord, bigrams)
        if next_state == None: # or len(next_state)<width:
            chord = np.random.choice([bigram.split(separator1)[0] for bigram in bigrams])
            continue
        #print('n',n,'chord',chord,'next_state',next_state,len(next_state))
        n += width
        chords.append(next_state)
        chord = chords[-1]
        if n >= length:
            #print("Collected note count:",n)
            break
    if ending_note:
        ending_note = ''.join(ending_note)
        try:
            last_pair = (np.random.choice([bigram for bigram in bigrams if bigram.split(separator1)[1]==ending_note]).split(separator1))
        #print('last_pair1',last_pair)
        except:
            print("Cound not find notes ending with",ending_note,"Ending notes are randomly generated")
            last_pair = (np.random.choice([bigram for bigram in bigrams]).split(separator1))
            #print('last_pair2',last_pair)
        chords += last_pair
    return chords # array # chords

if __name__ == '__main__':
    notations_files = ["../data/varnam.txt", "../data/varaveena.txt", "../data/valachi_vacchi.txt"]
    generated_notes = generate_notes_from_corpus(notations_files,None,None,160, width=4)
    print('generated notes',generated_notes, '\nlength',len(generated_notes))
    pass