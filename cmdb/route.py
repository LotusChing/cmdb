# coding:utf-8
import logging
from functools import wraps
from cmdb import application
from cmdb import idc_api
from cmdb import server_api
from cmdb import service_api
from flask import abort, request, Flask, render_template
from werkzeug.datastructures import ImmutableMultiDict


@application.route('/')
def index():
    return 'Index.'


@application.route('/server/list', methods=['POST', 'GET'])
def server_list():
    return server_api.list(request)


@application.route('/server/get_one_server', methods=['POST'])
def get_one_server():
    return server_api.get_one(request)


@application.route('/server/add', methods=['POST'])
def server_add():
    return server_api.add(request)


@application.route('/server/update', methods=['POST'])
def server_update():
    return server_api.update(request)


@application.route('/server/delete', methods=['POST'])
def server_delete():
    return server_api.delete(request)


@application.route('/server/search', methods=['POST'])
def server_search():
    return server_api.search(request)


@application.route('/server/filter', methods=['POST'])
def server_filter():
    return server_api.filter(request)


@application.route('/server/reports', methods=['POST'])
def server_reports():
    return server_api.reports(request)


@application.route('/idc/list', methods=['POST', 'GET'])
def idc_list():
    return idc_api.list(request)


@application.route('/idc/add', methods=['POST'])
def idc_add():
    return idc_api.add(request)


@application.route('/idc/delete', methods=['POST'])
def idc_delete():
    return idc_api.delete(request)


@application.route('/idc/get_one_idc', methods=['POST'])
def get_one_idc():
    return idc_api.get_one(request)


@application.route('/idc/update', methods=['POST'])
def idc_update():
    return idc_api.update(request)


@application.route('/service/list', methods=['POST', 'GET'])
def service_list():
    return service_api.list(request)


@application.route('/service/add', methods=['POST', 'GET'])
def service_add():
    return service_api.add(request)


@application.route('/service/get_one_service', methods=['POST', 'GET'])
def get_one_service():
    return service_api.get_one(request)


@application.route('/service/update', methods=['POST', 'GET'])
def service_update():
    return service_api.update(request)


@application.route('/service/delete', methods=['POST', 'GET'])
def service_delete():
    return service_api.delete(request)


@application.route('/service/search', methods=['POST', 'GET'])
def service_search():
    return service_api.search(request)


@application.route('/service/filter_idc_server', methods=['POST', 'GET'])
def service_filter_idc_server():
    return service_api.filter_idc_server(request)


@application.route('/service/filter_idc_server_service', methods=['POST', 'GET'])
def service_filter_idc_server_service():
    return service_api.filter_idc_server_service(request)

