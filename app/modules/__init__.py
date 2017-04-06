import os
import imp


class AutoLoad():
    """
        Auto Load Class
    """
    def __init__(self):
        self.modules_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules'))
        self.module_name = ""                                       # 模块名称
        self.module = None                                            # 已载入的模块
        self.func = None                                                # 已载入的模块

    def is_valid_module(self, module_name):
        """
        验证模块是否可用
        :param module_name: 需要导入的模块名
        :return: True/False
        """
        self.module_name = module_name
        return self._load_module()

    def is_valid_method(self, func):
        """
        验证方法是否可用
        :param func: 需要导入的函数
        :return: True/False
        """
        self.func = func
        if self.module is None:
            return False
        return hasattr(self.module, self.func)

    def get_call_method(self):
        """
        返回可执行的方法
        :return: func/none
        """
        if hasattr(self.module, self.func):
            return getattr(self.module, self.func)
        return

    def _load_module(self):
        """
        动态加载模块
        :return:
        """
        res = False
        for file_name in os.listdir(self.modules_dir):
            if file_name.endswith('.py'):
                module_name = file_name.rstrip('.py')
                if self.module_name == module_name:
                    fp, path_name, desc = imp.find_module(module_name, path=[self.modules_dir])
                    if not fp:
                        continue
                    try:
                        self.module = imp.load_module(module_name, fp, path_name, desc)
                        res = True
                    except:
                        pass
                    finally:
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
        print('开始校验Json')
        if self.validate():
            # 验证通过
            print('校验Json成功')
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
        if self.jsonData is None:
            self.json_error(-1, 101, '没有传Json数据')
            return False

        if 'id' not in self.jsonData:
            self.json_error(-1, 102, '没有传ID')
            return False
        code = 102
        for k in ['jsonrpc', 'method', 'auth', 'params']:
            code += 1
            if not k in self.jsonData:
                self.json_error(self.jsonData['id'], code, "{} 没有传".format(k))
                return self._response

        # 判断Json数据是否合法
        if str(self.jsonData['jsonrpc']) != "2.0":
            self.json_error(self.jsonData['id'], 107, "jsonrpc 版本不正确，应该为{}".format(self.VERSION))
            return False
        if not isinstance(self.jsonData['method'], str):
            self.json_error(self.jsonData['id'], 108, 'method 格式不正确，应为字符串类型 "module.method"')
            return False
        action = list(filter(None, self.jsonData['method'].strip().split('.')))
        if len(action) != 2:
            self.json_error(self.jsonData['id'], 109, 'method 格式不正确，应为字符串类型 "module.method"')
            return False
        if not isinstance(self.jsonData['id'], int):
            self.json_error(self.jsonData['id'], 110, "id 类型错误，应为int整数类型")
            return False
        if not isinstance(self.jsonData['params'], dict):
            self.json_error(self.jsonData['id'], 111, "params 类型错误，应为dict字典类型")
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
        self._response = {
            'jsonrpc': self.VERSION,
            'id': id,
            'err_code': errno,
            'err_msg': errmsg
        }
        pass

    def require_authtication(self, module, func):
        """
        Api权限验证，白名单中的Api不需要权限验证
        :return: True/False
        """
        white_list = ['user.log', 'api.info', 'lotus.go', 'lotus.no']
        if '{}.{}'.format(module, func) in white_list:
            return False
        return True

    def call_method(self, module, func, params, auth):
        print('开始加载模块方法 {}: {}'.format(module, func))
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
            return response
        if not at.is_valid_method(func_name):
            response.errorCode = 121
            response.errorMessage = '{} 下没有{}方法'.format(module_name, func_name)
            return response
        print('模块方法加载成功 {}: {}'.format(module_name, func_name))
        print('检查模块方法调用是否需要验证 {}: {}'.format(module_name, func_name))
        if self.require_authtication(module_name, func_name):
            # 需要登陆/验证
            print('模块方法正在验证 {}: {}'.format(module_name, func_name))
            if auth is None:
                response.errorCode = 122
                response.errorMessage = '该操作需要提供auth信息'
                return response
        called = at.get_call_method()
        try:
            print('模块方法无需认证，正在调用 {}: {}'.format(module_name, func_name))
            if callable(called):
                response.data = called(**params)
                print('模块方法调用成功，已返回数据 {}: {}'.format(module_name, func_name))
            else:
                print('模块方法调用失败，已返回数据 {}: {}'.format(module_name, func_name))
                response.errorCode = 123
                response.errorMessage = '{}下{}不能被调用'.format(module_name, func_name)
        except Exception as e:
            print('模块方法调用异常，已返回数据 {}: {}'.format(module_name, func_name))
            response.errorCode = -1
            response.errorMessage = str(e)
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
