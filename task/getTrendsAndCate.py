#coding=utf-8
from bs4 import BeautifulSoup 
#from selenium import webdriver
import sys
sys.path.append('..')
from commone.Dbobj import Dbobj 
import re
import threading
import time
from commone.videoDemo import videoDemo 
import pymongo
from multiprocessing import Pool
class getTrendsAndCate:
    base ="https://www.qq.com"
    def __init__(self,obj,curlObj):
        self.dbObj = obj
        self.curlObj = curlObj
    def getTrendsList(self):
        curTableObj = self.dbObj.getTbname('trends')
        trndsList = curTableObj.find({"_id":{"$gt":0}}) #.sort('_id', pymongo.DESCENDING)
        if trndsList is None:
            return False
        for v in trndsList:
            yield v

    def addTrends(self, data):
        curTableObj = self.dbObj.getTbname('redios')
        info = curTableObj.find_one({"id":str(data['id'])})
        #print(info);exit(556)
        if info is None:
            curDict = {
                "_id":self.dbObj.getNextValue('redios'),
                "id":data['id'],
                "title":data['title'],
                "status":0,
                "like_times":0,
                "view_times":0,
                "trends":[data['trends_id']],
                "url":data['url']

            }
            #print(curDict);exit('5')
            curTableObj.insert(curDict);
        else:
            #print(info);exit('5')
            newTrends = []
            trends = info.get('trends', 0)
            if trends == 0:
                newTrends.append(data['trends_id'])
                curTableObj.update({"_id":info['_id']},{"$set":{"trends":newTrends}})
            elif data['trends_id'] not in trends and str(data['trends_id']) not in trends:
                trends.append(data['trends_id'])
                curTableObj.update({"_id":info['_id']},{"$set":{"trends":trends}})
                    

            

    def getTrendsDetail(self, rel):
        i = 0
        while i<100:
            baseUrl = self.base+rel['url'].replace('&trend=CN','') 
            if i > 0:
               baseUrl = baseUrl+'&p='+str(i)       
            content = self.curlObj.mainContent(baseUrl)
            if content is None:
                break
            pattern = '<p class="title"><a href="([.|\s|\S|\n]*?)" title="([.|\s|\S|\n]*?)">([.|\s|\S|\n]*?)</a></p>'
            listCates = re.findall(pattern,content)
 
            if listCates is None:
                continue
            for v in listCates:
                if v[0] is not None:
                    c_pattern = 'video(\d*)/(.*)'
                    _id = re.findall(c_pattern,v[0])
                    curData = {
                        'id':_id[0][0],
                        'title':v[2],
                        'trends_id':rel['_id'],
                        'url':v[0]
                    }
                    self.addTrends(curData) 
            del listCates
            del content
            if i%10:
                time.sleep(0.5)
            i +=1 
    def getCateList(self):
        curTableObj = self.dbObj.getTbname('category')
        cateList = curTableObj.find({"_id":{"$gt":0}}) #.sort('_id', pymongo.DESCENDING)
        if cateList is None:
            return False
        for v in cateList:
            #print(v);exit(0)
            yield v
    def addCates(self, data):
        curTableObj = self.dbObj.getTbname('redios')
        info = curTableObj.find_one({"id":str(data['id'])})
        #print(info);exit(556)
        if info is None:
            curDict = {
                "_id":self.dbObj.getNextValue('redios'),
                "id":data['id'],
                "title":data['title'],
                "status":0,
                "like_times":0,
                "view_times":0,
                "category":[data['cates_id']],
                "url":data['url']

            }
            #print(curDict);exit('5')
            curTableObj.insert(curDict);
        else:
            newTrends = []
            trends = info.get('category', 0)
            if trends == 0:
                newTrends.append(data['cates_id'])
                curTableObj.update({"_id":info['_id']},{"$set":{"category":newTrends}})
            elif data['cates_id'] not in trends and str(data['cates_id']) not in trends:
                trends.append(data['cates_id'])
                curTableObj.update({"_id":info['_id']},{"$set":{"category":trends}})
                    

            

    def getCateDetail(self, rel):
        i = 0
        while i<100:
            baseUrl = self.base+rel['url'] 
            if i > 0:
               baseUrl = baseUrl+'/'+str(i)       
            content = self.curlObj.mainContent(baseUrl)
            if content is None:
                break
            pattern = '<p class="title"><a href="([.|\s|\S|\n]*?)" title="([.|\s|\S|\n]*?)">([.|\s|\S|\n]*?)</a></p>'
            listCates = re.findall(pattern,content)
            #print(listCates);exit(3)
            if listCates is None:
                continue
            for v in listCates:
                if v[0] is not None:
                    c_pattern = 'video(\d*)/(.*)'
                    _id = re.findall(c_pattern,v[0])
                    curData = {
                        'id':_id[0][0],
                        'title':v[2],
                        'cates_id':rel['_id'],
                        'url':v[0]
                    }
                    self.addCates(curData) 
            del listCates
            del content
            if i%10:
                time.sleep(0.5)
            i +=1     
    def runTreands(self):
        threadObj = []
        for v in self.getTrendsList():
            vinfo = self.getTrendsDetail(v)
    def runCates(self):
        threadObj = []
        for v in self.getCateList():
            vinfo = self.getCateDetail(v)


if __name__=='__main__':
    curlObj = videoDemo()
    dbObj = Dbobj('redio','re_')
    obj = getTrendsAndCate(dbObj,curlObj)
    p = Pool(2)
    p.apply_async(obj.runTreands(), args=())
    p.apply_async(obj.runCates, args=())
    p.close()
    p.join() 


