#!/usr/bin/env python
#coding:utf-8
from functools import wraps 
import time
import hashlib
import pickle

_caches={}

def is_expire(cache_entry,duration):
    return time.time()-cache_entry['time']<duration

def complex_func(func,args,kargs):
    key = pickle.dumps((func.func_name,args,kargs))
    return hashlib.sha1(key).hexdigest()

def cache(duration=300): 
    '''默认缓存5分钟
    '''
    def wrap(func):
        @wraps(func)
        def _(*args,**kargs):
            key=complex_func(func,args,kargs)
            if key in _caches and is_expire(_caches[key],duration):
                return _cache[key]['value']
            _caches[key] = {'time':time.time(),'value':func(*args,**kargs)}
            return _caches[key]['value']
        return _
    return wrap
