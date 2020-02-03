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
        trndsList = curTableObj.find({"_id":{"$gt":0}}).sort('_id', pymongo.DESCENDING)
        if trndsList is None:
            return False
        for v in trndsList:
           yield v   

    def getLocalStarDetail(self, rel):
        i = 0
        while i<100:
            baseUrl = self.base+rel['rel'] 
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
    def getListNew(self,v):
        url ="https://www.qq.com"+v['rel']
        country = v['country']     
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
        for v in listCates:
            curDict = {}
            curDict['_id'] = self.dbObj.getNextValue('local_stars')
            curDict['rel'] = '/profiles/'+v[0]
            curDict['cname'] = curDict['name'] = v[1].strip()
            curDict['country'] = country
            allData.append(curDict)

        table = self.dbObj.getTbname('local_stars')
        table.insert_many(allData)
    def getLocalStar(self):
        # curlObj = videoDemo()
        # dbObj = Dbobj('redio','re_')
        # #obj = getStarList(dbObj,curlObj)
        # #urls = ['https://www.qq.com/pornstars-index/japan','https://www.qq.com/pornstars-index/china','https://www.qq.com/pornstars-index/hong_kong']
        # i = 0
        # type = 0
        for v in self.getLocalCountryList():    
            self.getListNew(v)
    def getLocalCountryList(self):
        curTableObj = self.dbObj.getTbname('stars_country')
        trndsList = curTableObj.find({"_id":{"$gt":0}}) #.sort('_id', pymongo.DESCENDING)
        if trndsList is None:
            return False
        for v in trndsList:
           if v['country'] not in ('Japan','China','Hong Kong'):
              yield v          
    def getStarlink(self):
        url = "https://www.qq.com/pornstars-index/countries";  
        content = self.curlObj.mainContent(url)
        #newCurTable = self.dbObj.getTbname('stars')
        if content is None:
            return False
        pattern = '<ul class="tags-list">([.|\s|\S|\n]*?)</ul>'
        listCates = re.findall(pattern,content)
        #print(listCates);exit(3)
        if listCates is None:
            return False
        listCates = listCates[0]
        #print(listCates);exit('5')
        pattern = '<a href="([.|\s|\S|\n]*?)"><b><span([.|\s|\S|\n]*?)></span>([.|\s|\S|\n]*?)</b><span([.|\s|\S|\n]*?)>([.|\s|\S|\n]*?)</span></a>'
        listCates = re.findall(pattern,listCates)
        
        if listCates is None:
            return False
        countryList = []
        for v in listCates:
            curRel = v[0].strip()
            curCountry = v[2].strip()
            countryList.append({'rel':curRel,'country':curCountry,'_id':self.dbObj.getNextValue('stars_country')})
        table = self.dbObj.getTbname('stars_country')
        table.insert_many(countryList)
        
                

if __name__=='__main__':
    curlObj = videoDemo()
    dbObj = Dbobj('redio','re_')
    obj = getStarList(dbObj,curlObj)
    #obj.getStarlink();
    #obj.getLocalStar()
    obj.runStars()


