#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
#author dengguo
import os

HOST = '127.0.0.1'
POST = '3306'
DATABASE = 'zlktqa'
USERNAME = 'root'
PASSWORD = 'happya11'

DB_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,
                                                              PASSWORD, HOST, POST, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI


DEBUG = True

SECRET_KEY = os.urandom(24)

SQLALCHEMY_TRACK_MODIFICATIONS = False