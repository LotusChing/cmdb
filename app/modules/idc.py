# coding: utf8
from flask import current_app
from app.models import db, Idc


def create(**kwargs):
    # 1.  获取参数
    # 2. 验证参数
    if len(kwargs.keys()) == 0:
        current_app.logger.warning('参数错误，参数不能为空')
        raise Exception('params error: 请传参数')
    for field in kwargs.keys():
        if not hasattr(Idc, field):
            current_app.logger.warning('参数错误：idc表中没有{}列'.format(field))
            raise Exception('params error: idc表中没有{}列'.format(field))
        if not kwargs.get(field, None):
            current_app.logger.warning('参数错误：{}列不能为空'.format(field))
            raise Exception('params error: {} 不能为空'.format(field))
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
    order_by = kwargs.get('order_by', 'id desc')
    where = kwargs.get('where', {})

    '''
    验证Output列
    1. 判断output类型
    2. 判断输出列存在
   '''
    if not isinstance(output, list):
        current_app.logger.warning('output 必须为列表类型.')
        raise Exception('output 必须为列表类型.')

    for field in output:
        if not hasattr(Idc, field):
            current_app.logger.warning('参数错误：idc表中没有{}列.'.format(field))
            raise Exception('params error: idc表中没有{}列.'.format(field))
    '''
    验证Order By
    1. 排序规则正确
    2. 排序列存在
   '''
    tmp_order_by = order_by.split()
    order_by_list = ['asc', 'desc']
    if len(tmp_order_by) != 2:
        current_app.logger.warning('order by: {}参数不正确，应为field asc|desc.'.format(order_by))
        raise Exception('order by参数不正确，应为: {}'.format(order_by_list))

    if tmp_order_by[1].lower() not in order_by_list:
        current_app.logger.warning('order by 排序方式不正确，应为asc|desc.')
        raise Exception('order by 排序方式不正确，应为: {}'.format(order_by_list))

    if not hasattr(Idc, tmp_order_by[0].lower()):
        current_app.logger.warning('排序字段{}不在idc表中.'.format(tmp_order_by[0]))
        raise Exception('params error: 排序字段{}不在idc表中.'.format(tmp_order_by[0]))

    '''
    验证Limit值必须为数字
   '''
    if not str(limit).isdigit():
        raise Exception('type error: limit值必须为数字.')
    data = db.session.query(Idc).filter_by(**where).order_by(order_by).limit(limit).all()
    db.session.close()
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


def update(**kwargs):
    data = kwargs.get('data', {})
    where = kwargs.get('where', {})
    if not data:
        current_app.logger.debug('没有需要更新的.')
        raise Exception('没有需要更新的.')

    for field in data.keys():
        if not hasattr(Idc, field):
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
    res = db.session.query(Idc).filter_by(**where).update(data)
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.warning('提交失败：{}'.format(e))
        raise Exception('update commit error')
    print(res)
    return res


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