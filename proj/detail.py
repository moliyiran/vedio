#!/usr/bin/python3
# -*- coding: UTF-8 -*-
#分页抓取视频url
from videoDemo import videoDemo 
from Dbobj import Dbobj 
import json
from multiprocessing import Pool,Process
import time
import pymongo
import sys
sys.path.append('..')
from commone.GoogleTranslator import GoogleTranslator

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
       #_count = len(data)
       #pool = Pool(_count)
       if data is None:
          break;
       g = GoogleTranslator()
       for v in data:
           curUrl = base+v['rel'].strip('/')   
           #curTableObj.run(curUrl,i['id'])
           #curUrl='https://www.qq.com/video13860839/502_-_horny_asian_couple_had_sex_on_bed'
           tags = getObj.vdetail(curUrl,v['id'])

           v['title']=v['title'].replace('&#039','').replace('&amp;','')

           s=g.translate(v['title'])
           _curUpData = {}
           if s == '':
                _curUpData['status'] = 3
           else:
                _curUpData['status'] = 1
                _curUpData['ctitle'] = s           
           if tags != False:
                _curUpData['tags'] = tags
           data = curTableObj.update({"id":v['id']},{"$set":_curUpData})
       time.sleep(0.5)        
if __name__=='__main__':
    #70000-100000
    p = Pool(12) 
    _start = 70000
    for i in range(3):
        start = _start + i*10000
        end = start + 10000
        p.apply_async(poolDetail, args=(start,end))
    # p.close()
    # p.join()
    # #100000-600000
    # p = Pool(5) 
    _start = 100000
    for i in range(5):
        start = _start + i*100000
        end = start + 100000
        p.apply_async(poolDetail, args=(start,end))
    # p.close()
    # p.join()
    # #80-100
    # p = Pool(4)
    p.apply_async(poolDetail, args=(800000,1000000)) 
    p.apply_async(poolDetail, args=(1000000,2000000)) 
    p.apply_async(poolDetail, args=(2000000,2100000)) 
    p.apply_async(poolDetail, args=(2100000,3000000)) 
    p.close()
    p.join()

    print('All subprocesses done.')

    #    p.apply_async(curTableObj.vdetail, args=(curUrl,v['id']))
    # p.close()
    # p.join()
    # print('All subprocesses done.')