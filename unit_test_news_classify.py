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


        # news item with symbol/description mention and negative phrase. "may be hurt"
        classify = ClassifyNews(symbol, description, {"title": \
            "LITE may be hurt and Lumentum...", "description":  "LITE symbol and Lumentum name"})
        self.assertTrue(classify.classify() == -10)

        # news item with no symbol/description mention and negative phrase. "may be hurt"
        classify = ClassifyNews(symbol, description, {"title": \
            "LITEX may be hurt and LumentumX...", "description":  "LITEX symbol and LumentumX name"})
        self.assertTrue(classify.classify() == -1)

        # news item with symbol/description mention but not positive or negative
        classify = ClassifyNews(symbol, description, {"title": \
            "LITE symbol and Lumentum name", "description":  "LITE symbol and Lumentum name"})
        self.assertTrue(classify.classify() == 0)

        # news item with symbol mention but not positive or negative
        classify = ClassifyNews(symbol, description, {"title": \
            "LITE symbol and Luxxxmentum name", "description":  "LITE symbol and Luxxxmentum name"})
        self.assertTrue(classify.classify() == 0)

if __name__ == "__main__":
    print('Python', python_version())

    unittest.main()
