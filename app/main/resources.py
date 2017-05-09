# coding: utf8
from __future__ import unicode_literals
from flask import request, render_template, current_app, redirect
from . import main
import datetime
import hashlib
import json
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
            hosts_data = host_tb.get({'output': ['id', 'idc.name', 'product.name', 'hostname', 'os', 'manufacturer', 'server_model', 'people.name', 'status'], 'where': {'status': 1}, 'limit': [0, 10]})
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
        'output': ['idc.name', 'hostname', 'os', 'cpu_count', 'memory_size', 'product.name',  # 基础信息字段
                   'nic_info',   # 网络信息字段
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
    Test Route
'''


@main.route('/test', methods=['GET'])
def test():
    return render_template('cmdb/server_detail.html',
                           )