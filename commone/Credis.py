#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import redis
import json

class Credis:
    def __init__(self, dbname=1, prefix='re_', host='127.0.0.1', port='6379'):
       self.redisObj = redis.Redis(host=host,port=port,db=dbname)
       self.prefix = prefix
    def set(self,key,value,times=0,type=0):
        if type == 0:
           value = json.dumps(value)

        self.redisObj.set(self.getKey(key), value)
        if times > 0:
          self.redisObj.expire(self.getKey(key),times)
    def getKey(self,key):
        return self.prefix+key;    
    def get(self,key,type=0):
        value = self.redisObj.get(self.getKey(key))
        if type==0 and value != None:
               value = json.loads(value)
        return value 

