#!/usr/bin/python3
# -*- coding: UTF-8 -*-
#视频详情抓取
import json
from multiprocessing import Pool,Process
import time
import pymongo
import re
import sys
sys.path.append('..')
from commone.GoogleTranslator import GoogleTranslator
from commone.videoDemo import videoDemo 
from commone.Dbobj import Dbobj 
def starDir(_id):
    path = "./stars/"+str(_id)+".jpg"
    return path
def getDetail():
    getObj = videoDemo();
    dbObj = Dbobj('redio','re_')
    arr = [];
    # if type == 0:
    #    _sort = pymongo.DESCENDING
    # else:
    #    _sort = pymongo.ASCENDING  
    curTableObj = dbObj.getTbname('local_stars')
    base = 'https://www.qq.com/'
    while True:
       data = curTableObj.find({"imgs":{"$exists":False}}).sort('_id', pymongo.DESCENDING).limit(10)

       if data is None:
          sleep(10);
          continue;
       for v in data:
          _curUpData = {}
          _rel = v.get('rel',0)
          curUrl = base+_rel.strip('/')+'#_tabAboutMe'  
          content = getObj.mainContent(curUrl) 
          if content is None:
             continue
          #print(content.encode('gbk', 'ignore').decode('gbk'))
          pattern = '<div class="profile-pic">([.|\s|\S|\n]*?)<img src="(.*)" onerror=([.|\s|\S|\n]*?)</div>' 
          listCates = re.findall(pattern,content)
          if listCates is None:
             break
          img = listCates[1]
          #print(img[1]);exit('5')
          #print(content.encode('gbk', 'ignore').decode('gbk'));exit(3)
          file = starDir(v['_id'])
          getObj.getOtherSource(file,img[1])
          _curUpData['imgs'] = ''
          data = curTableObj.update({"_id":v['_id']},{"$set":_curUpData})
       time.sleep(0.5)   
if __name__=='__main__':
    getDetail();