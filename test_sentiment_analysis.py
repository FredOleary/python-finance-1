#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 10:31:22 2017

@author: fredoleary
"""
import numpy as np
from platform import python_version
import keras.preprocessing.text as preproc
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Dropout, Embedding, LSTM, Bidirectional
from keras.utils import to_categorical
from keras.callbacks import Callback
from DbFinance import FinanceDB
from CompanyList import CompanyWatch
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

def get_x_sets(finance, percent_train):
    """ Get rows where sentiment has not been set """
    _texts = []
    _news = []
    _sentiments = []
    _x_train_set = []
    _x_test_set = []
    _y_train_set = []
    _y_test_set = []

    rows = finance.get_news_with_sentiment()
    for row in rows:
        sentiment = row[8]
        _texts.append( row[4])
        if sentiment != "I":
            sentiment_num = 1
            if sentiment== "G":
                sentiment_num = 2
            elif sentiment == "B":
                sentiment_num = 0
            _news.append(row[4]) 
            _sentiments.append(sentiment_num)

    train_count = int((percent_train * len(_news))/100)
    _x_train_set = _news[:train_count]
    _y_train_set = _sentiments[:train_count]
    _x_test_set = _news[train_count:]
    _y_test_set = _sentiments[train_count:]
        
    return _texts, _x_train_set, _x_test_set, _y_train_set, _y_test_set

class my_chart(Callback):
    def __init__(self, num_epochs):
        plt.ion()
        self.num_epochs = num_epochs
        self.ax = plt.axes()
        self.ax.set_xlim(0, num_epochs)
        self.ax.set_ylim(0, 1)
        self.train_accuracy=[]
        self.train_loss=[]
        self.validation_accuracy=[]
        self.validation_loss=[]
        
    def create_segments( self ):
        graph_len = len(self.train_accuracy) # number of epochs so far
        x = np.arange(graph_len) 
    
        segs = np.zeros((4, graph_len, 2), float) # 4 lines ,x * y per linesegs[:, :, 1] = ys
        segs[:, :, 0] = x
        for index in range(graph_len):
            segs[0, index, 1] = self.train_accuracy[index]
        for index in range(graph_len):
            segs[1, index, 1] = self.train_loss[index]
        for index in range(graph_len):
            segs[2, index, 1] = self.validation_accuracy[index]
        for index in range(graph_len):
            segs[3, index, 1] = self.validation_loss[index]
            
        return segs[0], segs[1], segs[2], segs[3]

    def update( self, seg0, seg1, seg2, seg3 ):
     
        lc0 = LineCollection([seg0], linewidths=(1), colors= ['blue'], linestyle='solid')
        lc1 = LineCollection([seg1], linewidths=(1), colors= ['red'], linestyle='solid')
        lc2 = LineCollection([seg2], linewidths=(1), colors= ['green'], linestyle='solid')
        lc3 = LineCollection([seg3], linewidths=(1), colors= ['brown'], linestyle='solid')

        self.ax.legend([lc0, lc1, lc2, lc3], ['Train acc', 'Train loss', 'Val acc', 'Val loss'], loc='upper left')
        self.ax.add_collection(lc0)
        self.ax.add_collection(lc1)
        self.ax.add_collection(lc2)
        self.ax.add_collection(lc3)
        plt.pause(.1)

    def on_epoch_end(self, epoch, logs):
        #update accuracy/loss
        # segs = self.create_segments()
        self.train_accuracy.append( logs["acc"])
        self.train_loss.append( logs["loss"])
        self.validation_accuracy.append( logs["val_acc"])
        self.validation_loss.append( logs["val_loss"])
        seg0, seg1, seg2, seg3 = self.create_segments()
        self.update(seg0, seg1, seg2, seg3)
    
    

if __name__ == "__main__":
    print('Python', python_version())
    
    COMPANIES = CompanyWatch()
    FINANCE = FinanceDB(COMPANIES.get_companies())
    FINANCE.initialize()
    percent_train = 80
 
    texts, x_train_set, x_test_set, y_train_set, y_test_set = get_x_sets(FINANCE, percent_train)
    
    max_features = 20000
    batch_size = 32
    maxlen = 100
    num_epochs = 50
       
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
    embedding = Embedding(max_features, 128, input_length=maxlen)
    model.add(embedding)
    model.add(Bidirectional(LSTM(64)))
    model.add(Dropout(0.5))
#    model.add(Dense(3, activation='sigmoid'))
    model.add(Dense(3, activation='sigmoid'))
    
    # try using different optimizers and different optimizer configs
    model.compile('adam', 'binary_crossentropy', metrics=['accuracy'])
    
    print('Train...')
    history = model.fit(x_train, y_train, batch_size=batch_size, epochs=num_epochs, validation_data=[x_test, y_test], callbacks=[my_chart(num_epochs)])
    
    predict_train = np.around(model.predict(x_train[:2]))
    predict_test = np.around(model.predict(x_test[:2]))
    
    accuracy = 0
    predict_test_all = np.around(model.predict(x_test))
    for i in range( len(predict_test_all) ):
        if (predict_test_all[i] == y_test[i]).all():
            accuracy += 1
    print("done-accuracy:" , (accuracy/len(y_test))*100, "%")
    input("Done-press enter to exit")
