#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# author dengguo
from flask import Flask, render_template, request, session, redirect, url_for
from ayq_pro.decorators.decorators import login_required
from ayq_pro.config.config import Config
import datetime
from flask_admin import Admin, BaseView, expose


mongo_db = Config.db
now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

app = Flask(__name__)
app.config.from_object(Config)
admin = Admin(app)


@app.route('/')
def index():
    q = mongo_db.questions.aggregate([{'$lookup':
                                           {'from': "users",
                                            "localField": "uid",
                                            "foreignField": "uid",
                                            "as": "user_info"}
                                       },
                                      {'$sort': {
                                          'create_time': -1
                                      }}
                                      ])
    questions = list(q)
    content = {
        'questions': questions
    }
    return render_template('index.html', **content)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'GET':
            return render_template('login.html')
        else:
            phonenumber = request.form.get('phonenumber')
            password = request.form.get('password')
            user = mongo_db.users.find_one({'phone_number': phonenumber,
                                            'password': password
                                            })
            if user:
                session['user_id'] = user['uid']
                session.permanent = True
                return redirect(url_for('index'))
            else:
                return u'phonenumber or password incorreact, please insure'
    except Exception as e:
        print(e)


@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        if request.method == 'GET':
            return render_template('register.html')
        else:
            phonenumber = request.form.get('phonenumber')
            username = request.form.get('username')
            password1 = request.form.get('password1')
            password2 = request.form.get('password2')

            user = mongo_db.users.find_one({'phone_number': phonenumber,
                                            })
            if user:
                return u'The phonenumber has been registered, please change phonenumber'
            else:
                if password1 != password2:
                    return u'The password2 is not the same as password1, please insure'
                else:
                    user_info = {
                        'uid': Config.RANDOM_ID,
                        'nick_name': username,
                        'phone_number': phonenumber,
                        'password': password1,
                        'secret_info': {
                            'identify': False,
                            'name': '',
                            'gender': 'unknow',
                            'id_card': ''
                        },
                        'country': 'CHINA',
                        'province': '',
                        'create_time': now_time,
                        'update_time': '',

                    }
                    mongo_db.users.insert(user_info)
                    return redirect(url_for('login'))
    except Exception as e:
        print(e)


@app.route('/questions/', methods=['GET', 'POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')

        uid = session.get('user_id')

        question_info = {
            'uid': uid,
            'qid': Config.RANDOM_ID,
            'title': title,
            'content': content,
            'create_time': now_time,
            'update_time': '',

        }
        mongo_db.questions.insert(question_info)
        return redirect(url_for('index'))


@app.route('/detail/<question_id>')
def detail(question_id):
    question_model = mongo_db.questions.aggregate([{'$lookup':
                                                        {'from': "users",
                                                         "localField": "uid",
                                                         "foreignField": "uid",
                                                         "as": "user_info"},

                                                    }])
    answers = mongo_db.answers.aggregate([{'$lookup':
                                               {'from': "users",
                                                "localField": "uid",
                                                "foreignField": "uid",
                                                "as": "user_info"},

                                           }])

    return render_template('detail.html', question=list(question_model), answers=list(answers))


@app.route('/add_answer/', methods=['POST'])
@login_required
def add_answer():
    comment = request.form.get('comment')
    question_id = request.form.get('question_id')
    uid = session['user_id']

    answer_info = {
        'uid': uid,
        'qid': question_id,
        'aid': Config.RANDOM_ID,
        'comment': comment,
        'create_time': now_time,
        'update_time': '',

    }
    mongo_db.answers.insert(answer_info)
    return redirect(url_for('detail', question_id=question_id))


@app.context_processor
def my_context_processor():
    uid = session.get('user_id')
    if uid:
        user = mongo_db.users.find_one({'uid': uid})
        if user:
            return {'user': user}
    return {}


@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
