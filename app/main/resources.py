# coding: utf8
from __future__ import unicode_literals
from flask import request, render_template
from . import main
import app.utils


@main.route('/resources/idc/', methods=['GET'])
def resources_idc():
    res = app.utils.api_action('idc.get')
    return render_template('resources/server_idc_list.html',
                           title='IDC信息',
                           idcs=res)


@main.route('/resources/idc/modify/<int:idc_id>', methods=['GET'])
def resources_idc_modify(idc_id):
    res = app.utils.api_action('idc.get', {'where': {'id': idc_id}})
    if res:
        return render_template('resources/server_idc_modify.html',
                               title='IDC修改',
                               idc=res[0])
    return render_template('404.html')


@main.route('/resources/idc/update', methods=['POST'])
def resources_idc_update():
    data = request.form.to_dict()
    id = data.pop('id')
    res = app.utils.api_action('idc.update', {'data': data, "where": {'id': id}})
    if res:
        return render_template('public/success.html', next_url='/resources/idc/')
    else:
        return render_template('public/error.html', next_url='/resources/idc/')