import json
import logging
from cmdb import util
from cmdb import application
from werkzeug.datastructures import ImmutableMultiDict


def list(request):
    try:
        req_data = dict(ImmutableMultiDict(request.form))
        pageNumber = req_data['pageNumber'][0]
        pageSize = req_data['pageSize'][0]
        start_pos = (int(pageNumber) - 1) * int(pageSize)
        count_data = util.SQL('select count(id) from server;')[0][0]
        data = util.SQL('select * from server limit {}, {};'.format(start_pos, pageSize))
        jsonData = []
        for row in data:
            idc_data = util.SQL('select name from idc where id="{}"'.format(row[1]))
            myjson = {'id': row[0], 'idc_name': idc_data[0][0],  'os': row[2], 'ip': row[3], 'hostname': row[4], 'cpu': row[5], 'memory':row[6], 'disk':row[7],'net_type':row[8],'server_type':row[9],'manufacturer':row[10], 'model':row[11],'sn':row[12],'uuid':row[13],'sku':row[14]}
            jsonData.append(myjson)
        totalPages = int(count_data) // int(pageSize)
        return json.dumps({'code': 1, 'data': jsonData, 'totalPages': totalPages if int(count_data) % int(pageSize) == 0 else totalPages + 1}) # 不能整除则+1
    except Exception as f:
        return json.dumps({'code': 0, 'info': f}, encoding='utf8')


def get_one(request):
    try:
        req_data = dict(ImmutableMultiDict(request.form))
        server_id = req_data['id'][0]
        data = util.SQL('select * from server where id={}'.format(server_id))
        idc_data = util.SQL('select name from idc where id="{}"'.format(data[0][1]))
        return json.dumps({'code': 1, 'data': {'idc_name': idc_data[0][0],  'os': data[0][2], 'ip': data[0][3], 'hostname': data[0][4], 'cpu': data[0][5], 'memory':data[0][6], 'disk':data[0][7],'net_type':data[0][8],'server_type':data[0][9],'manufacturer':data[0][10], 'model':data[0][11],'sn':data[0][12],'uuid':data[0][13],'sku':data[0][14]}})
    except Exception as f:
        return json.dumps({'code': 0, 'info': f}, encoding='utf8')


def add(request):
    try:
        data = dict(ImmutableMultiDict(request.form))
        server_data = {
            'area': data['area'][0],
            'servername': data['servername'][0],
            'ip': data['ip'][0],
            'servertype': data['servertype'][0]
        }
        util.SQL("insert into server_info(area,  servername, ip, servertype) values ('{area}', '{servername}', '{ip}',  '{servertype}');".format(**server_data))
        return json.dumps({'code': 1})
    except Exception as f:
        logging.info(f)
        return json.dumps({'code': 0, 'info': f}, encoding='utf8')


def delete(request):
    try:
        data = dict(ImmutableMultiDict(request.form))
        for id in data['ids']:
            util.SQL("delete from server where id={}".format(id))
        return json.dumps({'code': 1})
    except Exception as f:
        logging.info(f)
        return json.dumps({'code': 0, 'info': f}, encoding='utf8')


def update(request):
    try:
        req_data = dict(ImmutableMultiDict(request.form))
        idc_name = req_data['idc_name'][0]
        id_data = util.SQL('select id from idc where name="{}"'.format(idc_name))
        data = {
            'id': req_data['id'][0],
            'idc_id': id_data[0][0],
            'ip': req_data['ip'][0],
            'hostname': req_data['hostname'][0],
            'cpu': req_data['cpu'][0],
            'memory': req_data['memory'][0],
            'disk': req_data['disk'][0]
        }
        util.SQL("update server set idc_id='{idc_id}',ip='{ip}',hostname='{hostname}',cpu='{cpu}',memory='{memory}',disk='{disk}' where id={id}".format(**data))
        return json.dumps({'code': 1})
    except Exception as f:
        logging.info(f)
        return json.dumps({'code': 0, 'info': f}, encoding='utf8')


def reports(request):
    try:
        virtual_os_list=['KVM','VMware Virtual Platform','VirtualBox','Bochs','Virtual Machine', 'HVM domU']
        idc_info = {
            'bj': '1'
        }
        server_info = json.loads(request.data.decode())
        ip_list=[ip.split(': ')[1] for ip in server_info['ip_list'].strip(', ').split(', ')]
        data = {
            'idc_id': idc_info[server_info['hostname'].split('-')[0]],
            'ip': ''.join([ip+'  ' for ip in ip_list]),
            'os': server_info['os'],
            'hostname': server_info['hostname'],
            'cpu': server_info['processor'],
            'memory': server_info['memory_size'],
            'disk': server_info['disk_size'],
            'net_type': server_info['net_type'],
            'server_type': 0 if server_info['model'] in virtual_os_list else 1,
            'manufacturer': server_info['manufacturer'],
            'model': server_info['model'],
            'sn': server_info['sn'],
            'uuid': server_info['uuid'],
            'sku': 0 if server_info['sku'].strip() == 'Not Specified' else server_info['sku'].strip()
        }
        util.SQL("insert into server(idc_id, os, ip, hostname, cpu, memory, disk, net_type, server_type, manufacturer, model, sn, uuid, sku)VALUES ('{idc_id}', '{os}', '{ip}', '{hostname}', '{cpu}', '{memory}', '{disk}', '{net_type}', '{server_type}', '{manufacturer}', '{model}', '{sn}', '{uuid}', '{sku}')".format(**data))
        return json.dumps({'code': 1})
    except Exception as f:
        logging.info(f)
        return json.dumps({'code': 0, 'info': f}, encoding='utf8')


def search(request):
    try:
        req_data = dict(ImmutableMultiDict(request.form))
        pageNumber = req_data['pageNumber'][0]
        pageSize = req_data['pageSize'][0]
        start_pos = (int(pageNumber) - 1) * int(pageSize)
        data = {
            'keywords': req_data['keywords'][0],
            'start_pos': start_pos,
            'pageSize': pageSize
        }
        count_data = util.SQL("select count(id) from server s where s.os like '%{keywords}%' or s.ip like '%{keywords}%' or s.hostname like '%{keywords}%' or s.manufacturer like '%{keywords}%';".format(**data))[0][0]
        data = util.SQL("select * from server s where s.os like '%{keywords}%' or s.ip like '%{keywords}%' or s.hostname like '%{keywords}%' or s.manufacturer like '%{keywords}%' limit {start_pos}, {pageSize};".format(**data))
        jsonData = []
        for row in data:
            idc_data = util.SQL('select name from idc where id="{}"'.format(row[1]))
            myjson = {'id': row[0], 'idc_name': idc_data[0][0],  'os': row[2], 'ip': row[3], 'hostname': row[4], 'cpu': row[5], 'memory':row[6], 'disk':row[7],'net_type':row[8],'server_type':row[9],'manufacturer':row[10], 'model':row[11],'sn':row[12],'uuid':row[13],'sku':row[14]}
            jsonData.append(myjson)
        totalPages = int(count_data) // int(pageSize)
        return json.dumps({'code': 1, 'data': jsonData, 'matchRows':count_data, 'totalPages': totalPages if int(count_data)% int(pageSize) == 0 else totalPages + 1})
    except Exception as f:
        return json.dumps({'code': 0, 'info': f}, encoding='utf8')


def filter(request):
    try:
        req_data = dict(ImmutableMultiDict(request.form))
        idc_name = req_data['idc_name'][0]
        id_data = util.SQL('select id from idc where name="{}"'.format(idc_name))
        data = util.SQL('select * from server where idc_id={};'.format(id_data[0][0]))
        jsonData = []
        for row in data:
            idc_data = util.SQL('select name from idc where id="{}"'.format(row[1]))
            myjson = {'id': row[0], 'idc_name': idc_data[0][0],  'os': row[2], 'ip': row[3], 'hostname': row[4], 'cpu': row[5], 'memory':row[6], 'disk':row[7],'net_type':row[8],'server_type':row[9],'manufacturer':row[10], 'model':row[11],'sn':row[12],'uuid':row[13],'sku':row[14]}
            jsonData.append(myjson)
        print(jsonData)
        return json.dumps({'code': 1, 'data': jsonData})
    except Exception as f:
        return json.dumps({'code': 0, 'info': f}, encoding='utf8')
