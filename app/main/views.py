from __future__ import unicode_literals
import json
import time
import hashlib
from datetime import timedelta
from flask import request, session, redirect, app, current_app, render_template, Response
from . import main
from app.modules.base_class import DBBaseClass

def is_login():
    if not request.cookies.get('tag', None) in session.values():
        print('Not found session, Redirect to login....', session)
        return False
    return True


@main.route('/', methods=['GET', 'POST'])
def index():
    if not is_login():
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
    if not is_login():
        print('Render Login Page....')
        return render_template('login.html')
    else:
        return redirect('/')


@main.route('/user_login', methods=['POST'])
def user_login():
    data = request.form.to_dict()
    md5 = hashlib.md5('LotusChing'.encode())
    md5.update(data['password'].encode())
    user, passwd = data['username'], md5.hexdigest()
    people_tb = DBBaseClass('people')
    user_data = people_tb.get({'where': {'name': user, 'password': passwd}})
    if len(user_data) >= 1:
        session.permanent = True
        app.permanent_session_lifetime = timedelta(days=1)
        session[data['username']] = str(user_data[0]['id'])
        res = Response(json.dumps({'code': 1}))
        res.set_cookie(key='tag', value=str(user_data[0]['id']), expires=time.time()+60*60)
        return res
    else:
        return json.dumps({'code': 0})


@main.route('/logout')
def logout():
    print(session)
    print('Logout CMDB, Render index Page....')
    res = Response(render_template('login.html'))
    res.set_cookie('tag', '', expires=0)
    return res


'''
    Home
'''


def product_tree():
    test_tb = DBBaseClass('product')
    top_level_products = test_tb.get({'output': ['id', 'name', 'cn_name', 'icon'], 'where': {'pid': 0, 'status': 1}})
    data = {
        'core': {
            'data': []
        }
    }
    for top_product in top_level_products:
        top_tmp_data = {
            'text': top_product['cn_name'],
            'icon': top_product['icon'],
            'state': {
                'opened': 'true'
            }
        }
        # 查找当前产品/项目是否有子项目
        second_level_products = test_tb.get({'output': ['id', 'cn_name', 'icon'], 'where': {'pid': top_product['id'], 'status': 1}})
        if len(second_level_products) >= 1:
            top_tmp_data['children'] = []
            for second_product in second_level_products:
                second_tmp_data = {
                    'text': second_product['cn_name'],
                    'icon': second_product['icon'],
                }
                top_tmp_data['children'].append(second_tmp_data)

        data['core']['data'].append(top_tmp_data)
    return json.dumps(data)


@main.route('/home', methods=['GET', 'POST'])
def home():
    server_tb = DBBaseClass('server')
    people_tb = DBBaseClass('people')
    product_tb = DBBaseClass('product')
    deploy_logs_tb = DBBaseClass('deploy_logs')
    server_count = len(server_tb.get({'output': ['id']}))
    people_count = len(people_tb.get({'output': ['id'],  'where': {'status': 1}, 'limit': [0, 999999999999]}))
    product_line_count = len(product_tb.get({'output': ['id'],  'where': {'status': 1, 'pid': 0}, 'limit': [0, 999999999999]}))
    deploy_logs_data = deploy_logs_tb.get({'order_by': 'deploy_stime desc'})
    product_count = product_tb.row('select count(id) from product where pid>0')[0][0]
    for item in deploy_logs_data:
        item['deploy_ts'] = int(time.mktime(time.strptime(str(item['deploy_stime']), '%Y-%m-%d %H:%M:%S'))) * 1000
    current_app.logger.debug('###### Data: {} ######'.format(deploy_logs_data))
    return render_template('home.html',
                           products_tree=product_tree(),
                           server_count=server_count,
                           people_count=people_count,
                           product_line_count=product_line_count,
                           product_count=product_count,
                           deploy_logs_data=deploy_logs_data)


@main.route('/test2', methods=['GET', 'POST'])
def test2():
    product_tb = DBBaseClass('product')
    product_count = product_tb.row('select count(id) from product where pid>0')
    return