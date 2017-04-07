#!/usr/bin/env python
# coding:utf-8
from app import db

class Idc(db.Model):
    __tablename__                  = 'idc'
    id                                         = db.Column(db.Integer, primary_key=True)
    name                                    = db.Column(db.String(50), index=True, nullable=False, unique=True)
    idc_name                             = db.Column(db.String(50), nullable=False)
    address                               = db.Column(db.String(255), nullable=False)
    phone                                   = db.Column(db.String(20), nullable=False)
    email                                    = db.Column(db.String(30), nullable=False)
    user_interface                   = db.Column(db.String(30), nullable=False)
    user_phone                         = db.Column(db.String(20), nullable=False)
    rel_cabinet_num                = db.Column(db.Integer, nullable=False)
    pact_cabinet_num              = db.Column(db.Integer, nullable=False)

