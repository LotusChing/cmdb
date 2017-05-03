#!/usr/bin/env python
# coding:utf-8
from app import db
from _datetime import datetime


class Idc(db.Model):
    __tablename__ = 'idc'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, nullable=False, unique=True)
    idc_name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    idc_interface = db.Column(db.String(30), nullable=False)
    idc_phone = db.Column(db.String(20), nullable=False)
    rel_cabinet_num = db.Column(db.Integer, nullable=True)
    status = db.Column(db.Integer, nullable=False, index=True, default=1)
    server_conn_idc = db.relationship('Server', backref='server_idc')


class Status(db.Model):
    __tablename__ = 'status'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, default='')
    pid = db.Column(db.Integer, index=True, nullable=False)
    module_letter = db.Column(db.String(15), nullable=False, default='')
    dev_interface = db.Column(db.String(100), nullable=False, default='')
    op_interface = db.Column(db.String(100), nullable=False, default='')
    status = db.Column(db.Integer, nullable=False, index=True, default=1)


class Supplier(db.Model):
    __tablename__ = 'supplier'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, default='')


class Server(db.Model):
    __tablename__ = 'server'
    id = db.Column(db.Integer, primary_key=True)
    manufacturers = db.Column(db.String(100), nullable=True, default='')
    manufacture_date = db.Column(db.Date)
    sn = db.Column(db.String(50), nullable=True, default='')
    uuid = db.Column(db.String(50), index=True, default='')
    os = db.Column(db.String(50), index=True, nullable=True, default='')
    server_model = db.Column(db.String(50), nullable=True)
    hostname = db.Column(db.String(30), index=True, default='', unique=True)
    nic_info = db.Column(db.String(200), nullable=True, default='')
    cpu_count = db.Column(db.Integer, nullable=True, default='')
    cpu_model = db.Column(db.String(50), nullable=True, default='')
    memory_size = db.Column(db.Integer, nullable=True, default='')
    memory_slots_count = db.Column(db.Integer, nullable=True, default='')
    memory_slot_use = db.Column(db.Integer, nullable=True, default='')
    memory_slot_info = db.Column(db.String(100), nullable=True, default='')
    disk_info = db.Column(db.String(200), nullable=True, default='')
    last_op_time = db.Column(db.DateTime, nullable=True, default=datetime.utcnow())
    monitor_mail_group = db.Column(db.String(50), nullable=True, default='')
    dev_interface = db.Column(db.Integer, nullable=True, default=0)
    check_update_time = db.Column(db.DateTime)
    is_vm = db.Column(db.Integer, index=True, nullable=True, default=0)
    status = db.Column(db.Integer, nullable=False, index=True, default=1)
    idc_id = db.Column(db.Integer, db.ForeignKey('idc.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    ops_interface = db.Column(db.Integer, db.ForeignKey('people.id'))
    remark = db.Column(db.Text, nullable=True, default='')


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    peoples = db.relationship('People', backref='role')

    def __repr__(self):
        return '<Role {}>'.format(self.name)


class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    nickname = db.Column(db.String(50),  nullable=False)
    phone = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(50), nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    remark = db.Column(db.Text, nullable=True, default='')
    status = db.Column(db.Integer, nullable=False, index=True, default=1)
    idc_conn_people = db.relationship('Idc', backref='idc_people')
    server_conn_people = db.relationship('Server', backref='server_conn_people')

    def __repr__(self):
        return '<User {}>'.format(self.name)

