#!/usr/bin/env python
# coding:utf-8
from app import db
from _datetime import datetime


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

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
    role = db.relationship('Role')

    def __repr__(self):
        return '<User {}>'.format(self.name)


class Idc(db.Model):
    __tablename__ = 'idc'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, nullable=False, unique=True)
    idc_name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    ops_interface = db.Column(db.Integer, db.ForeignKey('people.id'))
    idc_interface = db.Column(db.String(30), nullable=False)
    idc_phone = db.Column(db.String(100), nullable=False)
    rel_cabinet_num = db.Column(db.Integer, nullable=True)
    status = db.Column(db.Integer, nullable=False, index=True, default=1)
    people = db.relationship('People')


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, default='')
    cn_name = db.Column(db.String(50), nullable=False, default='')
    icon = db.Column(db.String(50), nullable=False, default='none')
    ops_interface = db.Column(db.Integer, db.ForeignKey('people.id'), default=0)
    dev_interface = db.Column(db.Integer, db.ForeignKey('people.id'), default=0)
    pid = db.Column(db.Integer, index=True, nullable=False)
    remark = db.Column(db.String(500), nullable=False, default='')
    status = db.Column(db.Integer, nullable=False, index=True, default=1)
    ops_people = db.relationship('People', foreign_keys=[ops_interface])
    dev_people = db.relationship('People', foreign_keys=[dev_interface])



class Server(db.Model):
    __tablename__ = 'server'
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(30), index=True, default='', unique=True)
    os = db.Column(db.String(50), index=True, nullable=True, default='')
    manufacturer = db.Column(db.String(100), nullable=True, default='')
    manufacture_date = db.Column(db.Date)
    server_model = db.Column(db.String(50), nullable=True)
    sn = db.Column(db.String(50), nullable=True, default='')
    uuid = db.Column(db.String(50), index=True, default='')
    cpu_count = db.Column(db.Integer, nullable=True, default='')
    cpu_model = db.Column(db.String(50), nullable=True, default='')
    memory_size = db.Column(db.Integer, nullable=True, default='')
    memory_slots_count = db.Column(db.Integer, nullable=True, default='')
    memory_slot_use = db.Column(db.Integer, nullable=True, default='')
    memory_slot_info = db.Column(db.Text, nullable=True, default='')
    disk_info = db.Column(db.Text, nullable=True, default='')
    nic_info = db.Column(db.Text, nullable=True, default='')
    last_op_time = db.Column(db.DateTime, nullable=True, default=datetime.utcnow())
    dev_interface = db.Column(db.Integer, nullable=True, default=0)
    is_vm = db.Column(db.Integer, index=True, nullable=True, default=0)
    status = db.Column(db.Integer, nullable=False, index=True, default=1)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), default=0)
    ops_interface = db.Column(db.Integer, db.ForeignKey('people.id'), default=0)
    idc_id = db.Column(db.Integer, db.ForeignKey('idc.id'), default=0)
    people = db.relationship('People')
    product = db.relationship('Product')
    idc = db.relationship('Idc')


class Deploy_Logs(db.Model):
    __tablename__ = 'deploy_logs'
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, nullable=False)
    job_name = db.Column(db.String(50), nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    commit_id = db.Column(db.String(50), nullable=False)
    commit_people = db.Column(db.String(100), nullable=False)
    commit_message = db.Column(db.String(200), nullable=False)

