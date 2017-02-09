# coding:utf-8

import logging
from views import idc_api
from views import server_api
from views import service_api

from flask import abort, request, Flask, render_template
from werkzeug.datastructures import ImmutableMultiDict

# static file path
app = Flask(__name__, static_url_path='/static')


@app.route('/')
def index():
    return 'Index.'


@app.route('/server/list', methods=['POST', 'GET'])
def server_list():
    return server_api.list(request)


@app.route('/server/get_one_server', methods=['POST'])
def get_one_server():
    return server_api.get_one(request)


@app.route('/server/add', methods=['POST'])
def server_add():
    return server_api.add(request)


@app.route('/server/update', methods=['POST'])
def server_update():
    return server_api.update(request)


@app.route('/server/delete', methods=['POST'])
def server_delete():
    return server_api.delete(request)


@app.route('/server/search', methods=['POST'])
def server_search():
    return server_api.search(request)


@app.route('/server/filter', methods=['POST'])
def server_filter():
    return server_api.filter(request)


@app.route('/server/reports', methods=['POST'])
def server_reports():
    return server_api.reports(request)


@app.route('/idc/list', methods=['POST', 'GET'])
def idc_list():
    return idc_api.list(request)


@app.route('/idc/add', methods=['POST'])
def idc_add():
    return idc_api.add(request)


@app.route('/idc/delete', methods=['POST'])
def idc_delete():
    return idc_api.delete(request)


@app.route('/idc/get_one_idc', methods=['POST'])
def get_one_idc():
    return idc_api.get_one(request)


@app.route('/idc/update', methods=['POST'])
def idc_update():
    return idc_api.update(request)


@app.route('/service/list', methods=['POST', 'GET'])
def service_list():
    return service_api.list(request)


@app.route('/service/add', methods=['POST', 'GET'])
def service_add():
    return service_api.add(request)


@app.route('/service/get_one_service', methods=['POST', 'GET'])
def get_one_service():
    return service_api.get_one(request)


@app.route('/service/update', methods=['POST', 'GET'])
def service_update():
    return service_api.update(request)


@app.route('/service/delete', methods=['POST', 'GET'])
def service_delete():
    return service_api.delete(request)


@app.route('/service/search', methods=['POST', 'GET'])
def service_search():
    return service_api.search(request)


@app.route('/service/filter_idc_server', methods=['POST', 'GET'])
def service_filter_idc_server():
    return service_api.filter_idc_server(request)


@app.route('/service/filter_idc_server_service', methods=['POST', 'GET'])
def service_filter_idc_server_service():
    return service_api.filter_idc_server_service(request)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(host='0.0.0.0', port=5002)
