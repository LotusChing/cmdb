from app.base import current_app
from app.models import db
import app.models as models


class DBBaseClass(object):
    def __init__(self, tb_name):
        self.obj = getattr(models, tb_name.title())
        current_app.logger.debug('{}表实例化DBBaseClass'.format(self.obj.__name__))

    def create(self, data):
        current_app.logger.debug('Create Data: {}'.format(data))
        if len(data.keys()) == 0:
            current_app.logger.warning('参数错误，参数不能为空')
            raise Exception('params error: 请传参数')
        for field in data.keys():
            if not hasattr(self.obj, field):
                current_app.logger.warning('参数错误: {}表中没有{}列'.format(self.obj.__name__, field))
                raise Exception('params error: {}表中没有{}列'.format(self.obj.__name__, field))
            if data.get(field) is None:
                current_app.logger.warning('参数错误：{}表中{}列不能为空'.format(self.obj.__name__, field))
                raise Exception('params error: {}表中{}列不能为空'.format(self.obj.__name__, field))

        tb_data = self.obj(**data)
        db.session.add(tb_data)
        try:
            db.session.commit()
        except Exception as e:
            current_app.logger.warning('提交到{}出错, 错误原因：{}'.format(self.obj.__name__, e))
            raise Exception('{}: commit error'.format(self.obj.__name__))
        return tb_data.id

    def get(self, params={}):
        output = params.get('output', [])
        limit = params.get('limit', [0, 10])
        order_by = params.get('order_by', 'id asc')
        where = params.get('where', {})

        '''验证limit类型'''

        if not isinstance(limit, list):
            raise Exception('type error: limit值必须为数字.')
        else:
            start_offset, page_size = limit

        '''验证输出列'''
        if not isinstance(output, list):
            current_app.logger.warning('output 必须为列表类型.')
            raise Exception('output 必须为列表类型.')

        for field in output:
            if '.' in field: continue
            if not hasattr(self.obj, field):
                current_app.logger.warning('参数错误：{}表中没有{}列.'.format(self.obj.__name__, field))
                raise Exception('params error: {}表中没有{}列。'.format(self.obj.__name__, field))

        '''验证Orderby字段'''
        tmp_order_by = order_by.split()
        order_by_list = ['asc', 'desc']
        if len(tmp_order_by) != 2:
            current_app.logger.warning('order by: {}参数不正确，应为field asc|desc.'.format(order_by))
            raise Exception('order by参数不正确，应为: {}'.format(order_by_list))

        if tmp_order_by[1].lower() not in order_by_list:
            current_app.logger.warning('order by 排序方式不正确，应为asc|desc.')
            raise Exception('order by 排序方式不正确，应为: {}'.format(order_by_list))

        if not hasattr(self.obj, tmp_order_by[0].lower()):
            current_app.logger.warning('排序字段{}不在idc表中.'.format(tmp_order_by[0]))
            raise Exception('params error: 排序字段{}不在idc表中.'.format(tmp_order_by[0]))

        '''执行SQL'''
        current_app.logger.debug('{}: 开始执行select SQL'.format(self.obj.__name__))
        # data = db.session.query(self.obj).filter_by(**where).order_by(order_by).limit(limit).all()
        data = db.session.query(self.obj).filter_by(**where).order_by(order_by).offset(start_offset).limit(page_size).all()
        current_app.logger.debug('执行SQL完成')

        '''处理返回数据'''
        current_app.logger.debug('处理返回数据.')
        res = []
        for obj in data:
            current_app.logger.debug('Obj: {}  dir: {}'.format(obj, dir(obj)))
            if output:
                tmp = {}
                for output_field in output:
                    if '.' in output_field:
                        ref_tb_name,  ref_tb_field = output_field.split('.')
                        current_app.logger.debug('table: {} field: {}'.format(ref_tb_name, ref_tb_field))
                        ref_tb_obj = getattr(obj, ref_tb_name)
                        current_app.logger.debug('tb obj: {} type: {}'.format(dir(ref_tb_obj), type(ref_tb_obj)))
                        tmp[output_field.replace('.', '_')] = getattr(ref_tb_obj, ref_tb_field)
                    else:
                        tmp[output_field] = getattr(obj, output_field)
                res.append(tmp)
            else:
                tmp = obj.__dict__
                tmp.pop('_sa_instance_state')
                res.append(tmp)
        db.session.close()
        current_app.logger.debug('关闭SQL Session')
        return res

    def update(self, params):
        data = params.get('data', {})
        where = params.get('where', {})
        if not data:
            current_app.logger.debug('没有需要更新的.')
            raise Exception('没有需要更新的.')

        for field in data.keys():
            if not hasattr(self.obj, field):
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

        current_app.logger.debug('执行更新SQL')
        res = db.session.query(self.obj).filter_by(**where).update(data)
        try:
            db.session.commit()
        except Exception as e:
            current_app.logger.warning('提交失败：{}'.format(e))
            raise Exception('{}: update commit error'.format(self.obj.__name__))
        return res

    def delete(self, params):
        where = params.get('where', {})
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

        res = db.session.query(self.obj).filter_by(**where).delete()
        try:
            db.session.commit()
        except Exception as e:
            current_app.logger.warning('删除失败：{}'.format(e))
            raise Exception('delete commit error')
        return res