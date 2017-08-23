#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 19:22:00 2017

@author: fredoleary
"""
import unittest
from platform import python_version
from NewsClassify import ClassifyNews

class SimplisticTest(unittest.TestCase):
    """ Unit tests for news classifiaction"""
    def test(self):
        """ Run news classification tests """
        symbol = "LITE"
        description = "Lumentum"

        # no news item..
        classify = ClassifyNews(symbol, description, None)
        self.assertTrue(classify.classify() == 0)


        # news item with symbol/description mention and negative word. "may be lowered"
        classify = ClassifyNews(symbol, description, {"title": \
            "LITE lowered and Lumentum...", "description":  "LITE symbol and Lumentum name"})
        self.assertTrue(classify.classify() == -10)

        # news item with no symbol/description mention and negative word. "lowered"
        classify = ClassifyNews(symbol, description, {"title": \
            "LITEX lowered and LumentumX...", "description":  "LITEX symbol and LumentumX name"})
        self.assertTrue(classify.classify() == -1)

        # news item with symbol/description mention but not positive or negative
        classify = ClassifyNews(symbol, description, {"title": \
            "LITE symbol and Lumentum name", "description":  "LITE symbol and Lumentum name"})
        self.assertTrue(classify.classify() == 0)

        # news item with symbol mention but not positive or negative
        classify = ClassifyNews(symbol, description, {"title": \
            "LITE symbol and Luxxxmentum name", "description":  "LITE symbol and Luxxxmentum name"})
        self.assertTrue(classify.classify() == 0)

        # news item with symbol/description mention and positive word. "achieved"
        classify = ClassifyNews(symbol, description, {"title": \
            "LITE and Lumentum...", "description":  "LITE achieved and Lumentum name"})
        self.assertTrue(classify.classify() == 10)

        # news item with no symbol/description mention and positive word. "achieved"
        classify = ClassifyNews(symbol, description, {"title": \
            "LITEX  and LumentumX...", "description":  "LITEX achieved and LumentumX name"})
        self.assertTrue(classify.classify() == 1)

if __name__ == "__main__":
    print('Python', python_version())

    unittest.main()
