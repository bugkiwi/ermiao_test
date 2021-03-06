#!/usr/bin/env python
#coding:utf-8
from time import time
from operator import itemgetter
import random
from datetime import datetime

from _redis import redis,redisWeightB
from model import UserModel,EntryModel
from utils import cache

class Entry(object):
    _WEIGHT_A_KEY="WEIGHT_A"
    _WEIGHT_B_KEY="WEIGHT_B"
    _ENTRY_KEY="Entry:%s"
    _LOGIN_ENTRY_KEY="LOGIN_ENTRY:%s"

    @classmethod
    def _add_weight(cls,id,weight):
        redis.zincrby(cls._WEIGHT_A_KEY,id,weight)
        cls.touch(id)

    @classmethod
    def _add_weight48(cls,id,weight):
        if redisWeightB.exists(cls._LOGIN_ENTRY_KEY%id):
            _old_weight=int(redisWeightB.zscore(cls._WEIGHT_B_KEY,id)[:1])
            _new_value=(_old_weight+weight)*10**11+time()
            redisWeightB.zincrby(cls._WEIGHT_B_KEY,_new_value,id)
            redisWeightB.set(cls._LOGIN_ENTRY_KEY%id,time())

    @classmethod
    def exists24(cls,id):
        return redis.get(cls._ENTRY_KEY%id)

    @classmethod
    def add(cls,uid,id):
        redis.setex(cls._ENTRY_KEY%id,86400,time())
        #redis.zadd(cls._ENTRY_KEY%uid,time(),id)

    @classmethod
    def touch(cls,id):
        redis.set(cls._ENTRY_KEY%id,time())

    @classmethod
    def favor(cls,id):
        '''喜欢过的'''
        if cls.exists24(id):
            cls._add_weight(id,1)
        else:
            cls._add_weight48(id,1)

    @classmethod
    def comment(cls,id):
        '''评论过的'''
        if cls.exists24(id):
            uid=EntryModel.uid_by_eid(id)
            weight=1
            if UserModel.has_pet(uid):
                weight=1.5
            cls._add_weight(id,weight)
        else:
            cls._add_weight48(id,2)

    @classmethod
    def _time_line_a(cls):
        #withscores=True
        _entry_kvs=dict(redis.zrangebyscore(cls._WEIGHT_A_KEY,0,"+inf",start=0,num=100,withscores=True))
        if len(_entry_kvs)<1:
            return []
        _entry_ks=map(lambda eid:cls._ENTRY_KEY%eid,_entry_kvs.keys())
        _entry_time=redis.mget(_entry_ks)
        weightA=[]
        for i,k in enumerate(_entry_kvs.keys()):
            weightA.append([k,_entry_kvs[k],_entry_time[i]])
        return weightA
    
    @classmethod
    def _time_line_b(cls,size=15):
        min_score=2*10**11+time()-3600*24
        _entry_kvs=redisWeightB.zrangebyscore(cls._WEIGHT_B_KEY,min_score,"+inf",withscores=True)
        if len(_entry_kvs)<1:
            return []
        weightB=set() 
        for i in range(size):
            eid,value=random.choice(_entry_kvs)
            _entry_kvs.remove((eid,value))
            weight,t=value[:1],value[1:]
            _weightB.add([eid,weight,t])

        return list(weightB)

    @classmethod
    @cache(300)
    def time_line(cls):
        weightA=cls._time_line_a()
        weightB=cls._time_line_b()
        weight=weightA+weightB
        return sorted(weight,key=itemgetter(2))

class User:
    @classmethod
    def login(self,uid):
        entries=UserEntry.entries_by_uid_createtime(uid,time()-86400)#  
        for e in entries:
            redisWeightB.setex(Entry._LOGIN_ENTRY_KEY%id,17200,0)
            redisWeightB.zadd(Entry._WEIGHT_B_KEY,time(),id)

def main():
    pass

if __name__=='__main__':
    print Entry.time_line()
