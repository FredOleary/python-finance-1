#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 19:35:54 2017

@author: fredoleary
"""
import re

SPECIFIC_NEWS_MULTIPLIER = 10
MAX_SENTIMENT = 100
MIN_SENTIMENT = -100

class ClassifyNews():
    """
        Calculate the sentiment of the news_item
    """
    def __init__(self, symbol, name, newsItem):
        self.negative_terms = ["struggling", "may be hurt"]
        self.positive_terms = []
        self.symbol = symbol
        self.name = name
        self.news_item = newsItem

    def classify(self):
        """
        returns a weigth between -100 and +100.
        -100 => really negative news
         0 => neutral news
        +100 => really positive news
        """
        weight = 0
        if self.news_item:
            weight = self._get_item_weight()
        return weight

    def _get_item_weight(self):
        multiplier = self._get_item_multiplier()
        sentiment = self._get_item_sentiment()
        if sentiment > MAX_SENTIMENT:
            sentiment = MAX_SENTIMENT
        elif sentiment < MIN_SENTIMENT:
            sentiment = MIN_SENTIMENT
        return multiplier*sentiment

    # test if the news item explicity mentions the symbol
    def _get_item_multiplier(self):
        regex = r'\b'+ self.symbol + r'\b|\b' + self.name + r'\b'
        search_results = re.findall(regex, self.news_item["title"], re.I | re.X)
        if search_results:
            return SPECIFIC_NEWS_MULTIPLIER
        search_results = re.findall(regex, self.news_item["description"], re.I | re.X)
        if search_results:
            return SPECIFIC_NEWS_MULTIPLIER
        return 1

    def _get_item_sentiment(self):
        sentiment = 0
        for negative in self.negative_terms:
            regex = r'\b'+ negative + r'\b'
            search_title = re.findall(regex, self.news_item["title"], re.I | re.X)
            search_description = re.findall(regex, self.news_item["description"], re.I | re.X)
            if search_title or search_description:
                sentiment = sentiment-1

        for positive in self.positive_terms:
            regex = r'\b'+ positive + r'\b'
            search_title = re.findall(regex, self.news_item["title"], re.I | re.X)
            search_description = re.findall(regex, self.news_item["description"], re.I | re.X)
            if search_title or search_description:
                sentiment = sentiment+1

        return 0
