import json
import logging
from views import util
from werkzeug.datastructures import ImmutableMultiDict


def list(request):
    try:
        data = util.SQL('select * from service;')
        jsonData = []
        for row in data:
            myjson = {'id': row[0], 'name': row[2],'service_type': row[3], 'port': row[4], 'path': row[5], 'commands': row[6], 'remark': row[7]}
            jsonData.append(myjson)
        return json.dumps({'code': 1, 'data': jsonData})
    except Exception as f:
        return json.dumps({'code': 0, 'info': f}, encoding='utf8')


def add(request):
    try:
        req_data = dict(ImmutableMultiDict(request.form))
        hostname = req_data['hostname'][0]
        id_data = util.SQL('select id from server where hostname="{}"'.format(hostname))
        service_data = {
            'server_id': id_data[0][0],
            'name': req_data['name'][0],
            'service_type': req_data['service_type'][0],
            'port': req_data['port'][0],
            'path': req_data['path'][0],
            'commands': req_data['commands'][0],
            'remark': req_data['remark'][0]
        }
        util.SQL("insert into service(server_id,  name, service_type, port, path, commands, remark) values ('{server_id}', '{name}', '{service_type}',  '{port}',  '{path}',  '{commands}',  '{remark}');".format(**service_data))
        return json.dumps({'code': 1})
    except Exception as f:
        logging.info(f)
        return json.dumps({'code': 0, 'info': f}, encoding='utf8')


def get_one(request):
    try:
        req_data = dict(ImmutableMultiDict(request.form))
        server_id = req_data['id'][0]
        data = util.SQL('select * from service where id={}'.format(server_id))
        hostname = util.SQL('select hostname from server where id="{}"'.format(data[0][1]))
        return json.dumps({'code': 1, 'data': {'hostname': hostname[0][0], 'name': data[0][2], 'service_type': data[0][3], 'port': data[0][4], 'path': data[0][5], 'commands':data[0][6], 'remark':data[0][7]}})
    except Exception as f:
        return json.dumps({'code': 0, 'info': f}, encoding='utf8')


def update(request):
    try:
        req_data = dict(ImmutableMultiDict(request.form))
        hostname = req_data['hostname'][0]
        id_data = util.SQL('select id from server where hostname="{}"'.format(hostname))
        data = {
            'id': req_data['id'][0],
            'server_id': id_data[0][0],
            'name': req_data['name'][0],
            'service_type': req_data['service_type'][0],
            'port': req_data['port'][0],
            'path': req_data['path'][0],
            'commands': req_data['commands'][0],
            'remark': req_data['remark'][0]
        }
        util.SQL("update service set server_id={server_id},  name='{name}',service_type='{service_type}',port='{port}',path='{path}',commands='{commands}',remark='{remark}' where id='{id}'".format(**data))
        return json.dumps({'code': 1})
    except Exception as f:
        logging.info(f)
        return json.dumps({'code': 0, 'info': f}, encoding='utf8')


def delete(request):
    try:
        data = dict(ImmutableMultiDict(request.form))
        for id in data['ids']:
            util.SQL("delete from service where id={}".format(id))
        return json.dumps({'code': 1})
    except Exception as f:
        logging.info(f)
        return json.dumps({'code': 0, 'info': f}, encoding='utf8')


def search(request):
    try:
        req_data = dict(ImmutableMultiDict(request.form))
        keywords = req_data['keywords'] * 6
        data = util.SQL("select * from service s where s.name like '%{}%' or s.service_type like '%{}%' or s.port like '%{}%' or s.path like '%{}%' or s.commands like '%{}%' or s.remark like '%{}%';".format(*keywords))
        jsonData = []
        for row in data:
            myjson = {'id': row[0], 'name': row[2], 'service_type': row[3], 'port': row[4], 'path': row[5], 'commands': row[6], 'remark': row[7]}
            jsonData.append(myjson)
        print(jsonData)
        return json.dumps({'code': 1, 'data': jsonData})
    except Exception as f:
        logging.info(f)
        return json.dumps({'code': 0, 'info': f}, encoding='utf8')


def filter_idc_server(request):
    try:
        req_data = dict(ImmutableMultiDict(request.form))
        idc_name = req_data['idc_name'][0]
        idc_id = util.SQL('select id from idc where name="{}"'.format(idc_name))[0][0]
        data = util.SQL('select hostname from server where idc_id={};'.format(idc_id))
        jsonData = []
        for row in data:
            myjson = {'hostname': row[0]}
            jsonData.append(myjson)
        return json.dumps({'code': 1, 'data': jsonData})
    except Exception as f:
        logging.info(f)
        return json.dumps({'code': 0, 'info': f}, encoding='utf8')


def filter_idc_server_service(request):
    try:
        req_data = dict(ImmutableMultiDict(request.form))
        # 如果hostname不重复则不需要判断idc，反之则需要
        # idc_name = req_data['idc_name'][0]
        hostname = req_data['hostname'][0]
        server_id = util.SQL('select id from server where hostname="{}"'.format(hostname))[0][0]
        data = util.SQL('select * from service where server_id={};'.format(server_id))
        jsonData = []
        for row in data:
            myjson = {'id': row[0], 'name': row[2],'service_type': row[3], 'port': row[4], 'path': row[5], 'commands': row[6], 'remark': row[7]}
            jsonData.append(myjson)
        print(jsonData)
        return json.dumps({'code': 1, 'data': jsonData})
    except Exception as f:
        logging.info(f)
        return json.dumps({'code': 0, 'info': f}, encoding='utf8')