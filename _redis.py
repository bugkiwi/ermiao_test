#!/usr/bin/env python
#coding:utf-8
from redis import StrictRedis
redis=StrictRedis(db=1)
redisWeightB=StrictRedis(db=2)

def _flushdb():
    redis.flushdb()
    redisWeightB.flushdb()
