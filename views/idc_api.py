import json
import logging
from views import util
from werkzeug.datastructures import ImmutableMultiDict


def list(request):
    try:
        data = util.SQL('select * from idc;')
        jsonData = []
        for row in data:
            myjson = {'id': row[0], 'name': row[1],'address': row[2], 'remark': row[3]}
            jsonData.append(myjson)
        return json.dumps({'code': 1, 'data': jsonData})
    except Exception as f:
        return json.dumps({'code': 0, 'info': f}, encoding='utf8')


def add(request):
    try:
        data = dict(ImmutableMultiDict(request.form))
        server_data = {
            'name': data['name'][0],
            'address': data['address'][0],
            'remark': data['remark'][0]
        }
        util.SQL("insert into idc(name,  address, remark) values ('{name}', '{address}', '{remark}');".format(**server_data))
        return json.dumps({'code': 1})
    except Exception as f:
        logging.info(f)
        return json.dumps({'code': 0, 'info': f}, encoding='utf8')


def delete(request):
    try:
        data = dict(ImmutableMultiDict(request.form))
        for id in data['ids']:
            util.SQL("delete from idc where id={}".format(id))
        return json.dumps({'code': 1})
    except Exception as f:
        logging.info(f)
        return json.dumps({'code': 0, 'info': f}, encoding='utf8')


def get_one(request):
    try:
        req_data = dict(ImmutableMultiDict(request.form))
        server_id = req_data['id'][0]
        data = util.SQL('select * from idc where id={}'.format(server_id))
        return json.dumps({'code': 1, 'data': {'name': data[0][1],  'address': data[0][2], 'remark': data[0][3]}})
    except Exception as f:
        return json.dumps({'code': 0, 'info': f}, encoding='utf8')


def update(request):
    try:
        req_data = dict(ImmutableMultiDict(request.form))
        data = {
            'id': req_data['id'][0],
            'name': req_data['name'][0],
            'address': req_data['address'][0],
            'remark': req_data['remark'][0]
        }
        util.SQL("update idc set name='{name}',address='{address}',remark='{remark}' where id={id}".format(**data))
        return json.dumps({'code': 1})
    except Exception as f:
        logging.info(f)
        return json.dumps({'code': 0, 'info': f}, encoding='utf8')