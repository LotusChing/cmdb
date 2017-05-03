from __future__ import unicode_literals
import json
import time
import hashlib
from flask import request, session, redirect, url_for, current_app, render_template,Response
from . import main
from app.modules.base_class import DBBaseClass


@main.route('/', methods=['GET', 'POST'])
def index():
    if not request.cookies.get('tag', None) in session.values():
        print('Not found session, Redirect to login....', session)
        return redirect('/login')
    else:
        user_id = request.cookies.get('tag')
        people_tb = DBBaseClass('people')
        people_data = people_tb.get({ 'output': ['id', 'name'],'where': {'id': user_id}})
        print('Found session, Render Index....', session)
        return render_template('index.html',
                               people=people_data[0])


@main.route('/login', methods=['GET'])
def login():
    print('Render Login Page....')
    return render_template('login.html',)


@main.route('/user_login', methods=['POST'])
def user_login():
    data = request.form.to_dict()
    md5 = hashlib.md5('LotusChing'.encode())
    md5.update(data['password'].encode())
    user, passwd = data['username'], md5.hexdigest()
    people_tb = DBBaseClass('people')
    user_data = people_tb.get({'where': {'name': user, 'password': passwd}})
    if len(user_data) >= 1:
        session[data['username']] = str(user_data[0]['id'])
        res = Response(json.dumps({'code': 1}))
        res.set_cookie(key='tag', value=str(user_data[0]['id']), expires=time.time()+6*60)
        return res
    else:
        return json.dumps({'code': 0})


@main.route('/logout')
def logout():
    print(session)
    del session['user']
    print('Logout CMDB, Render index Page....')
    res = Response(render_template('login.html'))
    res.set_cookie('tag', '', expires=0)
    return res


'''
    Home
'''


@main.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')