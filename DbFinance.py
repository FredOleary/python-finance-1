#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 19:35:54 2017

@author: fredoleary
"""
import sqlite3
import hashlib
import logging

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
                                        name TEXT NOT NULL
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
                                        aggregator TEXT,
                                        hash TEXT,
                                        sentiment TEXT
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

    def get_stock_data(self):
        """ Stock_data accessor """
        return self.stock_data

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

    def get_without_sentiment(self):
        """ access all rows where sentiment has not been set """
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM news WHERE sentiment IS NULL")
        rows = cursor.fetchall()
        return rows


    def get_news_with_sentiment(self):
        """ access all rows where sentiment has been set """
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM news WHERE sentiment IS NOT NULL")
        rows = cursor.fetchall()
        return rows

    def get_prices_before(self, symbol, time):
        """ get prices up to time """
        query = "SELECT * FROM prices WHERE symbol = ? AND time <= ? ORDER BY TIME DESC LIMIT 5"
        cursor = self.connection.cursor()
        cursor.execute(query, [symbol, time])
        rows = cursor.fetchall()
        return rows

    def get_prices_after(self, symbol, time):
        """ get prices onwards from time """
        query = "SELECT * FROM prices WHERE symbol = ? AND time >= ? ORDER BY TIME ASC LIMIT 5"
        cursor = self.connection.cursor()
        cursor.execute(query, [symbol, time])
        rows = cursor.fetchall()
        return rows

    def update_sentiment(self, hash_val, sentiment):
        """ set sentiment for row """
        update_sql = "UPDATE news SET sentiment = ? WHERE hash = ? "
        cursor = self.connection.cursor()
        cursor.execute(update_sql, [sentiment, hash_val])
        cursor.close()
        self.connection.commit()

    def update_weight(self, hash_val, weight):
        """ set weight for row """
        update_sql = "UPDATE news SET weight = ? WHERE hash = ? "
        cursor = self.connection.cursor()
        cursor.execute(update_sql, [weight, hash_val])
        cursor.close()
        self.connection.commit()

    def get_quotes(self, symbol):
        """ Fetch prices for symbol """
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM prices WHERE symbol = ?", [symbol])
        return cursor.fetchall()
    def add_news(self, symbol, news_list, aggregator):
        """ Added list of news items to the database """
        if news_list:
            for news in news_list:
                news_hash = self._news_already_added(symbol, news)
                if news_hash:
                    #print("Adding news item to database")
                    cursor = self.connection.cursor()
                    cursor.execute("INSERT INTO news VALUES (?,?,?,?,?,?,?,?,?)", [symbol,\
                               news["time"], \
                               news["source"], \
                               news["title"], \
                               news["description"], \
                               0, \
                               aggregator, \
                               news_hash, \
                               None])
                    self.connection.commit()
    def _news_already_added(self, symbol, news):
        try:
            blake_hash = hashlib.blake2b()
            if news["description"] is not None:
                blake_hash.update(news["description"].encode())
                news_hash = blake_hash.hexdigest()
                cursor = self.connection.cursor()
                cursor.execute("SELECT * FROM news WHERE symbol = ? AND  hash = ? ",\
                               [symbol, news_hash])
                rows = cursor.fetchall()
                if rows:
                    #print("News item already exists in database")
                    return None
                return news_hash
            else:
                return None
        except Exception as ex:
            logging.error(" failed to hash..." + str(ex))
            return None

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
                cursor.execute("INSERT INTO stocks VALUES (?,?,?)",\
                               [stock["symbol"], stock["description"], stock["name"]])
                self.connection.commit()
        return
