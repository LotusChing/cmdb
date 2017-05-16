# coding: utf8
from __future__ import unicode_literals
from flask import request, render_template, current_app, redirect
from jenkinsapi.jenkins import Jenkins
from . import main
import datetime
import requests
import pymysql
import random
import hashlib
import json
import time
import os
from app.modules.base_class import DBBaseClass

'''
########
    People
########
'''


@main.route('/people', methods=['GET', 'POST'])
def people_list():
    if request.method == 'GET':
        print('Args: ', request.args)
        print('Data: ', request.data)
        print('Json: ', request.json)
        print('Form: ', request.form)
        return render_template('cmdb/people_list.html')
    else:
        current_app.logger.debug('People POST Method...')
        current_app.logger.debug('Data: {}'.format(request.json))
        page_number = request.json.get('pageNumber')
        page_size = request.json.get('pageSize')
        start_offset = (int(page_number) - 1) * int(page_size)
        people_tb = DBBaseClass('people')
        peoples_data = people_tb.get({'output': ['id', 'name', 'nickname', 'phone', 'email', 'role.name', 'remark'], 'where': {'status': 1}, 'limit': [start_offset, page_size]})
        total_data = people_tb.get({'output': ['id'], 'where': {'status': 1}, 'limit': [0, 999999999999]})
        data = {
            'total': len(total_data),
            'rows': peoples_data
        }
        current_app.logger.info(json.dumps(data))
        return json.dumps(data)


@main.route('/people/add', methods=['GET', 'POST'])
def people_add():
    try:
        if request.method == 'GET':
            role_tb = DBBaseClass('role')
            roles = role_tb.get()
            return render_template('cmdb/PeopleManageAdd.html',
                                   roles=roles)
        else:
            data = json.loads(request.data.decode(), encoding='utf8')
            md5 = hashlib.md5('LotusChing'.encode())
            md5.update(data['password'].encode())
            data['password'] = md5.hexdigest()
            people_tb = DBBaseClass('people')
            res = people_tb.create(data)
            if res:
                data = {
                    'code': 1
                }
    except Exception as e:
        data = {
            'code': 0,
            'errMsg': str(e)
        }
    return json.dumps(data)


@main.route('/people/update/<int:people_id>', methods=['GET', 'POST'])
def people_update(people_id):
    people_tb = DBBaseClass('people')
    if request.method == 'GET':
        people_data = people_tb.get({'where': {'id': people_id}})
        return render_template('cmdb/PeopleManageUpdate.html',
                               people=people_data[0])
    else:
        data = request.form.to_dict()
        print(data)
        res = people_tb.update({'data': data, "where": {'id': people_id}})
        if res:
            return redirect('/people')


@main.route('/people/delete', methods=['POST'])
def people_delete():
    try:
        ids = json.loads(request.data.decode(), encoding='utf8')['id']
        people_tb = DBBaseClass('people')
        for id in ids:
            people_tb.update({'data': {'status': 0}, "where": {'id': id}})
        data = {
            'code': 1
        }
    except Exception as e:
        data = {
            'code': 0,
            'errMsg': str(e)
        }
    return json.dumps(data)

'''
########
    IDC
########
'''


@main.route('/idc', methods=['GET', 'POST'])
def idc_list():
    try:
        if request.method == 'GET':
            return render_template('cmdb/idc_list.html')
        else:
            current_app.logger.debug('IDC POST Method...')
            current_app.logger.debug('Data: {}'.format(request.json))
            page_number = request.json.get('pageNumber')
            page_size = request.json.get('pageSize')
            start_offset = (int(page_number) - 1) * int(page_size)
            idc_tb = DBBaseClass('idc')
            idcs_data = idc_tb.get({'output': ['id', 'name', 'idc_name', 'address', 'people.name', 'people.phone', 'idc_interface', 'idc_phone', 'rel_cabinet_num'], 'where': {'status': 1}, 'limit': [start_offset, page_size]})
            total_data = idc_tb.get({'output': ['id'], 'where': {'status': 1}, 'limit': [0, 999999999999]})
            data = {
                'total': len(total_data),
                'rows': idcs_data
            }
            current_app.logger.info('返回数据: {}'.format(json.dumps(data)))
            return json.dumps(data)
    except Exception as e:
        current_app.logger.warning('idc list with error, msg: {}'.format(e))


@main.route('/idc/update/<int:idc_id>', methods=['GET', 'POST'])
def idc_update(idc_id):
    idc_tb = DBBaseClass('idc')
    if request.method == 'GET':
        current_app.logger.debug('IDC Update [GET] method...')
        idc_data = idc_tb.get({'where': {'id': idc_id}})
        if idc_data:
            try:
                people_tb = DBBaseClass('people')
                people_data = people_tb.get({'output': ['id', 'name', 'phone'], 'where': {'id': idc_data[0]['ops_interface']}})
                peoples_data = people_tb.get({'output': ['id', 'name'], 'where': {'status': 1}})
                current_app.logger.debug('Start Render Update Template...')
                return render_template('cmdb/IDCManageUpdate.html',
                                       idc=idc_data[0],
                                       people=people_data[0],
                                       peoples=peoples_data)
            except Exception as e:
                current_app.logger.warning('IDC Update [GET] 出现错误：{}'.format(e))
                return json.dumps({'code': 0, 'errMsg': str(e)})
    else:
        data = json.loads(request.data.decode(), encoding='utf8')
        try:
            idc_tb.update({'data': data, "where": {'id': idc_id}})
            return json.dumps({'code': 1})
        except Exception as e:
            current_app.logger.warning('IDC Update [POST] 执行更新时出现错误：{}'.format(e))
            return json.dumps({'code': 0, 'errMsg': str(e)})


@main.route('/idc/delete', methods=['POST'])
def idc_delete():
    try:
        ids = json.loads(request.data.decode(), encoding='utf8')['id']
        idc_tb = DBBaseClass('idc')
        for id in ids:
            idc_tb.update({'data': {'status': 0}, "where": {'id': id}})
        data = {
            'code': 1
        }
    except Exception as e:
        data = {
            'code': 0,
            'errMsg': str(e)
        }
    return json.dumps(data)


@main.route('/idc/add', methods=['GET', 'POST'])
def idc_add():
    try:
        if request.method == 'GET':
            people_tb = DBBaseClass('people')
            peoples = people_tb.get({'where': {'status': 1}})
            return render_template('cmdb/IDCManageAdd.html',
                                   peoples=peoples)
        else:
            data = json.loads(request.data.decode(), encoding='utf8')
            idc_tb = DBBaseClass('Idc')
            res = idc_tb.create(data)
            if res:
                return json.dumps({'code': 1})
    except Exception as e:
        return json.dumps({'code': 0, 'errMsg': str(e)})


'''
########
    Server
########
'''


@main.route('/server/report', methods=['POST'])
def server_report():
    data = json.loads(request.data.decode(), encoding='utf8')
    current_app.logger.debug('载入json数据完成...,类型：{}  数据：\n{} '.format(type(data), data))
    server_tb = DBBaseClass('server')
    try:
        current_app.logger.info('收到服务器汇报信息，正在提交至数据库')
        server_tb.create(data)
        current_app.logger.info('提交服务器汇报信息成功')
        return json.dumps({'code': 1})
    except Exception as e:
        current_app.logger.warning('提交服务器汇报信息失败, 错误信息: {}'.format(e))
        return json.dumps({'code': 0, 'errMsg': str(e)})


@main.route('/server/add', methods=['GET', 'POST'])
def server_add():
    try:
        if request.method == 'GET':
            return render_template('cmdb/ServerManageAdd.html')
        else:
            current_app.logger.debug('开始载入json数据...')
            data = json.loads(request.data.decode(), encoding='utf8')
            for key in data:
                if isinstance(data[key], list):
                    data[key] = str(data[key])
            current_app.logger.debug('载入json数据完成...,类型：{}  数据：\n{} '.format(type(data), data))
            server_tb = DBBaseClass('server')
            res = server_tb.create(data)
            if res:
                return json.dumps({'code': 1})
    except Exception as e:
        current_app.logger.warning(str(e))
        return json.dumps({'code': 0, 'errMsg': str(e)})


@main.route('/server', methods=['GET', 'POST'])
def server_list():
    try:
        if request.method == 'GET':
            return render_template('cmdb/server_list.html')
        else:
            host_tb = DBBaseClass('server')
            # servers_data = server_tb.get({'output': ['server_idc.name', 'server_product.name', 'hostname', 'os', 'manufacturers', 'server_model', 'server_people.name', ''status'], 'where': {'status': 1}, 'limit': [start_offset, page_size]})
            hosts_data = host_tb.get({'output': ['id', 'idc.idc_name', 'product.name', 'hostname', 'os', 'manufacturer', 'server_model', 'people.name', 'status'], 'where': {'status': 1}, 'limit': [0, 10]})
            total_data = host_tb.get({'output': ['id'], 'where': {'status': 1}, 'limit': [1, 999999999999]})
            data = {
                'total': len(total_data),
                'rows': hosts_data
            }
        current_app.logger.info(json.dumps(data))
        return json.dumps(data)
    except Exception as e:
        current_app.logger.warning('server with error, msg: {}'.format(e))
        return json.dumps({'code': 0, 'errMsg': str(e)})


@main.route('/server/update/<int:server_id>', methods=['GET', 'POST'])
def server_update(server_id):
    server_tb = DBBaseClass('server')
    server_data = server_tb.get({
        'output': ['idc.name', 'hostname', 'os', 'cpu_count', 'memory_size', 'product.name',  # 基础信息字段
                   'nic_info',   # 网络信息字段
                   'is_vm', 'sn', 'cpu_model', 'manufacturer', 'server_model', 'manufacture_date',  # 硬件信息字段
                   'memory_slots_count', 'memory_slot_use', 'memory_slot_info', 'disk_info'],
        'where': {'status': 1, 'id': server_id}
    })[0]
    return json.dumps(server_data)


@main.route('/server/detail/<int:server_id>', methods=['GET', 'POST'])
def server_detail(server_id):
    server_tb = DBBaseClass('server')
    server_data = server_tb.get({
        'output': ['idc.idc_name', 'idc.address', 'idc.idc_interface', 'idc.idc_phone', 'hostname', 'os', 'cpu_count', 'memory_size', 'product.name',  # 基础信息字段
                   'nic_info', 'product.cn_name', 'people.name', # 网络信息字段
                   'is_vm', 'sn', 'cpu_model', 'manufacturer', 'server_model', 'manufacture_date',  # 硬件信息字段
                   'memory_slots_count', 'memory_slot_use', 'memory_slot_info', 'disk_info'],
        'where': {'status': 1, 'id': server_id}
    })[0]
    return render_template('cmdb/server_detail.html',
                           server_data=server_data)

'''
########
    产品线
########
'''


@main.route('/product', methods=['GET', 'POST'])
def product_list():
    try:
        if request.method == 'GET':
            return render_template('cmdb/product_list.html')
        else:
            host_tb = DBBaseClass('product')
            hosts_data = host_tb.get({'output': ['id', 'name', 'cn_name', 'ops_people.name', 'dev_people.name',  'remark'],
                                      'where': {'status': 1}
                                      })
            total_data = host_tb.get({'output': ['id'], 'where': {'status': 1}, 'limit': [1, 999999999999]})
            data = {
                'total': len(total_data),
                'rows': hosts_data
            }
        current_app.logger.info(json.dumps(data))
        return json.dumps(data)
    except Exception as e:
        return json.dumps({'code': 0, 'errMsg': str(e)})


@main.route('/product/update/<int:product_id>', methods=['GET', 'POST'])
def product_update(product_id):
    try:
        people_tb = DBBaseClass('people')
        product_tb = DBBaseClass('product')
        if request.method == 'GET':
            current_app.logger.debug('Product Update [GET] 开始...')
            peoples_data = people_tb.get({'output': ['id', 'name'], 'where': {'status': 1}})
            product_data = product_tb.get({'where': {'status': 1, 'id': product_id}})
            current_app.logger.debug('Product Data: {}'.format(product_data))
            current_app.logger.debug('Product Update [GET] 结束...')
            current_app.logger.debug('Product Update [Render] 开始...')
            return render_template('cmdb/product_update.html',
                                   product=product_data[0],
                                   peoples=peoples_data)
        else:
            current_app.logger.debug('Product Update [POST] 开始...')
            data = json.loads(request.data.decode(), encoding='utf8')
            product_tb.update({'data': data, "where": {'id': product_id}})
            current_app.logger.debug('Product Update [POST] 结束...')
            return json.dumps({'code': 1})
    except Exception as e:
        current_app.logger.warning('Product Update 执行更新时出现错误：{}'.format(e))
        return json.dumps({'code': 0, 'errMsg': str(e)})


@main.route('/product/add', methods=['GET', 'POST'])
def product_add():
    try:
        product_tb = DBBaseClass('product')
        if request.method == 'GET':
            current_app.logger.debug('Product add [Get] 开始...')
            people_tb = DBBaseClass('people')
            peoples = people_tb.get({'where': {'status': 1}})
            top_level_products = product_tb.get({'where': {'pid': 0}})
            current_app.logger.debug('Product add [Get] 结束...')
            current_app.logger.debug('TOP Data: {}'.format(top_level_products))
            return render_template('cmdb/product_add.html',
                                   peoples=peoples,
                                   products=top_level_products)
        else:
            current_app.logger.debug('Product add [POST] 开始...')
            data = json.loads(request.data.decode(), encoding='utf8')
            res = product_tb.create(data)
            if res:
                current_app.logger.debug('Product add [POST] 结束...')
                return json.dumps({'code': 1})
    except Exception as e:
        current_app.logger.warning('Product add 出现错误, 错误信息: {}'.format(e))
        return json.dumps({'code': 0, 'errMsg': str(e)})


@main.route('/product/delete', methods=['GET', 'POST'])
def product_delete():
    try:
        ids = json.loads(request.data.decode(), encoding='utf8')['id']
        product_tb = DBBaseClass('product')
        for id in ids:
            product_tb.update({'data': {'status': 0}, "where": {'id': id}})
        data = {
            'code': 1
        }
    except Exception as e:
        data = {
            'code': 0,
            'errMsg': str(e)
        }
    return json.dumps(data)


'''
    Zabbix
'''


@main.route('/zabbix/graph/<string:hostname>/<string:graph_name>', methods=['GET'])
def get_zabbix_graph(hostname, graph_name):
    try:
        zbx_api_url = 'http://zabbix.aiplatform.com.cn/zabbix/api_jsonrpc.php'
        zbx_login_url = 'http://zabbix.aiplatform.com.cn/index.php'
        logindata = {
            'autologin': '1',
            'name': 'LotusChing',
            'password': 'LotusChing',
            'enter': 'Sign in'
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0',
            'Content-type': 'application/x-www-form-urlencoded'
        }
        zabbix_session = requests.session()
        zabbix_session.post(zbx_login_url, params=logindata, headers=headers, verify=True)
        params = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": "LotusChing",
                "password": "LotusChing"
            },
            "id": 1
        }
        resp = zabbix_session .post(zbx_api_url, json=params)
        current_app.logger.debug(resp.cookies)
        zbx_auth = json.loads(resp.content.decode())['result']
        if zabbix_session.cookies['zbx_sessionid']:
            current_app.logger.debug('zabbix login successful.')
            resp = zabbix_session.post(zbx_api_url, json=params)
            if json.loads(resp.content.decode())['id'] is 1:
                current_app.logger.debug('Host get successful, Data: {}'.format(resp.content))
                params = {
                    "jsonrpc": "2.0",
                    "method": "graph.get",
                    "params": {
                        "output": ['name', 'graphid'],
                        "filter": {
                            "host": [hostname]
                        }
                    },
                    "auth": zbx_auth,
                    "id": 1
                }
                resp = zabbix_session.post(zbx_api_url, json=params)
                if json.loads(resp.content.decode())['id'] is 1:
                    current_app.logger.debug('Get graph [id, name] successful, ready to get image data...')
                    host_graphs = json.loads(resp.content.decode())['result']
                    for graph in host_graphs:
                        if graph['name'] == graph_name:
                            cpu_load_graphid = graph['graphid']
                            image_url = 'http://zabbix.aiplatform.com.cn/chart2.php?graphid={}&period=3600&stime={}&width=1120&height=120'.format(cpu_load_graphid, int(time.time()) - 3600)
                            current_app.logger.debug('Image url: {}'.format(image_url))
                            resp = zabbix_session.get(image_url, verify=True)
                            img_dir = str(os.getcwd()) + '/app/static/img/'
                            f = open('{}/{}-{}.png'.format(img_dir, hostname, graph_name), 'wb')
                            [f.write(chunk) for chunk in resp.iter_content(chunk_size=512 * 1024) if chunk]
                            f.close()
                            current_app.logger.debug('zabbix graph image get successful.')
                            return json.dumps({'code': 1, 'graph_url': '../../static/img/{}-{}.png?{}'.format(hostname, graph_name, random.randint(1, 999))})
    except Exception as e:
        current_app.logger.debug('Get zabbix graph with problem, msg: {}'.format(e))
        return json.dumps({'code': 0, 'errMsg': str(e)})

'''
    Test Route
'''


@main.route('/jenkins/build_history', methods=['GET'])
def build_history():
    item = request.json['item'].split('-')[1]
    jenkins_url = 'http://120.24.80.34:2222'
    server = Jenkins(jenkins_url, username='wecan', password='wecan405')
    auth = ('wecan', 'wecan405')
    jenkins_session = requests.session()
    current_app.logger.debug('Logging into jenkins...')
    resp = jenkins_session.post('http://120.24.80.34:2222/api/json', auth=auth)
    current_app.logger.debug('Logging success, getting all jobs info...')
    all_jobs_info = json.loads(resp.content.decode())
    job_name_list = [job['name'] for job in all_jobs_info['jobs'] if item in job['name']]
    data = []
    for job in job_name_list:
        current_app.logger.debug('[{}] getting job latest 10 ids...'.format(job))
        job_instance = server.get_job(job)
        res = job_instance.get_build_ids()
        last_10_build_ids = list(res)[:6]
        # 取出最近10条jenkins job build 信息
        current_app.logger.debug('[{}] getting latest 10 job data...'.format(job))
        for build_id in last_10_build_ids:
            build_data = job_instance.get_build(build_id)
            tmp_dict = {
                'id': build_id,
                'status': build_data.get_status(),
                'duration': str(build_data.get_duration()),
                'timestamp': str(build_data.get_timestamp() + datetime.timedelta(hours=8))
            }
            print(type(tmp_dict['timestamp']))
            data.append(tmp_dict)
    return json.dumps({'code': 1, 'msg': data})


@main.route('/deploy/build_result', methods=['POST'])
def test():
    data = request.json
    deploy_logs_tb = DBBaseClass('deploy_logs')
    deploy_logs_tb.create(data)
    return 'OK'
