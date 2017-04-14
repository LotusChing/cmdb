# coding: utf8
from __future__ import unicode_literals
from flask import request, render_template, current_app
from . import main
import app.utils
import json
from app.modules.base_class import  DBBaseClass
'''
    IDC
'''


@main.route('/resources/idc/', methods=['GET'])
def resources_idc():
    idc_tb = DBBaseClass('idc')
    res = idc_tb.get({'where': {'status': 1}})
    return render_template('resources/server_idc_list.html',
                           title='IDC信息',
                           idcs=res)


@main.route('/resources/idc/modify/<int:idc_id>', methods=['GET'])
def resources_idc_modify(idc_id):
    idc_tb = DBBaseClass('idc')
    res = idc_tb.get({'where': {'id': idc_id}})
    if res:
        return render_template('resources/server_idc_modify.html',
                               title='IDC修改',
                               idc=res[0])
    return render_template('404.html')


@main.route('/resources/idc/update', methods=['POST'])
def resources_idc_update():
    data = request.form.to_dict()
    id = data.pop('id')
    current_app.logger.debug('进入idc/update路由')
    idc_tb = DBBaseClass('idc')
    res = idc_tb.update({'data': data, "where": {'id': id}})
    jump_url = '/resources/idc/'
    return app.utils.jump(res, success_url=jump_url, error_url=jump_url)


@main.route('/resources/idc/add/', methods=['GET'])
def resources_idc_add():
        return render_template('resources/server_add_idc.html',
                               title='添加IDC',
                               show_resource=True,
                               show_idc_list=True)


@main.route('/resources/idc/doadd/', methods=['POST'])
def resources_idc_doadd():
    params = request.form.to_dict()
    idc_tb = DBBaseClass('Idc')
    res = idc_tb.create(params)
    jump_url = '/resources/idc/'
    return app.utils.jump(res, success_url=jump_url, error_url=jump_url)


@main.route('/resources/idc/delete/', methods=['POST'])
def resources_idc_delete():
    try:
        data = request.form.to_dict()
        id = data.pop('id')
        idc_tb = DBBaseClass('idc')
        res = idc_tb.update({'data': {'status': 0}, "where": {'id': id}})
        data = {
            'code': int(res)
        }
    except Exception as e:
        data = {
            'code': 0,
            'errMsg': str(e)
        }
    return json.dumps(data)

'''
    Server
'''


@main.route('/resources/server/list', methods=['GET'])
def resources_server_list():
    server_tb = DBBaseClass('server')
    status_tb = DBBaseClass('status')
    product_tb = DBBaseClass('product')
    servers = server_tb.get()
    status = status_tb.get()
    products = product_tb.get()
    return render_template('resources/server_list.html',
                           title='服务器列表',
                           servers=servers,
                           status=status,
                           products=products)


@main.route('/resources/server/add/', methods=['GET'])
def resources_server_add():
    supplier_tb = DBBaseClass('supplier')
    manufacturers_tb = DBBaseClass('manufacturers')
    status_tb = DBBaseClass('status')
    raid_tb = DBBaseClass('raid')
    power = DBBaseClass('power')
    raidtype_tb = DBBaseClass('raidtype')
    product_tb = DBBaseClass('product')
    idc_tb = DBBaseClass('idc')

    manufacturers = manufacturers_tb.get()
    suppliers = supplier_tb.get()
    status = status_tb.get()
    raids = raid_tb.get()
    powers = power.get()
    raidtypes = raidtype_tb.get()
    idcs = idc_tb.get({'where': {'status': 1}})
    products = product_tb.get( {'where': {'pid': 0}})

    return render_template('resources/server_add.html',
                           title='添加服务器',
                           manufacturers=manufacturers,
                           products=products,
                           status=status,
                           idc_info=idcs,
                           raids=raids,
                           powers=powers,
                           raidtypes=raidtypes,
                           suppliers=suppliers)


@main.route('/resources/server/doadd/', methods=['POST'])
def resources_server_doadd():
    params = request.form.to_dict()
    server_tb = DBBaseClass('Server')
    res = server_tb.create(params)
    jump_url = '/resources/idc/'
    return app.utils.jump(res, success_url=jump_url, error_url=jump_url)


'''
    Manufacturers
'''


@main.route('/resources/manufacturers/add/', methods=['GET'])
def resources_manufacturers_add():
    return render_template('resources/server_add_manufacturers.html',
                           title='添加制造商')


@main.route('/resources/server/manufacturers/doadd/', methods=['POST'])
def resources_manufacturers_doadd():
    params = request.form.to_dict()
    manufacturers_tb = DBBaseClass('manufacturers')
    res = manufacturers_tb.create(params)
    jump_url = '/resources/server/add/'
    return app.utils.jump(res, success_url=jump_url, error_url=jump_url)

'''
    Server Type
'''


@main.route('/resources/server/servertype/add/', methods=['GET'])
def resources_server_servertype_add():
    manufacturers_tb = DBBaseClass('manufacturers')
    manufacturers = manufacturers_tb.get()
    return render_template('resources/server_servertype_add.html',
                           title='添加服务器型号',
                           manufacturers=manufacturers)


@main.route('/resources/server/servertype/doadd/', methods=['POST'])
def resources_server_servertype_doadd():
    params = request.form.to_dict()
    servertype_tb = DBBaseClass('servertype')
    res = servertype_tb.create(params)
    jump_url = '/resources/server/add/'
    return app.utils.jump(res, success_url=jump_url, error_url=jump_url)


@main.route('/resources/server/servertype/list/', methods=['POST'])
def resources_servertype_list():
    current_app.logger.debug('进入ServerType路由...')
    params = request.form.to_dict()
    if params:
        servertype_tb = DBBaseClass('servertype')
        servertypes = servertype_tb.get({'where': params})
        return json.dumps(servertypes)


'''
    业务线/产品线
'''


@main.route('/resources/server/product/add/', methods=['GET'])
def resources_server_product_add():
    product_tb = DBBaseClass('product')
    products = product_tb.get()
    return render_template('resources/server_product_add.html',
                           title='添加业务线',
                           products=products)


@main.route('/resources/server/product/doadd/', methods=['POST'])
def resources_server_product_doadd():
    params = request.form.to_dict()
    product_tb = DBBaseClass('product')
    res = product_tb.create(params)
    jump_url = '/resources/server/add/'
    return app.utils.jump(res, jump_url, jump_url)


@main.route('/resources/server/product/get_server_product/', methods=['POST'])
def resources_server_product_get_server_product():
    params = request.form.to_dict()
    if params:
        product_tb = DBBaseClass('product')
        res = product_tb.get({'output': ['id', 'service_name', 'pid'], 'where': params})
        return json.dumps(res)


'''
    服务器状态
'''


@main.route('/resources/status/add/', methods=['GET'])
def resources_server_status_add():
    return render_template('resources/server_status_add.html',
                           title='添加服务器状态')


@main.route('/resources/status/doadd/', methods=['POST'])
def resources_server_status_doadd():
    params = request.form.to_dict()
    status_tb = DBBaseClass('status')
    res = status_tb.create(params)
    jump_url = '/resources/server/add/'
    return app.utils.jump(res, jump_url, jump_url)


'''
    机柜信息
'''


@main.route('/resources/cabinet/add/', methods=['GET'])
def resources_server_cabinet_add():
    idcs_tb = DBBaseClass('idcs')
    power_tb = DBBaseClass('power')
    idcs = idcs_tb.get({'where': {'status': 1}})
    powers = power_tb.get()
    return render_template('resources/server_cabinet_add.html',
                           title='添加机柜',
                           idcs=idcs,
                           powers=powers)


@main.route('/resources/cabinet/doadd/', methods=['POST'])
def resources_server_cabinet_doadd():
    params = request.form.to_dict()
    cabinet_tb = DBBaseClass('cabinet')
    res = cabinet_tb.create(params)
    jump_url = '/resources/server/add/'
    return app.utils.jump(res, jump_url, jump_url)


@main.route('/resources/cabinet/get_cabinet/', methods=['POST'])
def resources_server_cabinet_get_cabinet():
    params = request.form.to_dict()
    current_app.logger.debug('Requests Params: {}'.format(params))
    if params:
        cabinet_tb = DBBaseClass('cabinet')
        res = cabinet_tb.get({'where': params})
        current_app.logger.debug('Cabinet Result: {}'.format(res))
        return json.dumps(res)


'''
    电源功率
'''


@main.route('/resources/power/add/', methods=['GET'])
def resources_server_power_add():
    return render_template('resources/server_power_add.html',
                           title='添加机柜')


@main.route('/resources/power/doadd/', methods=['POST'])
def resources_server_power_doadd():
    params = request.form.to_dict()
    power_tb = DBBaseClass('power')
    res = power_tb.create(params)
    jump_url = '/resources/server/add/'
    return app.utils.jump(res, jump_url, jump_url)

'''
    Raid
'''


@main.route('/resources/server/raid/add/', methods=['GET'])
def resources_server_raid_add():
    return render_template('resources/server_raid_add.html',
                           title='添加RAID')


@main.route('/resources/server/raid/doadd/', methods=['POST'])
def resources_server_raid_doadd():
    params = request.form.to_dict()
    raid_tb = DBBaseClass('raid')
    res = raid_tb.create(params)
    jump_url = '/resources/server/add/'
    return app.utils.jump(res, jump_url, jump_url)


'''
    RAID Types
'''


@main.route('/resources/server/raidcardtype/add/', methods=['GET'])
def resources_server_raidcardtype_add():
    return render_template('resources/server_raidcardtype_add.html',
                           title='添加RAID类型')


@main.route('/resources/server/raidcardtype/doadd/', methods=['POST'])
def resources_server_raidcardtype_doadd():
    params = request.form.to_dict()
    raidcardtype_tb = DBBaseClass('raidcardtype')
    res = raidcardtype_tb.create(params)
    jump_url = '/resources/server/add/'
    return app.utils.jump(res, jump_url, jump_url)


'''
    供应商
'''


@main.route('/resources/server/supplier/add/', methods=['GET'])
def resources_server_supplier_add():
    return render_template('resources/server_supplier_add.html',
                           title='添加供应商')


@main.route('/resources/server/supplier/doadd/', methods=['POST'])
def resources_server_supplier_doadd():
    params = request.form.to_dict()
    supplier_tb = DBBaseClass('supplier')
    res = supplier_tb.create(params)
    jump_url = '/resources/server/add/'
    return app.utils.jump(res, jump_url, jump_url)
