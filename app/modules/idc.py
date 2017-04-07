# coding: utf8
from flask import current_app
from app.models import db, Idc



def create(**kwargs):
    # 1.  获取参数
    # 2. 验证参数
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
    pass


def update(**kwargs):
    pass


def delete(**kwargs):
    pass