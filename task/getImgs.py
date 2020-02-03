#!/usr/bin/python3
# -*- coding: UTF-8 -*-
#视频详情抓取
import json
from multiprocessing import Pool,Process
import time
import pymongo
import sys
sys.path.append('..')
from commone.GoogleTranslator import GoogleTranslator
from commone.videoDemo import videoDemo 
from commone.Dbobj import Dbobj 

def poolDetail(start,end):
    getObj = videoDemo();
    dbObj = Dbobj('redio','re_')
    arr = [];
    # if type == 0:
    #    _sort = pymongo.DESCENDING
    # else:
    #    _sort = pymongo.ASCENDING  
    curTableObj = dbObj.getTbname('redios')
    base = 'https://www.qq.com/'
    while True:
       data = curTableObj.find({"status":0,"_id":{"$gte":start,"$lt":end}}).sort('_id', pymongo.DESCENDING).limit(10)

       if data is None:
          break;
       #g = GoogleTranslator()
       for v in data:
           _rel = v.get('rel',0)
           if _rel == 0:
              _rel = v.get('url')
           curUrl = base+_rel.strip('/')  
           #curUrl = base+v['rel'].strip('/')   
           #curTableObj.run(curUrl,i['id'])
           #curUrl='https://www.qq.com/video13860839/502_-_horny_asian_couple_had_sex_on_bed'
           tags = getObj.vdetail(curUrl,v['id'])

           v['title']=v['title'].replace('&#039','').replace('&amp;','')

           #s=g.translate(v['title'])
           _curUpData = {}
           # if s == '':
           #      _curUpData['status'] = 3
           # else:
           #      _curUpData['status'] = 1
                #_curUpData['ctitle'] = s           
           _curUpData['status'] = 1     
           if tags != False:
                _curUpData['tags'] = tags
           data = curTableObj.update({"id":v['id']},{"$set":_curUpData})
       time.sleep(0.5)     

def getDetail():
    getObj = videoDemo();
    dbObj = Dbobj('redio','re_')
    arr = [];
    # if type == 0:
    #    _sort = pymongo.DESCENDING
    # else:
    #    _sort = pymongo.ASCENDING  
    curTableObj = dbObj.getTbname('redios')
    base = 'https://www.qq.com/'
    while True:
       data = curTableObj.find({"imgs":{"$exists":False}}).sort('_id', pymongo.DESCENDING).limit(10)

       if data is None:
          sleep(10);
          continue;
       for v in data:
           _curUpData = {}
           _rel = v.get('rel',0)
           if _rel == 0:
              _rel = v.get('url')
           curUrl = base+_rel.strip('/')   
           tags = getObj.vdetail(curUrl,v['id']);
           _curUpData['imgs'] = ''
           data = curTableObj.update({"id":v['id']},{"$set":_curUpData})
       time.sleep(0.5)   

if __name__=='__main__':
    getDetail();
    #70000-100000
    # p = Pool(19) 
    # _start = 0
    # for i in range(10):
    #     start = _start + i*10000
    #     end = start + 10000
    #     p.apply_async(poolDetail, args=(start,end))

    # _start = 100000
    # for i in range(5):
    #     start = _start + i*100000
    #     end = start + 100000
    #     p.apply_async(poolDetail, args=(start,end))

    # p.apply_async(poolDetail, args=(800000,1000000)) 
    # p.apply_async(poolDetail, args=(1000000,2000000)) 
    # p.apply_async(poolDetail, args=(2000000,2100000)) 
    # p.apply_async(poolDetail, args=(2100000,3000000)) 
    # p.close()
    # p.join()

    # print('All subprocesses done.')

    #    p.apply_async(curTableObj.vdetail, args=(curUrl,v['id']))
    # p.close()
    # p.join()
    # print('All subprocesses done.')