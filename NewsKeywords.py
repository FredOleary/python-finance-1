#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 19:35:54 2017

@author: fredoleary
"""

import re

class NewsKeywords():
    """
        Parse news items into keywords.
    """
    def __init__(self):
        self.dictionary = {}
        self.ignore_words = {}
        self.static_ignore = ["is", "the", "in", "that", "will", "have", "a", "as", \
                              "of", "and", "with", "for", "be", "this", "so", "would", \
                              "north", "not", "note", "noted", "now", "number", "october", "off", \
                              "offer", "offering", "oil", "on", "one", "paid", "painted", "payment", \
                              "no", "oct", "orca", "owl", "parents", "qcom", "plan", "qualcomm", \

                              "year", "years", "yet", "you", "youtube", "your", "zaks", "|" \
                              "x", "would", "worth", "working", "writes", "yet", "were", "which", \
                              "predict", "predicting", "present", "presents", "press", "preview", "previous", "price", \
                              "price-earnings", "price-to-sales", "prices", "prior", "private", "probably", "process", "processor", \
                              "product", "production", "products", "professional", "properties", "properties,", "q3", "q4", \
                              "quarter", "rather", "products", "regarding", "report", "revenue,", "s", "say", \
                              "or", "our", "out", "over", "owns", "pace,", "part", "penny", \
                              "people", "period", "out", "play", "owns", "upon,", "up", "upload", \
                              "used", "user", "users", "using", "under", "until,", "time", "to", \
                              "her", "his", "what", "company", "than", "are", "also"]

        self.sentiment_dictionary = {"accelerate":1, "achieved":1,"advanced":1, "advantages":1,"beat":1, \
                                     "below":1, "better":1, "better-than-expected":1, "blow":-1, "boost":1,\
                                     "boosted":1, "bottom":1, "bottoming":1, "bullish":1, "buy":1, "buying":1, \
                                     "challenges":-1, "comeback":1, "compelling":1, "convincing":1, "correction":-1, \
                                     "cut":-1, "declined":-1, "declining":-1, "decrease":-1, "decreased":-1, \
                                     "deferred":-1, "difficult":-1, "disappointing":-1, "down":-1, "downgraded":-1, \
                                     "drag":-1, "efficient":1, "engaged":1, "error":-1, "fall":-1, "falls":-1, \
                                     "fears":-1, "flagging":-1, "gained":1, "gains":1, "improve":1, "improves":1, \
                                     "increase":1, "increased":1, "innovation":1, "lifted":1, "lifts":1, \
                                     "lowered":-1, "milestone":1, \
                                     "needed":-1, "outperformed":1, "over-reaction":1, "oversold":1, "overweight":-1, \
                                     "pain":-1, "performance-boosting":1, "performance-enhanced":1, "plagued":-1, \
                                     "positive":1, "powerful":1, "premium":1, "profitability":1, "proven":1, \
                                     "pulled":-1, "raised":1, "raises":1, "ramp":1, "recognition":1, "record":1, \
                                     "restate":-1, "restated":-1, "reward":1, "rise":1, "risen":1, "risk":-1, \
                                     "sell":-1, "sell-off":-1, "selling":-1, "selloff":-1, "sells":-1, \
                                     "severely":-1, "short":-1, "shorts":-1, "slide":-1, "slips":-1, "slowdown":-1, \
                                     "slower":-1, "soars":1, "solid":1, "sputter":-1, "startling":-1, "strong":1, \
                                     "struggle":-1, "struggles":-1, "successful":1, "support":1, "tailwinds":1, \
                                     "taper":-1, "top-heavy":-1, "trimmed":-1, "turbocharge":1, "upgrade":1, "upgraded":1, \
                                     "upside":1, "wanting":-1, "warning":-1, "weighed":-1, "woes":-1, '“outperform”':1, \
                                     "“sell”":-1, "“underperform”":-1 \
                                     }

    def get_dictionary(self):
        """
        dictionary accessor
        """
        return self.dictionary
    
    def get_sentiment_dictionary(self):
        """
        sentiment_dictionary accessor
        """
        return self.sentiment_dictionary

    def update_news_items(self, news_items):
        """
        Rebuild the dictionary
        """
        self.dictionary.clear()
        for word in self.static_ignore:
            self.add_ignore_word(word)
        for news_item in news_items:
            self.update_keywords(news_item)

    def update_keywords(self, news_item):
        """
        Parse the news_item to build the object of keywords
        """
        self._update_dictionary(news_item["title"], news_item)
        self._update_dictionary(news_item["description"], news_item)

    def add_ignore_word(self, word):
        """
        Add word to be ignored to the dictionary
        """
        ignore_word = word.lower()
        if not ignore_word in self.ignore_words:
            self.ignore_words[ignore_word] = word

    def _update_dictionary(self, phrase, news_item):
        words = re.split(r'[,.!:?\s]\s*', phrase.lower())
        for word in words:
            if word in self.dictionary:
                self._update_reference(word, news_item)
            else:
                self._create_reference(word, news_item)

    def _create_reference(self, word, news_item):
        if self._use_word(word):
            self.dictionary[word] = {"count":0, "references":{}}
            self._update_reference_int(word, news_item)

    def _update_reference(self, word, news_item):
        if self._use_word(word):
            self._update_reference_int(word, news_item)

    def _update_reference_int(self, word, news_item):
        references = self.dictionary[word]["references"]
        if news_item["hash"] in references:
            references[news_item["hash"]]["count"] += 1
        else:
            references[news_item["hash"]] = {"count": 1}
        self.dictionary[word]["count"] += 1

    def _use_word(self, word):
        if word in self.ignore_words:
            return False
        return True
