#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 10:31:22 2017

@author: fredoleary
"""
import pprint
import numpy as np
from platform import python_version
import keras.preprocessing.text as preproc
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Dropout, Embedding, LSTM, Bidirectional
from keras.utils import to_categorical
from DbFinance import FinanceDB
from CompanyList import CompanyWatch


def get_x_sets(finance):
    """ Get rows where sentiment has not been set """
    _texts = []
    _x_train_set = []
    _x_test_set = []
    _y_train_set = []
    _y_test_set = []

    rows = finance.get_news_with_sentiment()
    row_num = 0
    for row in rows:
        sentiment = row[8]
        _texts.append( row[4])
        if sentiment != "I":
            sentiment_num = 1
            if sentiment== "G":
                sentiment_num = 2
            elif sentiment == "B":
                sentiment_num = 0

            if row_num % 2 == 0:
                _x_train_set.append(row[4])
                _y_train_set.append(sentiment_num)
            else:
                _x_test_set.append( row[4])
                _y_test_set.append(sentiment_num)
           
        row_num += 1
        
    return _texts, _x_train_set, _x_test_set, _y_train_set, _y_test_set

if __name__ == "__main__":
    print('Python', python_version())
    
    COMPANIES = CompanyWatch()
    FINANCE = FinanceDB(COMPANIES.get_companies())
    FINANCE.initialize()
 
    texts, x_train_set, x_test_set, y_train_set, y_test_set = get_x_sets(FINANCE)
    
    max_features = 20000
    batch_size = 32
    maxlen = 100
    

       
    nb_words = 1000
    tokenizer = preproc.Tokenizer(num_words=nb_words)
    tokenizer.fit_on_texts(texts)
    
    #pprint.pprint(tokenizer.word_index)
    #pprint.pprint(tokenizer.word_counts)
    
    
    x_train_unpad = tokenizer.texts_to_sequences(x_train_set)
    x_train = sequence.pad_sequences(x_train_unpad, maxlen=100)

    x_test_unpad = tokenizer.texts_to_sequences(x_test_set)
    x_test = sequence.pad_sequences(x_test_unpad, maxlen=100)
    
    y_train = to_categorical(y_train_set)
    y_test = to_categorical(y_test_set)
   
 #   y_train = np.array(y_train_set)
 #   y_test = np.array(y_test_set)

    model = Sequential()
    model.add(Embedding(max_features, 128, input_length=maxlen))
    model.add(Bidirectional(LSTM(64)))
    model.add(Dropout(0.5))
#    model.add(Dense(3, activation='sigmoid'))
    model.add(Dense(3, activation='sigmoid'))
    
    # try using different optimizers and different optimizer configs
    model.compile('adam', 'binary_crossentropy', metrics=['accuracy'])
    
    print('Train...')
    history = model.fit(x_train, y_train, batch_size=batch_size, epochs=100, validation_data=[x_test, y_test])
    
    predict_train = np.around(model.predict(x_train[:2]))
    predict_test = np.around(model.predict(x_test[:2]))
    
    accuracy = 0
    predict_test_all = np.around(model.predict(x_test))
    for i in range( len(predict_test_all) ):
        if (predict_test_all[i] == y_test[i]).all():
            accuracy += 1
    print("done-accuracy:" , (accuracy/len(y_test))*100, "%")
    print("Done")
