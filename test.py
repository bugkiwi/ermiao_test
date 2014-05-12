#!/usr/bin/env python
#coding:utf-8
from datetime import datetime
from pprint import pprint
import random

from model import EntryModel,UserModel,_drop_all,_create_all
from weight import Entry
from _redis import _flushdb
    
def create_user(name):
    #清表
    u=UserModel(name=name,has_pet=False)
    u.insert()
    print '创建用户:',u.name
    return u

def create_entry(user):
    entry=EntryModel(uid=user.uid,create_time=datetime.now(),update_time=datetime.now())
    entry.insert()
    Entry.add(user.uid,entry.eid)
    print '用户:%s 创建Entry:%s'%(user.name,entry.eid)
    return entry




users=[]
entries=[]
def test_init():
    print '*'*79
    _flushdb()
    _drop_all()
    _create_all()

    for i in range(100):
        users.append(create_user("u%s"%i))
    for i in range(200):
        user=random.choice(users)
        entry=create_entry(user)
        entries.append(entry)
        Entry.add(user.uid,entry.eid)

def testA():
    """测试邮件中所说数组A的策略
    """
    for i in xrange(60):
        """未去重,可重复喜欢"""
        entry=random.choice(entries)
        Entry.favor(entry.eid)

    for i in xrange(500):
        entry=random.choice(entries)
        Entry.comment(entry.eid) 

    print '#'*30
    pprint(Entry.time_line())

def testB():
    """测试数组B策略
    """
    pass

if __name__=='__main__':
    test_init()
    testA()
