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
class getStarList:
    base ="https://www.qq.com"
    def __init__(self,obj,curlObj):
        self.dbObj = obj
        self.curlObj = curlObj
    def getLocalStarList(self):
        curTableObj = self.dbObj.getTbname('local_stars')
        trndsList = curTableObj.find({"_id":45}) #.sort('_id', pymongo.DESCENDING)
        if trndsList is None:
            return False
        for v in trndsList:
           yield v   

    def getLocalStarDetail(self, rel):
        i = 0
        while i<100:
            baseUrl = self.base+rel['rel'] 
            #print(baseUrl);exit(5)
            if i > 0:
               baseUrl = baseUrl+'#'+str(i)
            baseUrl = baseUrl+'/videos/best'       
            content = self.curlObj.mainContent(baseUrl)
            if content is None:
                break 
            #print(content);exit('5')                
            pattern = '<div id="video_([.|\s|\S|\n]*?)" data-id="([.|\s|\S|\n]*?)" class="thumb-block([.|\s|\S|\n]*?)"><p class="title"><a href="([.|\s|\S|\n]*?)" title="([.|\s|\S|\n]*?)">([.|\s|\S|\n]*?)</a></p>([.|\s|\S|\n]*?)</div>'
            listCates = re.findall(pattern,content)
            if listCates is None:
                continue
            for v in listCates:
                #print(v[1],v[3],v[5]);exit('7')
                if v[1] is not None:
                    curData = {
                        'id':v[1],
                        'title':v[5],
                        'stars_id':rel['_id'],
                        'url':v[3]
                    }
                    self.addStarMovie(curData) 
            del listCates
            del content
            if i%10:
                time.sleep(0.5)
            i +=1
    def addStarMovie(self, data):
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
                "stars":[data['stars_id']],
                "rel":data['url'],
                "url":data['url']
            }
            curTableObj.insert(curDict);
        else:
            newTrends = []
            trends = info.get('stars', 0)
            if trends == 0:
                newTrends.append(data['stars_id'])
                curTableObj.update({"_id":info['_id']},{"$set":{"stars":newTrends}})
            elif data['stars_id'] not in trends and str(data['stars_id']) not in trends:
                trends.append(data['stars_id'])
                curTableObj.update({"_id":info['_id']},{"$set":{"stars":trends}})     
    def runStars(self):
        threadObj = []
        for v in self.getLocalStarList():
            vinfo = self.getLocalStarDetail(v)
    def getList(self,url,type=0):     
        content = self.curlObj.mainContent(url)
        newCurTable = self.dbObj.getTbname('stars')
        if content is None:
            return False
        pattern = '<p class="title"><a href="([.|\s|\S|\n]*?)" title="([.|\s|\S|\n]*?)">([.|\s|\S|\n]*?)</a></p>'
        pattern = '<a href="/profiles/([.|\s|\S|\n]*?)">([.|\s|\S|\n]*?)</a>'
        listCates = re.findall(pattern,content)
        #print(listCates);exit(3)
        if listCates is None:
            return False
        allData = []
        if url == 'https://www.qq.com/pornstars-index/japan':
            type = 1
        #print(type)        
        for v in listCates:
            curDict = {}
            curDict['_id'] = self.dbObj.getNextValue('local_stars')
            curDict['rel'] = '/profiles/'+v[0]
            curDict['cname'] = curDict['name'] = v[1].strip()
            if type == 1: #日本
                name = curDict['name']

                curInfo = newCurTable.find_one({"ename":name})
                #print(curInfo);exit('5')
                if curInfo is not None:
                    cname = curInfo.get('cname',0)
                    if cname != 0:
                        curDict['cname'] = cname
            allData.append(curDict)

        table = self.dbObj.getTbname('local_stars')
        table.insert_many(allData)
    def getLocalStar(self,obj):
        curlObj = videoDemo()
        dbObj = Dbobj('redio','re_')
        #obj = getStarList(dbObj,curlObj)
        urls = ['https://www.qq.com/pornstars-index/japan','https://www.qq.com/pornstars-index/china','https://www.qq.com/pornstars-index/hong_kong']
        i = 0
        for url in urls:
            if i == 0:
                type = 1
            else:
                type = 0
            i += 1     
            obj.getList(url,type)        


if __name__=='__main__':
    curlObj = videoDemo()
    dbObj = Dbobj('redio','re_')
    obj = getStarList(dbObj,curlObj)
    obj.runStars()
    # p = Pool(2)
    # p.apply_async(obj.runTreands(), args=())
    # p.apply_async(obj.runCates, args=())
    # p.close()
    # p.join() 


