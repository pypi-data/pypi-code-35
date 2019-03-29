#!/usr/bin/python
# coding: utf8

# Copyright 2019 Skiply

from __future__ import unicode_literals


from .base import db_session, Base, SkiplyBase


#from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import Column, Integer, String


class Device(Base):
    ''' Device '''
    __tablename__ = 'so_boitier'
    
    id = Column(Integer, primary_key=True, autoincrement=True)

    #created_date = Column('dateajout', DateTime)

    device_skiply_id = Column('devicename', String(255))
    device_description = Column('description', String(500))

    lora_id = Column('lora_id', String(255))
    sigfox_id = Column('sf_id', String(255))

    #device_battery_level = Column('battery_level', String(255))

    #device_button1_label = Column('label_button1', String(255))
    #device_button2_label = Column('label_button2', String(255))
    #device_button3_label = Column('label_button3', String(255))
    #device_button4_label = Column('label_button4', String(255))
    #device_button5_label = Column('label_button5', String(255))

    #device_last_swipe = Column('last_badge', DateTime)
    #device_last_transmission = Column('last_transmission', DateTime)
    #device_last_data_transmission = Column('last_data', DateTime)

    #device_status = Column('status', String(100))

    #device_type = Column('device_type', String(255))


    #device_erp_ref = Column('skpf', String(255))


    #billable = Column('billable', Boolean(), default=False)
    #commissioning_on = Column('commissioning_on', DateTime, default=None)
    #data_from_api = Column('data_from_api', Boolean(), default=False)


    #entity_id = Column('client_id', Integer, ForeignKey("so_client.id"), nullable=False)

    #group_id = Column('groupe_id', Integer, ForeignKey("so_groupe.id"), nullable=False)

    #keyboard_id = Column('frontage_id', Integer, ForeignKey("so_frontage.id"), nullable=False)

    #question_id = Column('question_id', Integer, ForeignKey("so_question.id"), nullable=False)

    #network_id = Column('network_id', Integer, ForeignKey("so_network.id"), nullable=False)

    def __init__(self, skiply_id, device_description, lora_id, sigfox_id):
        self.device_skiply_id = skiply_id
        self.device_description = device_description

        self.lora_id = lora_id
        self.sigfox_id = sigfox_id

    def __repr__(self):
        return '<Device %r>' % (self.device_skiply_id)

def get_device(device_id):
    return db_session.query(Device).filter((Device.sigfox_id == device_id) | (Device.lora_id == device_id)).first()