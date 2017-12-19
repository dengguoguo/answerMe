#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
#author dengguo
from flask import Flask, render_template, request, session, redirect, url_for
import config
from models import User, Question, Answer
from exts import db
from decorators import login_required

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

@app.route('/')
def index():
    content = {
    'questions' :Question.query.order_by('-create_time').all()
    }
    return render_template('index.html', **content)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        phonenumber = request.form.get('phonenumber')
        password = request.form.get('password')
        print(phonenumber, password)
        user = User.query.filter(User.phonenumber == phonenumber,
                                 User.password == password).first()
        print(user)
        if user:
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return u'phonenumber or password incorreact, please insure'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        phonenumber = request.form.get('phonenumber')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter(User.phonenumber == phonenumber).first()
        if user:
            return u'The phonenumber has been registered, please change phonenumber'
        else:
            if password1 != password2:
                return u'The password2 is not the same as password1, please insure'
            else:
                user = User(phonenumber=phonenumber,
                            username=username,
                            password=password1)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))

@app.route('/questions/', methods=['GET', 'POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title, content=content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        question.author = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/detail/<question_id>')
def detail(question_id):
    question_model = Question.query.filter(Question.id == question_id).first()
    # question_comments = Answer.query.filter(Question.id ==question_id).all()
    # print(question_comments)
    comments = question_model.answers
    print(comments)
    return render_template('detail.html', question=question_model, comments=comments)


@app.route('/add_answer/', methods=['POST'])
@login_required
def add_answer():
    comment = request.form.get('comment')
    question_id = request.form.get('question_id')

    answer = Answer(comment=comment)
    user_id = session['user_id']
    user = User.query.filter(User.id == user_id).first()
    answer.author = user
    question = Question.query.filter(Question.id == question_id).first()
    answer.question = question
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail', question_id=question_id))

if __name__ == '__main__':
    app.run()