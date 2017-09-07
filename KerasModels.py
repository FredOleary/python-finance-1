#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 15:14:13 2017

@author: fredoleary
"""
import keras.preprocessing.text as preproc
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Dropout, Embedding, LSTM, Bidirectional, Activation
from keras.utils import to_categorical

class ModelLSTM:
    def __init__(self, max_features, batch_size, max_seq_len, num_words):
        self.max_features = max_features
        self.batch_size = batch_size
        self.max_seq_len = max_seq_len
        self.num_words = num_words
        self.model = None
        self.x_train = None
        self.y_train = None
        self.x_test = None
        self.y_test = None
        
        
    def create_model(self, texts, x_train_set, x_test_set, y_train_set, y_test_set):       
        tokenizer = preproc.Tokenizer(num_words=self.num_words)
        tokenizer.fit_on_texts(texts)
        
        x_train_unpad = tokenizer.texts_to_sequences(x_train_set)
        self.x_train = sequence.pad_sequences(x_train_unpad, maxlen=100)

        x_test_unpad = tokenizer.texts_to_sequences(x_test_set)
        self.x_test = sequence.pad_sequences(x_test_unpad, maxlen=100)
    
        self.y_train = to_categorical(y_train_set)
        self.y_test = to_categorical(y_test_set)
   
 #   y_train = np.array(y_train_set)
 #   y_test = np.array(y_test_set)

        self.model = Sequential()
        embedding = Embedding(self.max_features, 128, input_length=self.max_seq_len)
        self.model.add(embedding)
        self.model.add(Bidirectional(LSTM(64)))
        self.model.add(Dropout(0.5))
#        model.add(Dense(3, activation='sigmoid'))
        self.model.add(Dense(3,activation='softmax'))
    
        # try using different optimizers and different optimizer configs
        self.model.compile('adam', 'categorical_crossentropy', metrics=['accuracy'])
        return self.model, self.x_train, self.x_test, self.y_train, self.y_test 
    
    def train_model(self, num_epochs, callbacks):
        history = self.model.fit(self.x_train, self.y_train, batch_size=self.batch_size, \
                                    epochs=num_epochs, validation_data=[self.x_test, self.y_test], \
                                    callbacks=[callbacks])
        return history

class ModelMLP:
    def __init__(self, max_features, batch_size, max_seq_len, num_words):
        self.max_features = max_features
        self.batch_size = batch_size
        self.max_seq_len = max_seq_len
        self.num_words = num_words
        self.model = None
        self.x_train = None
        self.y_train = None
        self.x_test = None
        self.y_test = None
        
        
    def create_model(self, texts, x_train_set, x_test_set, y_train_set, y_test_set):       
        print('Vectorizing sequence data...')
        tokenizer = preproc.Tokenizer(num_words=self.num_words)
        tokenizer.fit_on_texts(texts)
        
        x_train_unpad = tokenizer.texts_to_sequences(x_train_set)
        self.x_train = tokenizer.sequences_to_matrix(x_train_unpad, mode='binary')
        
        x_test_unpad = tokenizer.texts_to_sequences(x_test_set)
        self.x_test = tokenizer.sequences_to_matrix(x_test_unpad, mode='binary')
        print('x_train shape:', self.x_train.shape)
        print('x_test shape:', self.x_test.shape)
    
        self.y_train = to_categorical(y_train_set)
        self.y_test = to_categorical(y_test_set)
   
 #   y_train = np.array(y_train_set)
 #   y_test = np.array(y_test_set)

        self.model = Sequential()
        self.model.add(Dense(512, input_shape=(self.num_words,)))
        self.model.add(Activation('relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(3))
        self.model.add(Activation('softmax'))

        self.model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
    
        return self.model, self.x_train, self.x_test, self.y_train, self.y_test 
    

    
    def train_model(self, num_epochs, callbacks):
        history = self.model.fit(self.x_train, self.y_train, batch_size=self.batch_size, \
                                    epochs=num_epochs, validation_data=[self.x_test, self.y_test], \
                                    callbacks=[callbacks])
        return history