#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 19:35:54 2017

@author: fredoleary
"""
import sqlite3
from hashlib import blake2b
from datetime import datetime  
from datetime import timedelta  

class FinanceDB():
    def __init__(self, stock_data ):
        self.dbName = "FinanceDb"
        self.stock_data = stock_data
        self.tables = [{ "name":"stocks",
                         "create_sql": """ CREATE TABLE IF NOT EXISTS stocks (
                                        symbol TEXT PRIMARY KEY,
                                        description TEXT
                                    ); """ }, \
                       { "name" :"prices",
                         "create_sql": """ CREATE TABLE IF NOT EXISTS prices (
                                        symbol TEXT,
                                        time TIMESTAMP NOT NULL,
                                        price REAL NOT NULL,
                                        UNIQUE( symbol, time)
                                    ); """ }, \
                       { "name" :"news",
                         "create_sql": """ CREATE TABLE IF NOT EXISTS news (
                                        symbol TEXT,
                                        time REAL INTEGER NOT NULL,
                                        source TEXT NOT NULL,
                                        title TEXT NOT NULL,
                                        description TEXT NOT NULL,
                                        weight INTEGER NOT NULL
                                    ); """ } ]
        
    def initialize( self ) :       
        self.connnection = sqlite3.connect(self.dbName, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        self._create_verify_tables()
        self._create_verify_stock_data()
        
    def add_quotes( self, symbol, quotes ):
        for quote in quotes:
            self._add_quote( symbol, quote )
        
    def _add_quote( self, symbol, quote ):
        if quote :
            try:
                cursor = self.connnection.cursor()
                cursor.execute("INSERT INTO prices VALUES (?,?,?)", [symbol,\
                           quote["time"], \
                           quote["price"]])
                self.connnection.commit()
            except sqlite3.IntegrityError:
                print( "value already added" )

    def get_quotes( self, symbol):
        cursor = self.connnection.cursor()
        cursor.execute("SELECT * FROM prices WHERE symbol = ?", [symbol])
        return cursor.fetchall()
        
    def add_news( self, symbol, newsList ):
        if newsList :
            for news in newsList :
                if not self._news_already_added( symbol, news ):
                    cursor = self.connnection.cursor()
                    cursor.execute("INSERT INTO news VALUES (?,?,?,?,?,?)", [symbol,\
                               news["time"].timestamp(), \
                               news["source"], \
                               news["title"], \
                               news["description"], \
                               0] )
                    self.connnection.commit()
           
    def _news_already_added( self, symbol, news ):
        tsBefore = (news["time"] - timedelta(days=1)).timestamp()
        tsAfter  = (news["time"] + timedelta(days=1)).timestamp()
        h = blake2b()
        h.update(news["description"].encode())
        newHash = h.hexdigest()
        
        cursor = self.connnection.cursor()
        cursor.execute( "SELECT * FROM news WHERE symbol = ? AND  time >= ? AND time <= ? ", [ symbol,tsBefore, tsAfter])
        rows = cursor.fetchall()
        for row in rows :
            h = blake2b()
            h.update(row[4].encode())
            existingHash = h.hexdigest()
            if existingHash == newHash :
                return True
            
        return False

        
    def _create_verify_tables(self):
        #Get a list of all tables
        cursor = self.connnection.cursor()
        cmd = "SELECT name FROM sqlite_master WHERE type='table'"
        cursor.execute(cmd)
        names = [row[0] for row in cursor.fetchall()]
        for table in self.tables :
            if not table['name'] in names:
                cursor.execute( table['create_sql'] )
                #table doesn't exist, create it 
            
    def _create_verify_stock_data(self):
        for stock in self.stock_data:
            cursor = self.connnection.cursor()
            cursor.execute( "SELECT * FROM stocks WHERE symbol = ?", [stock["symbol"]])
            rows = cursor.fetchall()
            if not rows : #empty - record does not exist
                cursor.execute("INSERT INTO stocks VALUES (?,?)",[stock["symbol"], stock["description"]] )
                self.connnection.commit()
        return


