#!/usr/bin/python3
# -*- coding: UTF-8 -*-
#分页抓取视频url
import json
from multiprocessing import Pool,Process
import time
import pymongo
import sys
sys.path.append('..')
from commone.GoogleTranslator import GoogleTranslator
from commone.videoDemo import videoDemo 
from commone.Dbobj import Dbobj 

def deRange(num):
    getObj = videoDemo();
    dbObj = Dbobj('redio','re_')
    arr = [];
    curTableObj = dbObj.getTbname('redios')
    if num < 1:
        url="https://www.qq.com/"
    else:    
        url="https://www.qq.com/new/"+str(num);

    for v in getObj.getVedioUrl(url):
        if v['id']!='':
           v['_id'] = dbObj.getNextValue('redios')
           v['tags']=v['cates']=''
           v['status']=0
           curTableObj.update({"id":v['id'].strip()},{"$setOnInsert":v}, upsert=True);   
if __name__=='__main__':
    pageList = list(range(0,10))
    for i in pageList:
        deRange(i)

    # pageCount = len(pageList)
    # p = Pool(pageCount)
    # for i in pageList:
    #     p.apply_async(deRange, args=(i,))
    # p.close()
    # p.join()
