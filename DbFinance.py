#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 19:35:54 2017

@author: fredoleary
"""
import sqlite3
import hashlib

class FinanceDB():
    """ Storage for news/prices etc """
    def __init__(self, stock_data):
        self.connection = None
        self.db_name = "FinanceDb"
        self.stock_data = stock_data
        self.tables = [{"name":"stocks",
                        "create_sql": """ CREATE TABLE IF NOT EXISTS stocks (
                                        symbol TEXT PRIMARY KEY,
                                        description TEXT,
                                    ); """}, \
                       {"name" :"prices",
                        "create_sql": """ CREATE TABLE IF NOT EXISTS prices (
                                        symbol TEXT,
                                        time TIMESTAMP NOT NULL,
                                        price REAL NOT NULL,
                                        UNIQUE( symbol, time)
                                    ); """}, \
                       {"name" :"news",
                        "create_sql": """ CREATE TABLE IF NOT EXISTS news (
                                        symbol TEXT,
                                        time TIMESTAMP NOT NULL,
                                        source TEXT NOT NULL,
                                        title TEXT NOT NULL,
                                        description TEXT NOT NULL,
                                        weight INTEGER NOT NULL,
                                        hash TEXT
                                    ); """}]
    def initialize(self):
        """ Initialize database connection and tables """
        self.connection = sqlite3.connect(self.db_name, \
                            detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        self._create_verify_tables()
        self._create_verify_stock_data()

    def close(self):
        """ Close db if necessary """
        if self.connection is not None:
            self.connection.close()

    def add_quotes(self, symbol, quotes):
        """ Add prices for symbol to database """
        for quote in quotes:
            self._add_quote(symbol, quote)
    def _add_quote(self, symbol, quote):
        if quote:
            try:
                cursor = self.connection.cursor()
                cursor.execute("INSERT INTO prices VALUES (?,?,?)", [symbol,\
                           quote["time"], \
                           quote["price"]])
                self.connection.commit()
                #print("value added for time: ", quote["time"])
            except sqlite3.IntegrityError:
                pass
                #print("value already added for time: ", quote["time"])

    def get_quotes(self, symbol):
        """ Fetch prices for symbol """
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM prices WHERE symbol = ?", [symbol])
        return cursor.fetchall()
    def add_news(self, symbol, news_list):
        """ Added list of news items to the database """
        if news_list:
            for news in news_list:
                news_hash = self._news_already_added(symbol, news)
                if news_hash:
                    #print("Adding news item to database")
                    cursor = self.connection.cursor()
                    cursor.execute("INSERT INTO news VALUES (?,?,?,?,?,?, ?)", [symbol,\
                               news["time"], \
                               news["source"], \
                               news["title"], \
                               news["description"], \
                               0, \
                               news_hash])
                    self.connection.commit()
    def _news_already_added(self, symbol, news):
        blake_hash = hashlib.blake2b()
        blake_hash.update(news["description"].encode())
        news_hash = blake_hash.hexdigest()
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM news WHERE symbol = ? AND  hash = ? ", [symbol, news_hash])
        rows = cursor.fetchall()
        if rows:
            #print("News item already exists in database")
            return None
        return news_hash
    def _create_verify_tables(self):
        #Get a list of all tables
        cursor = self.connection.cursor()
        cmd = "SELECT name FROM sqlite_master WHERE type='table'"
        cursor.execute(cmd)
        names = [row[0] for row in cursor.fetchall()]
        for table in self.tables:
            if not table['name'] in names:
                cursor.execute(table['create_sql'])
                #table doesn't exist, create it
    def _create_verify_stock_data(self):
        for stock in self.stock_data:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM stocks WHERE symbol = ?", [stock["symbol"]])
            rows = cursor.fetchall()
            if not rows: #empty - record does not exist
                cursor.execute("INSERT INTO stocks VALUES (?,?)",\
                               [stock["symbol"], stock["description"]])
                self.connection.commit()
        return
