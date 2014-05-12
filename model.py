#!/usr/bin/env python
#coding:utf-8
from sqlalchemy import create_engine,Column,Integer,String,Boolean,DateTime,and_
from sqlalchemy.dialects.mysql import DATE
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import MYSQL_USER,MYSQL_PASS,MYSQL_HOST,MYSQL_PORT,MYSQL_DB
#mysql+mysqldb://<user>:<password>@<host>[:<port>]/<dbname>
engine=create_engine("mysql+mysqldb://%s:%s@%s:%s/%s?charset=utf8&use_unicode=0"%(MYSQL_USER,MYSQL_PASS,MYSQL_HOST,MYSQL_PORT,MYSQL_DB),echo=False)

_MODEL=declarative_base()
Session=sessionmaker(bind=engine)
session=Session()

class EntryModel(_MODEL):
    __tablename__='UserEntry'
    eid=Column(Integer,primary_key=True)
    uid=Column(Integer,index=True)
    create_time=Column(DateTime)
    update_time=Column(DateTime)
    
    @classmethod
    def uid_by_eid(cls,eid):
        ue=session.query(cls).get(eid)
        return ue.uid

    @classmethod
    def entries_by_uid_createtime(cls,uid,lastCreateTime):
        entries=session.query(cls).filter(and_(cls.uid==uid,cls.create_time<lastDate)).all()
        return entries

    def insert(self):
        session.add(self)
        session.flush()
        session.commit()

class UserModel(_MODEL):
    __tablename__='User'
    uid=Column(Integer,primary_key=True)
    name=Column(String(256))
    has_pet=Column(Boolean)
    
    @classmethod
    def has_pet(cls,uid):
        return session.query(cls).get(uid)

    def insert(self):
        session.add(self)
        session.flush()
        session.commit()

def  _drop_all():
    _MODEL.metadata.drop_all()

def _create_all():
    _MODEL.metadata.bind=engine
    _MODEL.metadata.create_all()

_create_all()
