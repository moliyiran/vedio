#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import re
import requests
import os
import threading
import random
from multiprocessing import Pool,Process
import datetime
import json
from googletrans import Translator
import os
from Dbobj import Dbobj 

class videoDemo:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"}
    baseUrl = ''
    def __init__(self):
        self.dbObj = Dbobj('redio','re_')
    def failedLog(self,content):
        curTableObj = dbObj.getTbname('failedLog')
        curTableObj.insert(content)
        # t_time = datetime.datetime.now().strftime('%Y-%m-%d')
        # log = "./log/"+t_time+'.txt'
        # time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'\n'+self.baseUrl+'\n'+content
        # self.write_to_file(log,content)
    def ackGet(self,url, type, proxy=None):
        try:
            if proxy != None:
                response = requests.get(url, headers = self.headers)# 打开一个文件        # 进行状态码判断，是否正确读取到网页
            else:        
                proxy = self.getProxy()  
                response = requests.get(url, headers = self.headers, proxies=proxy)

            if response.status_code == 200:
                return response.content if type == 1 else response.text 
        except Exception as eo :
            return False
        # response = requests.get(url, headers = self.headers)

        # if response.status_code == 200:
        #     return response.content if type == 1 else response.text 
    def mainContent(self, url, type=0,proxy=None):
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"}
        result = self.ackGet(url,type)
        if result != False:
            return result
        i = 5
        while i:
            if result == False:
                result = self.ackGet(url,type)
            else:
                return result
            i -=1;
        result = self.ackGet(url,type,1);
        if result == False:
           return None
           #self.failedLog(url) 
        else:
            return result        
        return None
        # except RequestException:
        #     return None
        #print(re.match(r'html5player\.(.*);', r))
    # 解析网页
    def parse_one_page(self,html):
        patternDict = {'setVideoUrlLow': "html5player.setVideoUrlLow\('(.*?)'\)",'setVideoUrlHigh':"html5player.setVideoUrlHigh\('(.*?)'\)",'setVideoHLS':"html5player.setVideoHLS\('(.*?)'\)",'setThumbUrl':"html5player.setThumbUrl\('(.*?)'\)",'setThumbUrl169':"html5player.setThumbUrl169\('(.*?)'\)",'setVideoURL':"html5player.setVideoURL\('(.*?)'\)",'setStaticDomain':"html5player.setStaticDomain\('(.*?)'\)",'setVideoTitle':"html5player.setVideoTitle\('(.*?)'\)"}
        newDict = {}
        for k,v in patternDict.items():
           gtems = re.findall(v,html)
           if gtems != None:
                newDict[k] = gtems
        return newDict
    # 将抓取的内容保存到文件
    def write_to_file(self,file,content,mode='a'):
       if mode == 'a':        
           with open(file,mode, encoding='utf-8') as f:
                f.write(content)
                f.close()
       else:        
           with open(file,mode) as f:
                f.write(content)
                f.close()
    def getOtherSource(self,file,url,sourceType='img'):
        content = self.mainContent(url,1)
        if content!=None:
            self.write_to_file(file,content,'wb')
        #检查是否抓取成功    
        if os.path.exists(file) == False:
            failedLog({"file":file,"url":url})
    #抓取图片
    def imgFunc(self, path,dict):
        checkSource = otherSource = []
        for k,v in dict.items():
            #if k == 'setThumbUrl' and v.strip() != '':
            if k == 'setThumbUrl' and len(v)>0:
                tmpName = path+'/'+k+'.jpg';
                #checkSource.append({"tmpName":tmpName,"url":v[0]})
                self.getOtherSource(tmpName,v[0])
                # tmp_k = threading.Thread(target=self.getOtherSource, name='img_tsThread'+k, args=(tmpName,v[0]))
                # otherSource.append(tmp_k)
            if k == 'setThumbUrl169' and len(v)>0:
                tmpName = path+'/'+k+'.jpg';
                self.getOtherSource(tmpName,v[0])
                # checkSource.append({"tmpName":tmpName,"url":v[0]})
                # tmp_k = threading.Thread(target=self.getOtherSource, name='img_tsThread'+k, args=(tmpName,v[0]))
                # otherSource.append(tmp_k)
        # for i in otherSource:
        #     i.start()
        # for i in otherSource:
        #     i.join()

    def vdetail(self,videoUrl,videoNo):
        self.baseUrl = videoUrl
        # path = "./source/"+videoNo
        # if os.path.isdir(path) == False:
        #     os.makedirs( path, 755 );
        
        htmlContent = self.mainContent(videoUrl)
        if htmlContent == None:
            return False
        dict = self.parse_one_page(htmlContent)
        if(len(dict)<0):
            return False
        tags = []
        pattern = '<div class="video-metadata video-tags-list ordered-label-list cropped">([.|\s|\S|\n]*?)</div>'
        tags = re.findall(pattern,htmlContent)
        if(len(tags)<0):
            return False   
        tags = tags[0]
        #print(tags)
        pattern = '<a href="/tags/([.|\s|\S|\n]*?)" class="btn btn-default">([.|\s|\S|\n]*?)</a>'
        tags = re.findall(pattern,tags)
        if(len(tags)<0):
            return False
        reTags = []
        for i in tags:
            if len(i[1])>0:
             reTags.append(i[1].strip())
        #self.imgFunc(path,dict) 
        return reTags
        #开始多进程抓取数据
        # _pools = []
        # _pools.append(Process(target=self.imgFunc, args=(path,dict)))
        # checkDict = {}           
        # for k,v in dict.items():
        #     # print(k)
        #     # print(v,len(v))
        #     if len(v)>0:                
        #         checkDict[k] = v[0] 
        #     if k == 'setVideoUrlHigh' and len(v) > 0:
        #         tmpName = path+'/'+k+'.mp4'
        #         _pools.append(Process(target=self.getOtherSource, args=(tmpName, v[0])))
        #     if k == 'setVideoUrlLow' and len(v) > 0:
        #         tmpName = path+'/'+k+'.mp4'
        #         _pools.append(Process(target=self.getOtherSource, args=(tmpName, v[0]))) 
        #     if k == 'setVideoHLS' and len(v) > 0:
        #         _pools.append(Process(target=self.poolTs, args=(v[0],videoNo)))
        # for i in _pools:
        #     i.start();
        # for i in _pools:
        #     i.join();
    def run(self,videoUrl,videoNo):
        self.baseUrl = videoUrl
        path = "./source/"+videoNo
        if os.path.isdir(path) == False:
            os.makedirs( path, 755 );
        
        htmlContent = self.mainContent(videoUrl)
        if htmlContent == None:
            return False
        dict = self.parse_one_page(htmlContent)
        if(len(dict)<0):
            return False
        #开始多进程抓取数据
        _pools = []
        _pools.append(Process(target=self.imgFunc, args=(path,dict)))
        checkDict = {}           
        for k,v in dict.items():
            # print(k)
            # print(v,len(v))
            if len(v)>0:                
                checkDict[k] = v[0] 
            if k == 'setVideoUrlHigh' and len(v) > 0:
                tmpName = path+'/'+k+'.mp4'
                _pools.append(Process(target=self.getOtherSource, args=(tmpName, v[0])))
            if k == 'setVideoUrlLow' and len(v) > 0:
                tmpName = path+'/'+k+'.mp4'
                _pools.append(Process(target=self.getOtherSource, args=(tmpName, v[0]))) 
            if k == 'setVideoHLS' and len(v) > 0:
                _pools.append(Process(target=self.poolTs, args=(v[0],videoNo)))
        for i in _pools:
            i.start();
        for i in _pools:
            i.join();

        #开始记录

        # p = Pool(1)
        # #图片单独提出来
        # p.apply_async(self.imgFunc, args=(path,dict))           
        # for k,v in dict.items():
        #     # print(k)
        #     # print(v,len(v))
        #     if k == 'setVideoUrlHigh' and len(v) > 0:
        #         tmpName = path+'/'+k+'.mp4'
        #         p.apply_async(self.getOtherSource, args=(tmpName, v[0]))
        #     if k == 'setVideoUrlLow' and len(v) > 0:
        #         tmpName = path+'/'+k+'.mp4'
        #         p.apply_async(self.getOtherSource, args=(tmpName, v[0]))
        #     if k == 'setVideoHLS' and len(v) > 0:
        #         p.apply_async(self.poolTs, args=(v[0],videoNo))
        # p.close()
        # p.join()
        return True
        #最后抓取文件
        # mp4List = ['setVideoUrlLow', 'setVideoUrlHigh']
        # jpgList = [ 'setThumbUrl', 'setThumbUrl169']
        # sp = ['setVideoHLS']
        # $imgSuffix = '.jpg'
        # $videoSuffix = ".mp4"
        # for k,v in dict.items():        # 第二个实例
        #     if v.strip()!='':
        #         if jpgList.index( k ):
        #             jpg = mainContent(v)
        #             if jpg !=None:
        #                 tmpFile = k.lower()+imgSuffix
        #                 write_to_file(tmpFile,jpg)
        #         elif mp4List.index( k ):
        #             jpg = mainContent(v)
        #             if mp4 !=None:
        #                 tmpFile = k.lower()+videoSuffix
        #                 write_to_file(tmpFile,mp4)
        #         elif sp.index( k ):
        #             sp = mainContent(v)
        #             if sp !=None:
        #                 tmpFile = k.lower()+videoSuffix
        #                 write_to_file(tmpFile,mp4)
    # def checkCompleteness(path,*dict):
    #     for k in dict:
    #         if k == 'setVideoUrlHigh' or k == 'setVideoUrlLow':
    #             tmpName = path+'/'+k+'.mp4'
    #             if os.path.exists(tmpName) == False:
    #         if k == 'setVideoUrlLow':
    #             tmpName = path+'/'+k+'.mp4'
    #             _pools.append(Process(target=self.getOtherSource, args=(tmpName, v[0]))) 
    #         if k == 'setVideoHLS' and len(v) > 0:
    #             _pools.append(Process(target=self.poolTs, args=(v[0],videoNo)))
             

    def poolTs(self,setVideoHLS,videoNo):
        hlsPath = setVideoHLS
        if hlsPath.strip() == '':
            return False
        baseUrl = self.sourceUrl(hlsPath)
        m3u8PathList = self.parseM3u8(hlsPath);
        if m3u8PathList == False:
            return False
        validPath = self.testValidPath(baseUrl,m3u8PathList);
#        print(validPath);exit(-3)
        if validPath == False:
            return False
        m3u8Path = baseUrl+validPath    
#        m3u8Path = m3u8Path.replace('hls.m3u8','hls-360p.m3u8')
        tsStatus = self.parseRealM3u8(baseUrl,m3u8Path,validPath,videoNo)
        return tsStatus                     
    def getTs(self,url,tsPrefix,index,videoNo):
            #print('thread %s start.' % threading.current_thread().name)
            tmpName = tsPrefix+index+".ts";
            #print(tmpName);exit(33)
            #proxy = self.getProxy()
            tmpTs =  self.mainContent(url+tmpName,1)
            _ordFile = './source/'+videoNo+'/'+tmpName
            if tmpTs !=None:
                self.write_to_file(_ordFile,tmpTs,'wb')
            #检查是否抓取成功    
            if os.path.exists(_ordFile) == False:
                failedLog({"file":_ordFile,"url":url})
            #print('thread %s ended.' % threading.current_thread().name)
    def parseRealM3u8(self,baseUrl,m3u8url,validPath,videoNo):
        content =  self.mainContent(m3u8url,0)
        if content == None:
            return False
        _ordFile = './source/'+videoNo+'/hls.m3u8'
        m3u8Name = res = re.sub('tsPrefix+"(\d*)\.ts"',r'\tsPrefix+"\1\.ts"',content)    
        tsPrefix = validPath.replace('.m3u8','')
        v = tsPrefix+"(\d*).ts";
        #curUrl = sourceUrl(m3u8url)
        gtems = re.findall(v,content)
        # print(gtems);exit(9)
        # print(content)
        # print(gtems);exit(-3)
        #之后替换成多线程
        # for i in gtems:
        #     self.getTs(baseUrl,tsPrefix,i);exit(-3)

        try:
            threadList = []
            for i in gtems:
                threadList.append(threading.Thread(target=self.getTs, name='tsThread'+i, args=(baseUrl,tsPrefix,i,videoNo)))
            for i in threadList:
                i.start()
            for i in threadList:
                i.join()
        except Exception as eo :
            return False
#        finally:            
        return True

    def sourceUrl(self,url):
        urlList = url.split('/')
        urlList = urlList[0:-1]
        url = '/'.join(urlList)
        url += '/'
        return url
     #解析地址名   
    def parseM3u8(self,m3u8url):
        content = self.mainContent(m3u8url)
        if content == None:
            return False
        urlList = []
        g=re.findall('#EXT-X-STREAM-INF(.*?)NAME="(.*?)p"([.|\s|\S|\n]*?)\.m3u8',content)
        for k in g:
           curK = k[2].strip()
           if curK != '':
                urlList.append(curK+".m3u8")
        if len(urlList) == 0:
            return False
        return urlList
    def testValidPath(self,url,list):
        path = list[0];
        for k in list:
            content =  self.mainContent(url+k)
            if content != None:
                return k
        return False
    #抓取页面链接    
    def getVedioUrl(self,pageUrl):
        content = self.mainContent(pageUrl) 
        if content == None:
            return False 
        #print(content);exit('555')
        pattern = '<div id="video_(.*?)" data-id="(.*?)"(.*?)<p class="title"><a href="(.*?)"(.*?)>(.*?)</a></p>(.*?)<span class="duration">(.*?)</span>(.*?)</script></div>'
        gtems = re.findall(pattern,content);

        for v in gtems:#self.doTrans(v[5])
            #print(v);exit('5')
            # t = v[7].replace('min','').strip()
            # t = t.replace('sec','')
            yield {'id':v[0],'rel':v[3],'title':v[5],'ctitle':'','show_time':v[7],'real_time':''}
            # print('id',v[0])
            # print('rel',v[3])
            # print('title',self.doTrans(v[5]))
            # print('show_time',v[7])
            # print('real_time',int(v[7].replace('min','').strip()))            
    def getProxy(self):
            data = [{'http': '47.88.195.233:3128'}, {'http': '188.113.138.238:3128'}, {'http': '114.6.34.194:8080'}, {'http': '176.107.242.142:8080'}, {'http': '142.147.117.1:8080'}, {'http': '162.223.88.243:80'}, {'http': '181.211.191.227:8080'}, {'http': '203.160.172.163:8090'}, {'http': '85.242.171.213:8080'}, {'http': '177.87.45.74:8080'}, {'http': '200.56.200.38:3128'}, {'http': '213.136.77.246:80'}, {'http': '27.131.47.132:8080'}, {'http': '58.176.46.248:80'}, {'http': '116.197.134.130:8080'}, {'http': '213.136.89.121:80'}, {'http': '112.214.73.253:80'}, {'http': '177.37.160.198:3128'}, {'http': '36.37.81.130:8080'}, {'http': '200.68.27.100:3128'}, {'http': '80.1.116.80:80'}, {'http': '178.62.124.132:8118'}, {'http': '41.205.231.202:8080'}, {'http': '93.174.55.82:8080'}, {'http': '101.255.62.202:80'}, {'http': '115.124.73.122:80'}, {'http': '1.179.194.41:8080'}, {'http': '154.73.220.137:8080'}, {'http': '114.199.102.174:8080'}, {'http': '181.49.105.68:8080'}, {'http': '47.90.46.132:3128'}, {'http': '138.36.106.18:3128'}, {'http': '185.21.76.37:8080'}, {'http': '103.36.35.106:8080'}, {'http': '1.179.185.249:8080'}, {'http': '1.179.183.93:8080'}, {'http': '182.253.223.140:8080'}, {'http': '202.150.143.170:8080'}, {'http': '160.202.42.10:8080'}, {'http': '197.220.199.5:443'}, {'http': '122.155.222.98:3128'}, {'http': '197.211.45.4:8080'}, {'http': '120.52.72.59:80'}, {'http': '196.15.141.27:8080'}, {'http': '196.11.90.57:8080'}, {'http': '118.97.24.178:8080'}, {'http': '185.21.76.34:8080'}, {'http': '118.189.157.9:3128'}, {'http': '197.210.196.66:8080'}, {'http': '122.52.133.5:8080'}, {'http': '137.135.166.225:8131'}, {'http': '51.254.132.238:80'}, {'http': '93.63.142.144:80'}, {'http': '78.46.8.204:80'}, {'http': '202.142.158.114:8080'}, {'http': '204.29.115.149:8080'}, {'http': '62.122.100.90:8080'}, {'http': '201.57.249.10:8080'}, {'http': '137.135.166.225:8132'}, {'http': '123.49.34.3:8080'}, {'http': '218.191.247.51:80'}, {'http': '177.135.117.165:3128'}, {'http': '113.253.13.205:80'}, {'http': '180.250.207.162:8080'}, {'http': '177.87.8.50:8080'}, {'http': '45.40.143.57:80'}, {'http': '113.11.87.186:8080'}, {'http': '178.238.229.236:80'}, {'http': '160.202.41.58:8080'}, {'http': '46.16.226.10:8080'}, {'http': '181.39.16.106:8080'}, {'http': '80.245.115.61:8080'}, {'http': '190.104.245.39:8080'}, {'http': '200.29.191.149:3128'}, {'http': '72.252.14.163:8080'}, {'http': '92.255.187.219:8080'}, {'http': '180.250.74.210:8080'}, {'http': '200.108.138.118:3128'}, {'http': '78.83.201.101:8081'}, {'http': '122.155.3.143:3128'}, {'http': '190.248.135.134:8080'}, {'http': '181.229.140.11:8085'}, {'http': '177.103.182.12:3128'}, {'http': '203.83.165.134:8080'}, {'http': '116.68.206.122:8080'}, {'http': '137.135.166.225:8123'}, {'http': '50.30.152.130:8086'}, {'http': '193.232.184.141:8080'}, {'http': '113.185.19.192:80'}, {'http': '122.154.71.49:8080'}, {'http': '202.173.214.15:8080'}, {'http': '94.20.21.38:3128'}, {'http': '178.62.120.187:8118'}, {'http': '186.179.109.77:8080'}, {'http': '190.121.158.114:8080'}, {'http': '152.204.130.62:8080'}, {'http': '177.130.59.66:3128'}, {'http': '210.101.131.231:8080'}, {'http': '196.22.249.124:80'}, {'http': '192.140.223.94:8080'}, {'http': '178.62.118.19:8118'}, {'http': '177.128.225.193:8080'}, {'http': '115.236.7.180:3128'}, {'http': '93.64.156.3:80'}, {'http': '61.136.115.147:3128'}, {'http': '94.23.205.32:3128'}, {'http': '186.225.52.57:8080'}, {'http': '202.148.4.26:8080'}, {'http': '121.15.137.75:808'}, {'http': '110.78.161.106:8080'}, {'http': '180.250.165.156:80'}, {'http': '91.194.42.51:80'}, {'http': '91.217.42.4:8080'}, {'http': '109.201.108.77:8080'}, {'http': '123.7.88.2:3128'}, {'http': '186.103.193.51:8080'}, {'http': '120.85.132.234:80'}, {'http': '124.88.67.81:80'}, {'http': '177.75.70.1:80'}, {'http': '120.28.45.202:8090'}, {'http': '186.10.5.138:8080'}, {'http': '89.26.71.134:8080'}, {'http': '120.76.79.21:80'}, {'http': '137.135.166.225:8133'}, {'http': '115.186.56.146:8080'}, {'http': '177.55.253.68:8080'}, {'http': '120.52.72.56:80'}, {'http': '203.130.192.179:80'}, {'http': '77.123.18.56:81'}, {'http': '190.29.22.247:8080'}, {'http': '61.153.145.202:25'}, {'http': '113.161.68.146:8080'}, {'http': '210.91.48.121:3128'}, {'http': '190.221.23.158:80'}, {'http': '188.93.133.211:8080'}, {'http': '91.98.143.85:80'}, {'http': '181.40.84.194:8080'}, {'http': '120.52.72.54:80'}, {'http': '197.149.179.181:8888'}, {'http': '31.131.67.76:8080'}, {'http': '120.52.73.97:8080'}, {'http': '75.150.203.77:8118'}, {'http': '210.91.48.122:3128'}, {'http': '119.40.98.162:8080'}, {'http': '41.79.170.33:8080'}, {'http': '189.84.51.11:8080'}, {'http': '125.209.91.190:8080'}, {'http': '50.117.86.55:25'}, {'http': '89.191.131.243:8080'}, {'http': '86.102.106.150:8080'}, {'http': '91.143.199.86:3128'}, {'http': '91.221.233.82:8080'}, {'http': '47.88.12.78:8118'}, {'http': '213.60.151.29:80'}, {'http': '114.5.12.178:8080'}, {'http': '122.228.179.178:80'}, {'http': '59.47.125.10:9797'}, {'http': '223.197.56.102:80'}, {'http': '175.154.229.72:8998'}, {'http': '124.42.7.103:80'}, {'http': '177.128.193.114:8089'}, {'http': '89.41.106.99:8080'}, {'http': '124.206.167.250:3128'}, {'http': '183.131.151.208:80'}, {'http': '49.1.244.139:3128'}, {'http': '79.188.42.46:8080'}, {'http': '62.84.66.39:120'}, {'http': '176.106.145.122:8080'}, {'http': '210.91.41.60:3128'}, {'http': '51.254.86.25:80'}, {'http': '185.28.193.95:8080'}, {'http': '202.152.40.28:8080'}, {'http': '103.240.103.10:8080'}, {'http': '139.162.20.41:80'}, {'http': '89.145.188.122:8080'}, {'http': '210.211.18.140:808'}, {'http': '202.59.163.129:8080'}, {'http': '37.236.148.243:8080'}, {'http': '177.66.201.170:8080'}, {'http': '41.160.118.226:8080'}, {'http': '186.219.36.2:8080'}, {'http': '91.217.42.2:8080'}, {'http': '123.30.130.215:3128'}, {'http': '180.234.217.27:8080'}, {'http': '128.199.132.114:8080'}, {'http': '200.195.141.178:8080'}, {'http': '197.210.216.22:8080'}, {'http': '31.146.182.122:443'}, {'http': '150.129.4.18:8080'}, {'http': '202.147.206.114:8080'}, {'http': '202.130.104.236:8080'}, {'http': '124.88.67.39:80'}, {'http': '81.208.32.6:80'}, {'http': '113.200.159.155:9999'}, {'http': '200.192.248.74:8080'}, {'http': '93.174.55.82:80'}, {'http': '61.19.193.211:80'}, {'http': '212.185.87.53:443'}, {'http': '168.63.24.174:8118'}, {'http': '202.51.181.34:8080'}, {'http': '200.33.128.25:8080'}, {'http': '151.80.197.192:80'}, {'http': '197.210.246.30:8080'}, {'http': '1.179.146.153:8080'}, {'http': '137.135.166.225:8119'}, {'http': '125.99.100.73:8080'}, {'http': '194.154.74.210:8080'}, {'http': '180.250.149.73:8080'}, {'http': '1.179.183.109:8080'}, {'http': '82.151.117.162:8080'}, {'http': '91.142.84.182:3128'}, {'http': '119.254.84.90:80'}, {'http': '60.21.221.228:80'}, {'http': '213.57.89.97:18000'}, {'http': '128.199.178.217:8080'}, {'http': '203.91.121.74:3128'}, {'http': '195.34.238.154:8080'}, {'http': '202.56.203.40:80'}, {'http': '40.114.5.134:8118'}, {'http': '91.243.163.202:8080'}, {'http': '115.159.185.186:8088'}, {'http': '190.183.61.157:8080'}, {'http': '183.63.90.197:808'}, {'http': '46.101.22.124:8118'}, {'http': '190.248.153.162:8080'}, {'http': '190.82.94.13:80'}, {'http': '1.179.183.89:8080'}, {'http': '177.39.186.59:8008'}, {'http': '202.69.38.82:8080'}, {'http': '82.117.212.214:8080'}, {'http': '41.220.28.138:8080'}, {'http': '80.77.29.22:80'}, {'http': '178.22.148.122:3129'}, {'http': '80.87.33.134:8080'}, {'http': '118.144.143.249:3128'}, {'http': '123.30.238.16:3128'}, {'http': '187.60.219.248:3128'}, {'http': '89.189.96.24:80'}, {'http': '41.204.93.54:8080'}, {'http': '94.200.231.130:8080'}, {'http': '58.147.174.113:8080'}, {'http': '181.48.203.202:8080'}, {'http': '202.183.32.200:80'}, {'http': '175.184.234.42:8080'}, {'http': '222.92.141.250:80'}, {'http': '178.32.218.91:80'}, {'http': '142.0.128.220:8088'}, {'http': '202.183.32.181:80'}, {'http': '216.241.14.94:8080'}, {'http': '201.222.55.18:8080'}, {'http': '202.183.32.182:80'}, {'http': '221.199.203.106:3128'}, {'http': '189.111.108.160:21320'}, {'http': '116.90.208.131:8080'}, {'http': '221.195.55.182:8080'}, {'http': '184.69.67.122:80'}, {'http': '168.63.24.174:8121'}, {'http': '41.187.15.198:80'}, {'http': '124.155.112.85:80'}, {'http': '202.141.248.130:8080'}, {'http': '80.14.12.161:80'}, {'http': '83.172.144.19:80'}, {'http': '177.207.234.14:80'}, {'http': '103.224.118.191:80'}, {'http': '189.14.199.218:80'}, {'http': '177.5.219.112:8080'}, {'http': '202.183.32.185:80'}, {'http': '203.189.130.125:8080'}, {'http': '37.120.165.209:3128'}, {'http': '173.224.124.210:8080'}, {'http': '188.168.26.0:8080'}, {'http': '118.193.185.83:80'}, {'http': '140.113.195.12:8118'}, {'http': '137.135.166.225:8125'}, {'http': '86.105.226.131:80'}, {'http': '173.201.183.172:8000'}, {'http': '168.63.24.174:8143'}, {'http': '112.25.163.149:63000'}, {'http': '125.217.199.148:80'}, {'http': '183.250.179.29:80'}, {'http': '192.64.10.19:3128'}, {'http': '47.88.8.215:8118'}, {'http': '47.88.6.158:8118'}, {'http': '92.62.28.140:80'}, {'http': '104.236.48.178:8080'}, {'http': '212.47.237.30:9010'}, {'http': '101.255.64.210:80'}, {'http': '137.135.166.225:8127'}, {'http': '168.63.24.174:8146'}, {'http': '168.63.24.174:8137'}, {'http': '23.101.77.155:80'}, {'http': '137.135.166.225:8124'}, {'http': '137.135.166.225:8142'}, {'http': '40.113.118.174:8118'}, {'http': '168.63.24.174:8123'}, {'http': '168.63.20.19:8121'}, {'http': '137.135.166.225:8118'}, {'http': '137.135.166.225:8143'}, {'http': '168.63.24.174:8136'}, {'http': '137.135.166.225:8120'}, {'http': '137.135.166.225:8147'}, {'http': '178.62.123.240:8118'}, {'http': '137.135.166.225:8121'}, {'http': '137.135.166.225:8135'}, {'http': '137.135.166.225:8122'}, {'http': '41.87.164.49:3128'}, {'http': '103.21.77.118:8080'}, {'http': '137.135.166.225:8126'}, {'http': '201.54.5.115:8080'}, {'http': '187.33.229.99:8080'}, {'http': '212.47.239.185:9018'}, {'http': '137.135.166.225:8145'}, {'http': '137.135.166.225:8137'}, {'http': '122.72.18.160:80'}, {'http': '137.135.166.225:8128'}, {'http': '80.72.34.114:80'}, {'http': '212.47.237.30:9015'}, {'http': '186.27.126.130:80'}, {'http': '213.165.155.189:80'}, {'http': '137.135.166.225:8139'}, {'http': '137.135.166.225:8140'}, {'http': '201.241.88.63:80'}, {'http': '179.108.32.255:8080'}, {'http': '91.134.221.52:80'}, {'http': '81.46.212.102:80'}, {'http': '212.1.227.182:80'}, {'http': '51.255.161.222:80'}, {'http': '204.13.164.179:80'}, {'http': '217.29.167.157:80'}, {'http': '203.114.110.83:8080'}, {'http': '221.180.160.114:80'}, {'http': '221.180.160.113:80'}, {'http': '202.175.123.148:80'}, {'http': '177.159.113.114:8080'}, {'http': '168.63.24.174:8119'}, {'http': '80.72.225.179:8080'}, {'http': '111.1.23.173:80'}, {'http': '196.41.60.230:8080'}, {'http': '115.29.34.2:3128'}, {'http': '124.47.7.45:80'}, {'http': '137.135.166.225:8129'}, {'http': '119.29.119.49:80'}, {'http': '181.168.138.149:8080'}, {'http': '119.1.170.3:80'}, {'http': '94.231.116.134:8080'}, {'http': '190.15.222.55:8080'}, {'http': '210.101.131.232:8080'}, {'http': '111.23.6.164:80'}, {'http': '168.63.24.174:8134'}, {'http': '114.215.150.13:3128'}, {'http': '185.15.43.53:8080'}, {'http': '111.1.23.153:8080'}, {'http': '168.63.24.174:8129'}, {'http': '222.86.133.67:80'}, {'http': '121.17.126.68:8081'}, {'http': '177.152.174.141:8080'}, {'http': '185.97.12.130:3128'}, {'http': '81.218.174.175:8088'}, {'http': '79.129.56.159:8080'}, {'http': '137.135.166.225:8146'}, {'http': '152.160.35.171:80'}, {'http': '119.29.232.113:3128'}, {'http': '91.235.91.62:3128'}, {'http': '125.209.97.190:8080'}, {'http': '59.90.111.127:8080'}, {'http': '202.152.20.114:8080'}, {'http': '52.24.15.151:80'}, {'http': '168.63.24.174:8132'}, {'http': '46.101.22.228:8118'}, {'http': '190.52.185.218:8080'}, {'http': '137.135.166.225:8130'}, {'http': '116.212.183.186:8080'}, {'http': '31.148.219.180:80'}, {'http': '82.107.202.30:8080'}, {'http': '212.47.229.71:9002'}, {'http': '154.127.68.193:8080'}, {'http': '124.47.7.38:80'}, {'http': '46.21.93.18:8080'}, {'http': '115.248.109.90:3128'}, {'http': '185.15.43.51:8080'}, {'http': '103.251.83.62:8080'}, {'http': '91.232.188.20:8080'}, {'http': '1.179.176.37:8080'}, {'http': '207.5.112.114:8080'}, {'http': '118.97.239.146:8080'}, {'http': '160.202.42.114:8080'}, {'http': '80.232.222.135:3128'}, {'http': '137.135.166.225:8134'}, {'http': '125.141.200.43:80'}, {'http': '125.141.200.7:80'}, {'http': '125.141.200.20:80'}, {'http': '125.141.200.26:80'}, {'http': '47.88.104.219:80'}, {'http': '125.141.200.5:80'}, {'http': '125.141.200.44:80'}, {'http': '200.123.138.229:8080'}, {'http': '186.177.17.131:8080'}, {'http': '200.223.213.142:3128'}, {'http': '23.91.96.251:80'}, {'http': '120.52.73.1:8081'}, {'http': '146.120.104.166:3128'}, {'http': '125.141.200.14:80'}, {'http': '125.141.200.52:80'}, {'http': '125.141.200.45:80'}, {'http': '173.192.128.238:8123'}, {'http': '201.33.206.229:3128'}, {'http': '125.141.200.53:80'}, {'http': '115.112.106.146:8080'}, {'http': '23.91.97.54:80'}, {'http': '159.8.114.37:25'}, {'http': '125.141.200.21:80'}, {'http': '120.52.73.1:8080'}, {'http': '169.57.1.84:8123'}, {'http': '125.141.200.4:80'}, {'http': '106.39.160.121:80'}, {'http': '201.248.252.243:8080'}, {'http': '125.141.200.40:80'}, {'http': '125.141.200.46:80'}, {'http': '125.141.200.15:80'}, {'http': '1.179.201.18:3128'}, {'http': '200.153.145.109:80'}, {'http': '125.141.200.11:80'}, {'http': '125.141.200.35:80'}, {'http': '125.141.200.55:80'}, {'http': '125.141.200.34:80'}, {'http': '159.8.114.37:8123'}, {'http': '125.141.200.51:80'}, {'http': '125.141.200.24:80'}, {'http': '78.39.252.125:8080'}, {'http': '183.245.146.62:80'}, {'http': '125.141.200.23:80'}, {'http': '202.69.40.173:8080'}, {'http': '125.141.200.37:80'}, {'http': '120.52.73.1:80'}, {'http': '61.5.156.222:8080'}, {'http': '125.141.200.6:80'}, {'http': '115.112.106.147:8080'}, {'http': '123.124.168.107:80'}, {'http': '125.141.200.39:80'}, {'http': '219.141.225.107:80'}, {'http': '125.141.200.2:80'}, {'http': '184.173.139.10:80'}]
            s = random.randint(0,len(data))
            return data[s]

# #EXTM3U
# #EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=423936,RESOLUTION=544x408,NAME="360p"
# hls-360p.m3u8
# #EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=155648,RESOLUTION=374x280,NAME="250p"
# hls-250p.m3u8        
#        return 'hls-360p.m3u8'
    #判断变量类型的函数
    def typeof(self,variate):
        type=None
        if isinstance(variate,int):
            type = "int"
        elif isinstance(variate,str):
            type = "str"
        elif isinstance(variate,float):
            type = "float"
        elif isinstance(variate,list):
            type = "list"
        elif isinstance(variate,tuple):
            type = "tuple"
        elif isinstance(variate,dict):
            type = "dict"
        elif isinstance(variate,set):
            type = "set"
        return type
    # 返回变量类型
    def getType(self,variate):
        arr = {"int":"整数","float":"浮点","str":"字符串","list":"列表","tuple":"元组","dict":"字典","set":"集合"}
        vartype = self.typeof(variate)
        if not (vartype in arr):
            return "未知类型"
        return arr[vartype]
    def getCategory(self,url):
        #<li class="dyn"><a href="/lang/chinese" class="btn btn-default">說中文的色情</a></li>
        pattern = '<li class="sub-list mobile-hide" id="main-cat-sub-list">([.|\s|\S|\n]*?)<ul>([.|\s|\S|\n]*?)</ul></li>'
        content = self.mainContent(url);
        if content == None:
            return False 
        content = re.findall(pattern,content);
        if content == None:
            return False
        #<li class="dyn  topcat topcat-36"><a href="/c/Fucked+Up+Family-81" class="btn btn-default">Fucked Up Family</a></li>
        pattern = '<a href="/c/([.|\s|\S|\n]*?)" class="btn btn-default">([.|\s|\S|\n]*?)</a>'
        #print(self.getType(content[0]));
        contente = content[0][1];
        gtems = re.findall(pattern,contente);
        #return gtems;
        for k,v in gtems:
            #print(v);exit(1)
            yield v
    def getTags(self,url):
        #<li class="dyn"><a href="/lang/chinese" class="btn btn-default">說中文的色情</a></li>
        pattern = '<ul class="tags-list" id="tags">([.|\s|\S|\n]*?)</ul>'
        content = self.mainContent(url);
        if content == None:
            return False 
        content = re.findall(pattern,content)
        pattern = '<b>([.|\s|\S|\n]*?)</span>([.|\s|\S|\n]*?)<b>([.|\s|\S|\n]*?)</b>'
        content = content[0];
        gtems = re.findall(pattern,content)
        for v in gtems:
            yield v[2]
    def doTrans(self,keywords):
        #print(keywords)
        translate = Translator()
        result = translate.translate(keywords,dest='zh-CN');#print(result);exit('3')
        return result.text
        # url = "http://fanyi.youdao.com/translate?&doctype=json&type=AUTO&i="+keywords
        # content = self.mainContent(url);
        # if content == None:
        #     return False 
        # dJson = json.loads(content);
        # curData = dJson['translateResult']
        # return curData[0][0]['tgt']
        # 
        # print(curData);
        # print(curData[0][0]['src'])
        # exit('233')    
# if __name__=='__main__':
#     url="https://www.qq.com/video44806979/elegant_anal_-_nikky_dream_-_frozen_-_babes";
#     #print('llk');exit(8)
#     getObj = videoDemo()
#     getObj.getVedioUrl('https://www.qq.com/')
    #getObj.run(url,'2')
# if text == None:
#    exit(-5)
#print(text)
#return
# targetText = re.match(r'<h2 class="mobile-hide" id="dsktp-title-comment">(.*)</span></h2>', text)
# print(targetText) 
