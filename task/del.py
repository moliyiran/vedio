#!/usr/bin/python3
# -*- coding: UTF-8 -*-
#视频详情抓取
import json
from multiprocessing import Pool,Process
import time
import pymongo
import sys
import math
sys.path.append('..')
from commone.GoogleTranslator import GoogleTranslator
from commone.videoDemo import videoDemo 
from commone.Dbobj import Dbobj     

def getDetail():
    getObj = videoDemo();
    dbObj = Dbobj('redio','re_')
    arr = [];
    # if type == 0:
    #    _sort = pymongo.DESCENDING
    # else:
    #    _sort = pymongo.ASCENDING  
    curTableObj = dbObj.getTbname('ads')
    #data = curTableObj.aggregate([{"status":0},{"$sample":{"size":1}}])
    data = curTableObj.aggregate([
    	{"$match":{'status':0,'device':2,'type':1}},#,"path":"$path","url":"$url","device":"$device","type":"$type","status":"$status", 
    	{"$group": {"_id":"$_id","count": {"$sum": 1},"data":{"$push":{"url":"$url","status":"$status","_id":"$_id",'device':"$device",'type':"$type"}}}},
		{"$sample":{"size":1}},
		#{"$project":{"path":1,"url":1,"device":1,"type":1,"status":1}},
		{"$sort":{"_id":-1}}
	])
    newData = {}
    for i in data:
    	newData = i.get('data')[0]
    print(newData)
    print(newData.get('url'))
if __name__=='__main__':
	for i in range(1,3):
		print(i)
    #getDetail();