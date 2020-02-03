#!/usr/bin/python3
# -*- coding: UTF-8 -*-
#分页抓取视频url
import json
from multiprocessing import Pool,Process
import time
import pymongo
import sys
import re
sys.path.append('..')
from commone.videoDemo import videoDemo 
from commone.Dbobj import Dbobj 

def getList(obj,num):
    dbObj = Dbobj('redio','re_')
    arr = [];
    curTableObj = dbObj.getTbname('stars')
    url = "https://www.123fanhao.com/special-show-p-"+str(num)+".html"
    content = obj.mainContent(url)
    if content is None:
        return False 
    pattern = '<div class="col-xs-6 col-sm-2 placeholder">([.|\s|\S|\n]*?)<a href="([.|\s|\S|\n]*?)" target="_blank"><img src="([.|\s|\S|\n]*?)" title="([.|\s|\S|\n]*?)" class="img-thumbnail"></a><h4><a href="([.|\s|\S|\n]*?)" target="_blank">([.|\s|\S|\n]*?)</a>([.|\s|\S|\n]*?)</div>'
    listCates = re.findall(pattern,content) 
    if listCates is None:
        return False  
    #baseUrl = 'https://www.123fanhao.com'
    data = []
    for v in listCates:
        if len(v) < 1:
            continue
        curDict = {}    
        curDict['_id'] = dbObj.getNextValue('stars')
        curDict['ename'] = v[3].split('/')[1].strip()
        curDict['rel'] = v[1]
        curDict['img'] = v[2]
        curDict['cname']= v[5].strip()
        curDict['status']= 0
        data.append(curDict)
    curTableObj.insert_many(data);
def runList():
    getObj = videoDemo();
    pageList = list(range(1,1106))
    for i in pageList:
        getList(getObj,i)       
if __name__=='__main__':
    #runList()
    
    # pageCount = len(pageList)
    # p = Pool(pageCount)
    # for i in pageList:
    #     p.apply_async(deRange, args=(i,))
    # p.close()
    # p.join()
