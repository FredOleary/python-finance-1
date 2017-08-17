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

    def test(self):
        symbol = "LITE"
        description = "Lumentum"
        
        # no news item..
        classify = ClassifyNews( symbol, description, None)
        self.assertTrue(classify.classify() == 0 )

        
        # news item with symbol/description mention but not positive or negative
        classify = ClassifyNews( symbol, description, {"title":  "LITE symbol and Lumentum name", "description":  "LITE symbol and Lumentum name"})
        self.assertTrue(classify.classify() == 0 )

        # news item with symbol mention but not positive or negative
        classify = ClassifyNews( symbol, description, {"title":  "LITE symbol and Luxxxmentum name", "description":  "LITE symbol and Luxxxmentum name"})
        self.assertTrue(classify.classify() == 0 )

if __name__ == "__main__":
    print('Python', python_version())

    unittest.main()