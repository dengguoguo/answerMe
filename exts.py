#!/usr/bin/python
# -*- coding: utf-8 -*-
#author dengguo

from pymongo import MongoClient
from ayq_pro.config.config import Config

mongo_client = MongoClient(Config.MONGO_HOST, Config.MONGO_PORT)
mongo_db = mongo_client.ayq.authenticate(Config.MONGO_USER, Config.MONGO_PASSWORD, mechanism='SCRAM-SHA-1')  #ayq id database
mongo_db_user = mongo_client.users
mongo_db_questions = mongo_client.questions
mongo_db_answers = mongo_client.answers

