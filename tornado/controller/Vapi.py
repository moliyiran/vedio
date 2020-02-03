#!/usr/bin/python
# -*- coding: UTF-8 -*-
import tornado.ioloop
import tornado.web
# import sys
# sys.path.append('D:\\wwwroot\\py\\tornado')
#from videoDemo import videoDemo 
#from Dbobj import Dbobj 
import math
import pymongo
import re
import hashlib
import json
from urllib.parse import urlparse
#import sys
#sys.path.append('....commone')
import os
os.sys.path.append(os.path.join( os.path.dirname(__file__), '../..'))
from commone.Credis import Credis
from commone.Dbobj import Dbobj
from commone.videoDemo import videoDemo

class Vapi(tornado.web.RequestHandler):
    _k = '12345,.Abc33678'
    _dbobj = ''
    def post(self):
      #try:
        
        head = self.request.headers
        nonce = head.get('nonce',None)
        token = head.get('token',None)

        if(nonce == None or token == None):
           self.finish({'status':1})
           return
        isValid = self.checkPost(nonce,token)
        if isValid == False:
           self.finish({'status':1})
           return
   
        ads =  self.get_argument('ads',0)
        if ads == 0:
           self.finish({'status':1})
           return
        _type =  self.get_argument('type',1)           
        _device =   self.get_argument('device',1) 
        #title =   self.get_argument('title',1)  
        allData = []
        curData = []
        curData = json.loads(ads)
        curTableObj = self.__dbInfo('ads')
        for i in curData:
           i['_id'] = self._dbobj.getNextValue('ads')
           i['type'] = int(_type)
           i['device'] = int(_device)
           i['status'] = 0
           #i['title'] = title
           allData.append(i)    
        re = curTableObj.insert_many(allData)
        if re: 
         self.finish({'status':0})
        else:
         self.finish({'status':1})  
    def __dbInfo(self, tableName):
        getObj = videoDemo();
        self._dbobj = dbObj = Dbobj('redio','re_')
        return dbObj.getTbname(tableName)
    def checkPost(self,nonce,token):
        #return True
        nonce = str(nonce).strip()
        _str = str(nonce)+"..,"+self._k
        m = hashlib.md5()
        b = _str.encode(encoding='utf-8')
        m.update(b)
        str_md5 = m.hexdigest()
        print(str_md5)
        re = False
        if str_md5 == token:
           re = True
        else:
           re = False   
        
        return re    



        
                
