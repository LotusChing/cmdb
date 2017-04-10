# coding: utf8
import json
import requests
from app.base import current_app
from app.base import AutoLoad


def api_action(method='', params={}):
    try:
        module, func = method.split('.')
    except Exception as e:
        current_app.logger.warning('method传值错误：{}'.format(e))
        return False

    at = AutoLoad()
    if not at.is_valid_module(module):
        current_app.logger.warning('{} 模块不存在'.format(module))
        return False
    if not at.is_valid_method(func):
        current_app.logger.warning('{} 下没有{}方法'.format(module, func))
        return False
    try:
        called = at.get_call_method()
        if callable(called):
            return called(**params)
        else:
            current_app.logger.warning('模块{}方法{}不可被调用'.format(module, func))
            return False
    except Exception as e:
        current_app.logger.warning('模块{}方法{}执行出错，错误信息: {}'.format(module, func, e))
        return False