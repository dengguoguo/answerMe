#!/usr/bin/python
# -*- coding: utf-8 -*-
#author dengguo

# ----------------
#  mongodb modules
# ----------------

"""
users
    uid            string            # user id
    phone_number   string            # register phone
    nick_name      string            # nickname
    password       string            # password
    secret_info    json           # secret info
        {
            identify   boo         # if identify
            name        string       # name
            gender     enum         # gender
            id_card     string      # id card
        }
    country        string            # country
    province       string            # province
    create_time  string              # register time
    update_time    string            # update time


questions
    uid            string            # user id
    qid            string            # question id
    title          string            # question title
    content        string            # question content
    create_time    string            # publish time
    update_time    string            # update time


answers
    uid            string            # user id
    qid            string            # question id
    aid            string            # answer id
    comment         string          # comment
    create_time    string            # publish time
    update_time    string            # update time

"""


