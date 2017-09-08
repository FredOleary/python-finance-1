#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 10:31:22 2017

@author: fredoleary
"""
import numpy as np
import html
import sys
from platform import python_version
from keras.models import Sequential
from keras.layers import Embedding
from keras.callbacks import Callback
from DbFinance import FinanceDB
from CompanyList import CompanyWatch
from KerasModels import ModelLSTM, ModelMLP

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

def get_x_sets(finance, pcnt_train):
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
        news = html.unescape(row[3]) + ". " + html.unescape(row[4])
        _texts.append(news)
        if sentiment != "I":
            sentiment_num = 1
            if sentiment== "G":
                sentiment_num = 2
            elif sentiment == "B":
                sentiment_num = 0
            _news.append(news) 
            _sentiments.append(sentiment_num)

    train_count = int((pcnt_train * len(_news))/100)
    _x_train_set = _news[:train_count]
    _y_train_set = _sentiments[:train_count]
    _x_test_set = _news[train_count:]
    _y_test_set = _sentiments[train_count:]
        
    return _texts, _x_train_set, _x_test_set, _y_train_set, _y_test_set

def test__embedding():
    model = Sequential()
    model.add(Embedding(1000, 64, input_length=10))
      # the model will take as input an integer matrix of size (batch, input_length).
      # the largest integer (i.e. word index) in the input should be no larger than 999 (vocabulary size).
      # now model.output_shape == (None, 10, 64), where None is the batch dimension.
    
    input_array = np.random.randint(1000, size=(32, 10))
    
    model.compile('rmsprop', 'mse')
    output_array = model.predict(input_array)
    assert output_array.shape == (32, 10, 64)

class my_chart(Callback):
    def __init__(self, no_epochs):
        super().__init__() 
        plt.ion()
        self.num_epochs = no_epochs
        self.ax = plt.axes()
        self.ax.set_xlim(0, no_epochs)
        self.ax.set_ylim(0, 3)
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

    def on_epoch_end(self, epoch, logs=None):
        #update accuracy/loss
        # segs = self.create_segments()
        if logs is not None:
            self.train_accuracy.append( logs["acc"])
            self.train_loss.append( logs["loss"])
            self.validation_accuracy.append( logs["val_acc"])
            self.validation_loss.append( logs["val_loss"])
            seg0, seg1, seg2, seg3 = self.create_segments()
            self.update(seg0, seg1, seg2, seg3)
    
if __name__ == "__main__":
    print('Python', python_version())
    #test__embedding()
    
    COMPANIES = CompanyWatch()
    FINANCE = FinanceDB(COMPANIES.get_companies())
    FINANCE.initialize()
    if len(sys.argv) > 1:
        percent_train = int(sys.argv[1])
    else:
        percent_train = 50
        
    num_epochs = 50
 
    texts, x_train_set, x_test_set, y_train_set, y_test_set = get_x_sets(FINANCE, percent_train)
#    model_LSTM = ModelLSTM(20000, 32, 100,1000 )
    model_LSTM = ModelMLP(20000, 32, 100,1000 )
    
    lstm_model, x_train, x_test, y_train, y_test = model_LSTM.create_model(texts, x_train_set, x_test_set, y_train_set, y_test_set)
    
    print('Train... Percent train = ', percent_train, '%')
    history = model_LSTM.train_model( num_epochs, my_chart(num_epochs))
    
    predict_train = np.around(lstm_model.predict(x_train[:2]))
    predict_test = np.around(lstm_model.predict(x_test[:2]))
    
    accuracy = 0
    predict_test_all = np.around(lstm_model.predict(x_test))
    for i in range( len(predict_test_all) ):
        if (predict_test_all[i] == y_test[i]).all():
            accuracy += 1
    print("done-accuracy:" , (accuracy/len(y_test))*100, "%")
    input("Done-press enter to exit")
