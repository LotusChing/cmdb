# coding: utf8
from flask import current_app
from app.models import db, Idc
from app.utils import check_field_exits
from app.utils import check_output_field
from app.utils import check_order_by
from app.utils import check_limit
from app.utils import execute_get_sql
from app.utils import process_result
from app.utils import check_update_data
from app.utils import execute_update_sql


def create(**kwargs):
    # 1.  获取参数
    # 2. 验证参数
    check_field_exits(Idc, kwargs)
    # 3. 插入数据库
    idc = Idc(**kwargs)
    db.session.add(idc)
    try:
        db.session.commit()
    except Exception as e:
        current_app.warning('提交到数据库出错, 错误原因：{}'.format(e))
        raise Exception('commit error')
    # 4. 返回插入状态
    return idc.id


def get(**kwargs):
    # 条件整理
    output = kwargs.get('output', [])
    limit = kwargs.get('limit', 10)
    order_by = kwargs.get('order_by', 'id asc')
    where = kwargs.get('where', {})

    '''
    验证Output列
    1. 判断output类型
    2. 判断输出列存在
   '''
    check_output_field(Idc, output)
    current_app.logger.debug('校验输出列完成.')
    '''
    验证Order By
    1. 排序规则正确
    2. 排序列存在
   '''
    check_order_by(Idc, order_by)

    '''
    验证Limit值必须为数字
   '''
    current_app.logger.debug('开始校验Limit.')
    check_limit(limit)

    '''
    执行SQL
   '''
    data = execute_get_sql(db, Idc, where, order_by, limit)

    '''
    处理数据
   '''
    return process_result(data, output)


def update(**kwargs):
    data = kwargs.get('data', {})
    where = kwargs.get('where', {})
    check_update_data(Idc, data, where)
    return execute_update_sql(db, Idc, where, data)


def delete(**kwargs):
    where = kwargs.get('where', {})
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

    res = db.session.query(Idc).filter_by(**where).delete()
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.warning('删除失败：{}'.format(e))
        raise Exception('delete commit error')
    return res