# coding: utf8
import json
import requests
from app.base import current_app
from app.base import AutoLoad
from flask import render_template


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
        current_app.logger.debug('获取{}模块下{}方法用以调用'.format(module, func))
        called = at.get_call_method()
        if callable(called):
            current_app.logger.debug('调用{}模块下{}方法'.format(module, func))
            return called(**params)
        else:
            current_app.logger.warning('模块{}方法{}不可被调用'.format(module, func))
            return False
    except Exception as e:
        current_app.logger.warning('模块{}方法{}执行出错，错误信息: {}'.format(module, func, e))
        return False


def check_field_exits(obj, data):
    if len(data.keys()) == 0:
        current_app.logger.warning('参数错误，参数不能为空')
        raise Exception('params error: 请传参数')
    for field in data.keys():
        if not hasattr(obj, field):
            current_app.logger.warning('参数错误: {}表中没有{}列'.format(obj.__name__, field))
            raise Exception('params error: {}表中没有{}列'.format(obj.__name__, field))
        if not data.get(field, None):
            current_app.logger.warning('参数错误：{}表中{}列不能为空'.format(obj.__name__, field))
            raise Exception('params error: {}表中{}列不能为空'.format(obj.__name__, field))


def check_output_field(obj, output):
    if not isinstance(output, list):
        current_app.logger.warning('output 必须为列表类型.')
        raise Exception('output 必须为列表类型.')

    for field in output:
        if not hasattr(obj, field):
            current_app.logger.warning('参数错误：{}表中没有{}列.'.format(obj.__name__, field))
            raise Exception('params error: {}表中没有{}列。'.format(obj.__name__, field))


def check_order_by(obj, order_by):
    tmp_order_by = order_by.split()
    order_by_list = ['asc', 'desc']
    if len(tmp_order_by) != 2:
        current_app.logger.warning('order by: {}参数不正确，应为field asc|desc.'.format(order_by))
        raise Exception('order by参数不正确，应为: {}'.format(order_by_list))

    if tmp_order_by[1].lower() not in order_by_list:
        current_app.logger.warning('order by 排序方式不正确，应为asc|desc.')
        raise Exception('order by 排序方式不正确，应为: {}'.format(order_by_list))

    if not hasattr(obj, tmp_order_by[0].lower()):
        current_app.logger.warning('排序字段{}不在idc表中.'.format(tmp_order_by[0]))
        raise Exception('params error: 排序字段{}不在idc表中.'.format(tmp_order_by[0]))
    return order_by_list


def check_limit(limit):
    if not str(limit).isdigit():
        raise Exception('type error: limit值必须为数字.')


def execute_get_sql(db, obj, where, order_by, limit):
    current_app.logger.debug('{}: 开始执行SQL'.format(obj.__name__))
    data = db.session.query(obj).filter_by(**where).order_by(order_by).limit(limit).all()
    current_app.logger.debug('执行SQL完成')
    db.session.close()
    current_app.logger.debug('关闭SQL Session')
    return data


def process_result(data, output):
    res = []
    for obj in data:
        if output:
            tmp = {}
            for output_field in output:
                tmp[output_field] = getattr(obj, output_field)
            res.append(tmp)
        else:
            tmp = obj.__dict__
            tmp.pop('_sa_instance_state')
            res.append(tmp)
    return res


def check_update_data(obj, data, where):
    if not data:
        current_app.logger.debug('没有需要更新的.')
        raise Exception('没有需要更新的.')

    for field in data.keys():
        if not hasattr(obj, field):
            current_app.logger.warning('参数错误：idc表中没有{}列，无法更新.'.format(field))
            raise Exception('params error: idc表中没有{}列，无法更新.'.format(field))

    if not where:
        current_app.logger.warning('参数错误：更新需要提供where条件.')
        raise Exception('params error: 更新需要提供where条件.')
    if not where.get('id', None):
        current_app.logger.warning('参数错误：更新需要提供where条件.')
        raise Exception('params error: 需要提供id为更新条件')

    if str(where.get('id')).isdigit():
        if int(where.get('id')) <= 0:
            current_app.logger.warning('类型错误：id的值应该为大于0的整数')
            raise Exception('type error: id的值应该为大于0的整数')
    else:
        current_app.logger.warning('类型错误：id应该为int类型')
        raise Exception('type error: id应该为int类型')


def execute_update_sql(db, obj, where, data):
    current_app.logger.debug('执行更新SQL')
    res = db.session.query(obj).filter_by(**where).update(data)
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.warning('提交失败：{}'.format(e))
        raise Exception('{}: update commit error'.format(obj.__name__))
    return res


def jump(res, success_url, error_url):
    success = 'public/success.html'
    error = 'public/error.html'
    if res:
        return render_template(success,
                               next_url=success_url,
                               title='操作成功')
    else:
        return render_template(error,
                               next_url=error_url,
                               title='操作失败')