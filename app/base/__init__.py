#!/usr/bin/env python
# coding:utf-8
import os
import imp
from flask import current_app


class AutoLoad():
    """
        Auto Load Class
    """
    def __init__(self):
        self.modules_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules'))
        current_app.logger.debug('当前模块目录为: {}'.format(self.modules_dir))
        self.module_name = ""                                       # 模块名称
        self.module = None                                            # 已载入的模块
        self.func = None                                                # 已载入的模块

    def is_valid_module(self, module_name):
        """
        验证模块是否可用
        :param module_name: 需要导入的模块名
        :return: True/False
        """
        current_app.logger.debug('正在验证模块是否可用，模块名为：{}'.format(module_name))
        self.module_name = module_name
        return self._load_module()

    def is_valid_method(self, func):
        """
        验证方法是否可用
        :param func: 需要导入的函数
        :return: True/False
        """
        self.func = func
        current_app.logger.debug('正在验证模块 {} 下 {} 方法是否存在'.format(self.module_name, self.func))
        if self.module is None:
            current_app.warning('函数验证失败，模块{}为空'.format(self.module_name))
            return False
        return hasattr(self.module, self.func)

    def get_call_method(self):
        """
        返回可执行的方法
        :return: func/none
        """
        current_app.logger.debug('正在获取{}模块{}方法'.format(self.module_name, self.func))
        if hasattr(self.module, self.func):
            return getattr(self.module, self.func)
        return None

    def _load_module(self):
        """
        动态加载模块
        :return:
        """
        current_app.logger.debug('开始加载{}模块'.format(self.module_name))
        res = False
        # 遍历模块目录
        for file_name in os.listdir(self.modules_dir):
            # 过滤出.py文件
            if file_name.endswith('.py'):
                # 取出模块名
                module_name = file_name.rstrip('.py')
                if self.module_name == module_name:
                    # 获取具体模块信息，以供后面load_module使用
                    current_app.logger.debug('正在获取{}模块详细信息'.format(module_name))
                    fp, path_name, desc = imp.find_module(module_name, path=[self.modules_dir])
                    if not fp:
                        # 模块信息查找失败
                        current_app.logger.warning('获取{}模块详细失败'.format(module_name))
                        continue
                    try:
                        # 导入模块
                        current_app.logger.debug('加载{}模块成功'.format(module_name))
                        self.module = imp.load_module(module_name, fp, path_name, desc)
                        res = True
                    except Exception as e:
                        current_app.logger.warning('加载{}模块失败，失败原因：{}'.format(module_name, e))
                    finally:
                        # 关闭文件描述符
                        fp.close()
                    break
        return res


class Response():
    def __init__(self):
        self.data = None                      # 调用返回数据
        self.errorCode = 0                  # 执行结果状态码
        self.errorMessage = None      # 执行结果状态信息


class JsonRpc():
    def __init__(self):
        self.jsonData = None
        self.VERSION = "2.0"
        self._response = {}

    def execute(self):
        current_app.logger.debug('进入API执行，开始校验Json')

        if self.validate():
            # 验证通过
            current_app.logger.debug('校验Json成功')
            params = self.jsonData['params']
            auth = self.jsonData['auth']
            module, func = self.jsonData['method'].split('.')
            res = self.call_method(module, func, params, auth)
            self.process_result(res)
        return self._response

    def validate(self):
        """
        验证Json数据格式
        # jsonrpc      值必须为  2.0
        # method      必须要有"."，且用点分割的只有两个元素，不能为空
        # id               整型
        # auth           必须要有，可以为None
        # params       必须为dict，dict可以为空
        :return: True/False
        """
        # 判断Json数据是否传递
        current_app.logger.debug('开始校验Json数据是否有效')
        if self.jsonData is None:
            self.json_error(-1, 101, '没有传Json数据')
            current_app.logger.warning('没有传Json数据')
            return False
        if 'id' not in self.jsonData:
            self.json_error(-1, 102, '没有传ID')
            current_app.logger.warning('没有传ID')
            return False
        code = 102
        for k in ['jsonrpc', 'method', 'auth', 'params']:
            code += 1
            if not k in self.jsonData:
                self.json_error(self.jsonData['id'], code, "{} 没有传".format(k))
                current_app.logger.warning('没有传{}'.format(k))
                return False
        # 判断Json数据是否合法
        if str(self.jsonData['jsonrpc']) != "2.0":
            self.json_error(self.jsonData['id'], 107, "jsonrpc 版本不正确，应该为{}".format(self.VERSION))
            current_app.logger.warning('jsonrpc 版本不正确，应该为'.format(self.VERSION))
            return False
        if not isinstance(self.jsonData['method'], str):
            self.json_error(self.jsonData['id'], 108, 'method 格式不正确，应为字符串类型 "module.method"')
            current_app.logger.warning('method 格式不正确')
            return False
        action = list(filter(None, self.jsonData['method'].strip().split('.')))
        if len(action) != 2:
            self.json_error(self.jsonData['id'], 109, 'method 格式不正确，应为字符串类型 "module.method"')
            current_app.logger.warning('method 格式不正确')
            return False
        if not isinstance(self.jsonData['id'], int):
            self.json_error(self.jsonData['id'], 110, "id 类型错误，应为int整数类型")
            current_app.logger.warning('id 类型错误')
            return False
        if not isinstance(self.jsonData['params'], dict):
            self.json_error(self.jsonData['id'], 111, "params 类型错误，应为dict字典类型")
            current_app.logger.warning('params 类型错误')
            return False
        return True

    def json_error(self, id, errno, errmsg):
        """
        处理Json错误信息
        :param id:
        :param errno:
        :param errmsg:
        :return:
        """
        current_app.logger.debug('处理Json错误')
        self._response = {
            'jsonrpc': self.VERSION,
            'id': id,
            'err_code': errno,
            'err_msg': errmsg
        }

    def require_authtication(self, module, func):
        """
        Api权限验证，白名单中的Api不需要权限验证
        :return: True/False
        """
        white_list = ['user.log', 'api.info', 'lotus.go', 'lotus.no', 'idc.create']
        if '{}.{}'.format(module, func) in white_list:
            print('###模块名称', module, func)
            return False
        return True

    def call_method(self, module, func, params, auth):
        current_app.logger.debug('开始加载模块方法 {}: {}'.format(module, func))
        """
        执行Api调用
        :param module: 模块名
        :param func:  方法名
        :param params:  参数
        :param auth:  认证信息
        :return:
      """
        module_name, func_name = module.lower(), func.lower()
        response = Response()
        at = AutoLoad()
        if not at.is_valid_module(module_name):
            response.errorCode = 120
            response.errorMessage = '{} 模块不存在'.format(module_name)
            current_app.logger.warning('{} 模块不存在'.format(module_name))
            return response
        if not at.is_valid_method(func_name):
            response.errorCode = 121
            response.errorMessage = '{} 下没有{}方法'.format(module_name, func_name)
            current_app.logger.warning('{} 下没有{}方法'.format(module_name, func_name))
            return response
        current_app.logger.debug('模块方法加载成功 {}: {}'.format(module_name, func_name))
        current_app.logger.debug('检查模块方法调用是否需要验证 {}: {}'.format(module_name, func_name))
        if self.require_authtication(module_name, func_name):
            # 需要登陆/验证
            current_app.logger.debug('模块方法正在验证 {}: {}'.format(module_name, func_name))
            if auth is None or auth == '':
                response.errorCode = 122
                response.errorMessage = '{}模块{}方法不在白名单中，并且该操作需要提供正确的auth信息'.format(module_name, func_name)
        called = at.get_call_method()
        try:
            current_app.logger.debug('模块{}方法{}无需认证，正在执行该方法'.format(module_name, func_name))
            if callable(called):
                response.data = called(**params)
                current_app.logger.debug('模块 {} 方法 {} 调用成功，已返回数据: {}'.format(module_name, func_name, response.data))
            else:
                response.errorCode = 123
                response.errorMessage = '{}下{}不能被调用'.format(module_name, func_name)
                current_app.logger.debug('模块 {} 方法 {} 调用失败，已返回数据: {}'.format(module_name, func_name, response.errorMessage))
        except Exception as e:
            response.errorCode = -1
            response.errorMessage = str(e)
            current_app.logger.debug('模块 {} 方法 {} 调用异常，已返回数据: {}'.format(module_name, func_name, response.errorMessage))
        return response

    def process_result(self, response):
        """
        处理返回结果
        :param response:
        :return:
        """
        if response.errorCode != 0:
            self.json_error(self.jsonData['id'], response.errorCode, response.errorMessage)
        else:
            self._response = {
                'jsonrpc': self.VERSION,
                'result': response.data,
                'id': self.jsonData['id']
            }


if __name__ == '__main__':
    jr = JsonRpc()
    jr.jsonData = {
        'jsonrpc': '2.0',
        'method': 'lotus.go',
        'id': 4,
        'auth': None,
        'params': {
            'name': 'LotusChing',
            'Age': 22
        }
    }
    res = jr.execute()
    print(res)
