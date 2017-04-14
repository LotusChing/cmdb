# coding: utf8
from flask import current_app
from app.models import db, ServerType
from app.utils import check_limit, execute_get_sql, process_result
from app.utils import check_field_exits, check_output_field, check_order_by


def create(**kwargs):
    # 1.  获取参数
    # 2. 验证参数
    check_field_exits(ServerType, kwargs)
    # 3. 插入数据库
    manufacturers = ServerType(**kwargs)
    db.session.add(manufacturers)
    try:
        db.session.commit()
    except Exception as e:
        current_app.warning('提交到数据库出错, 错误原因：{}'.format(e))
        raise Exception('commit error')
    # 4. 返回插入状态
    return manufacturers.id


def get(**kwargs):
    current_app.logger.debug('进入ServerType Get方法...')
    # 条件整理
    output = kwargs.get('output', [])
    limit = kwargs.get('limit', 10)
    order_by = kwargs.get('order_by', 'id desc')
    where = kwargs.get('where', {})
    current_app.logger.debug(where)
    '''
    验证输出列
   '''
    check_output_field(ServerType, output)

    '''
    验证Order By
    1. 排序规则正确
    2. 排序列存在
   '''
    check_order_by(ServerType, order_by)

    '''
    验证Limit
   '''
    check_limit(limit)

    '''
    执行SQL
   '''
    data = execute_get_sql(db, ServerType, where, order_by, limit)

    '''
    处理数据
   '''
    return process_result(data, output)
