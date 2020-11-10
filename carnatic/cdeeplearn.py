import os, re, regex
import json
import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import LSTM, Dropout, TimeDistributed, Dense, Activation, Embedding
from carnatic import cparser

#charIndex_json = "char_to_index.json"
model_weights_directory = 'model_weights/'
BATCH_SIZE = 16
SEQ_LENGTH = 64
EPOCHS = 90
MODEL_WEIGHTS_FILE = ''
JSON_FILE = ''
def set_parameters(batch_size=None, number_of_epochs=None,model_weights_folder= None,
                   json_file=None, model_weights_file=None):
    """
    Set parameters of deep learning method:
    @param batch_size: Batch size for training. Default=16
    @param number_of_epochs: Default 90
    @param model_weights_folder: Default: "model_weights/"
    @param json_file: File containing dictionary of unique notes. Default:"<raagam_name>_corpus|lessons.json"
    @param model_weights_file: File containing trained weights. Default:"<raagam_name>_corpus|lessons.h5"
    """
    global BATCH_SIZE, EPOCHS, model_weights_directory, JSON_FILE, MODEL_WEIGHTS_FILE
    if batch_size:
        BATCH_SIZE = batch_size
    if number_of_epochs:
        EPOCHS = number_of_epochs
    if model_weights_folder:
        model_weights_directory = model_weights_folder
    if json_file:
        JSON_FILE = json_file
        print('JSON_FILE=',JSON_FILE)
    if model_weights_file:
        MODEL_WEIGHTS_FILE = model_weights_file
        print('MODEL_WEIGHTS_FILE',MODEL_WEIGHTS_FILE)
def _read_batches(all_chars, unique_chars):
    length = all_chars.shape[0]
    batch_chars = int(length / BATCH_SIZE) #155222/16 = 9701
    
    for start in range(0, batch_chars - SEQ_LENGTH, 64):  #(0, 9637, 64)  #it denotes number of batches. It runs everytime when
        #new batch is created. We have a total of 151 batches.
        X = np.zeros((BATCH_SIZE, SEQ_LENGTH))    #(16, 64)
        Y = np.zeros((BATCH_SIZE, SEQ_LENGTH, unique_chars))   #(16, 64, 87)
        for batch_index in range(0, 16):  #it denotes each row in a batch.  
            for i in range(0, 64):  #it denotes each column in a batch. Each column represents each character means 
                #each time-step character in a sequence.
                X[batch_index, i] = all_chars[batch_index * batch_chars + start + i]
                Y[batch_index, i, all_chars[batch_index * batch_chars + start + i + 1]] = 1 #here we have added '1' because the
                #correct label will be the next character in the sequence. So, the next character will be denoted by
                #all_chars[batch_index * batch_chars + start + i] + 1. 
        yield X, Y
def _get_model(batch_size, seq_length, unique_chars):
    model = Sequential()
    
    model.add(Embedding(input_dim = unique_chars, output_dim = 512, batch_input_shape = (batch_size, seq_length), name = "embd_1")) 
    
    model.add(LSTM(256, return_sequences = True, stateful = True, name = "lstm_first"))
    model.add(Dropout(0.2, name = "drp_1"))
    
    model.add(LSTM(256, return_sequences = True, stateful = True))
    model.add(Dropout(0.2))
    
    model.add(LSTM(256, return_sequences = True, stateful = True))
    model.add(Dropout(0.2))
    
    model.add(TimeDistributed(Dense(unique_chars)))
    model.add(Activation("softmax"))
    
    #model.load_weights("model_weights/Weights_80.h5", by_name = True)
    
    return model
def _train_the_model(data, epochs):
    global MODEL_WEIGHTS_FILE, JSON_FILE
    char_to_index = {ch: i for (i, ch) in enumerate(sorted(list(set(data))))}
    print("Number of unique characters in our whole tunes database = {}".format(len(char_to_index)),"\n",char_to_index) #87
    with open(os.path.join(model_weights_directory, JSON_FILE), mode = "w") as f:
        json.dump(char_to_index, f)
        
    index_to_char = {i: ch for (ch, i) in char_to_index.items()}
    unique_chars = len(char_to_index)
    
    model = _get_model(BATCH_SIZE, SEQ_LENGTH, unique_chars)
    model.summary()
    model.compile(loss = "categorical_crossentropy", optimizer = "adam", metrics = ["accuracy"])
    
    all_characters = np.asarray([char_to_index[c] for c in data], dtype = np.int32)
    print("Total number of characters = "+str(all_characters.shape[0])) #155222
    
    epoch_number, loss, accuracy = [], [], []
    
    for epoch in range(epochs):
        print("Epoch {}/{}".format(epoch+1, epochs))
        final_epoch_loss, final_epoch_accuracy = 0, 0
        epoch_number.append(epoch+1)
        
        for i, (x, y) in enumerate(_read_batches(all_characters, unique_chars)):
            final_epoch_loss, final_epoch_accuracy = model.train_on_batch(x, y) #check documentation of train_on_batch here: https://keras.io/models/sequential/
            print("Batch: {}, Loss: {}, Accuracy: {}".format(i+1, final_epoch_loss, final_epoch_accuracy))
            #here, above we are reading the batches one-by-one and train our model on each batch one-by-one.
        loss.append(final_epoch_loss)
        accuracy.append(final_epoch_accuracy)
        
    if not os.path.exists(model_weights_directory):
        os.makedirs(model_weights_directory)
    model.save_weights(os.path.join(model_weights_directory, MODEL_WEIGHTS_FILE))
    print('Saved Weights at epoch {} to file {}'.format(epoch+1, MODEL_WEIGHTS_FILE))
    
    #creating dataframe and record all the losses and accuracies at each epoch
    log_frame = pd.DataFrame(columns = ["Epoch", "Loss", "Accuracy"])
    log_frame["Epoch"] = epoch_number
    log_frame["Loss"] = loss
    log_frame["Accuracy"] = accuracy
    log_frame.to_csv("log.txt", index = False)
    
def _make_model(unique_chars):
    model = Sequential()
    
    model.add(Embedding(input_dim = unique_chars, output_dim = 512, batch_input_shape = (1, 1))) 
  
    model.add(LSTM(256, return_sequences = True, stateful = True))
    model.add(Dropout(0.2))
    
    model.add(LSTM(256, return_sequences = True, stateful = True))
    model.add(Dropout(0.2))
    
    model.add(LSTM(256, stateful = True)) 
    #remember, that here we haven't given return_sequences = True because here we will give only one character to generate the
    #sequence. In the end, we just have to get one output which is equivalent to getting output at the last time-stamp. So, here
    #in last layer there is no need of giving return sequences = True.
    model.add(Dropout(0.2))
    
    model.add((Dense(unique_chars)))
    model.add(Activation("softmax"))
    
    return model
def _generate_sequence(starting_note, ending_note, seq_length):
    global MODEL_WEIGHTS_FILE, JSON_FILE
    print('_generate_sequence','JSON_FILE',JSON_FILE,'MODEL_WEIGHTS_FILE',MODEL_WEIGHTS_FILE)
    with open(os.path.join(model_weights_directory, JSON_FILE)) as f:
        char_to_index = json.load(f)
    index_to_char = {i:ch for ch, i in char_to_index.items()}
    initial_index = char_to_index[starting_note]
    ending_index = char_to_index[ending_note]
    unique_chars = len(index_to_char)
    
    model = _make_model(unique_chars)
    model_file = model_weights_directory + MODEL_WEIGHTS_FILE
    print("Reading model weights from file:"+model_file)
    model.load_weights(model_file)
     
    sequence_index = [initial_index]
    
    for _ in range(seq_length-2):
        batch = np.zeros((1, 1))
        batch[0, 0] = sequence_index[-1]
        
        predicted_probs = model.predict_on_batch(batch).ravel()
        sample = np.random.choice(range(unique_chars), size = 1, p = predicted_probs)
        
        sequence_index.append(sample[0])
    sequence_index.append(ending_index)
    seq = [index_to_char[c] for c in sequence_index]
    return seq 
def generate_notes_from_corpus(corpus_files:list,starting_note:str, ending_note:str, length:int=32, save_to_file=None,perform_training=False):
    """
    Generate note sequence of defined length from corpus text files
    @param corpus_files: List of corpus file paths that contain sequence of notes
    @param starting_note: Starting note (should be one of aarognam/avaroganam notes). Default=None
    @param ending_note: Ending note (should be one of aarognam/avaroganam notes). Default=None
    @param length: desired length of notes to be generated. 
            Note: Not always exact number of notes may be generated
    @param save_to_file: File name to which generated notes are to be written. Default=None
    @param perform_training: True/False. Default = False. 
        If True, training weights are generated even if model weight file is found  
    """
    global MODEL_WEIGHTS_FILE,JSON_FILE
    print('generate_notes_from_corpus','JSON_FILE',JSON_FILE,'MODEL_WEIGHTS_FILE',MODEL_WEIGHTS_FILE)
    model_file = model_weights_directory + MODEL_WEIGHTS_FILE
    if not os.path.isfile(model_file) or perform_training:
        data = []
        for notations_file in corpus_files:
            data += cparser._get_notes_from_file(notations_file)
        _train_the_model(data, epochs=EPOCHS)
    notes = _generate_sequence(starting_note, ending_note, length)
    return notes

if __name__ == "__main__":
    pass
