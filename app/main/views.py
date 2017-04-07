from __future__ import unicode_literals
import json

from flask import request, current_app
from . import main
from app.base import JsonRpc


@main.route('/', methods=['GET', 'POST'])
def index():
    current_app.logger.debug('访问首页.')
    return 'Index.'


@main.route('/api', methods=['GET', 'POST'])
def api():
    allowed_content = ['application/json', 'application/json-rpc']
    if request.content_type in allowed_content:
        jsonData = request.get_json()

        current_app.logger.debug('请求Json数据为{}'.format(json.dumps(jsonData)))
        jsonrpc = JsonRpc()
        jsonrpc.jsonData = jsonData
        res = jsonrpc.execute()
        return json.dumps(res, ensure_ascii=False)
    else:
        current_app.logger.debug('用户请求的Content-Type为：{}，不予处理.'.format(None if request.content_type == '' else request.content_type))
        return '200', 400
