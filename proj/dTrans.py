#分页抓取视频url
from videoDemo import videoDemo 
from Dbobj import Dbobj 
import json
from multiprocessing import Pool,Process
import time
import pymongo
import math
import sys
sys.path.append('..')
from commone.GoogleTranslator import GoogleTranslator

def trans(g,text):
    e = g.translate(text)
    return e   
def pTrans(curTableObj,curPage):
    skip = (curPage-1)*10000
    data = curTableObj.find({"status":1,"ctitle":""}).sort('_id', pymongo.ASCENDING).limit(10000).skip(skip)
    i = 0
    for v in data:
       translator = GoogleTranslator()
       title = v['title'].strip('/').replace('&#039','').replace('&amp;','')
       #print(title) 
       tags = trans(translator,title)
       #print(tags);exit('3')
       if tags == '':
          curTableObj.update({"id":v['id']},{"$set":{"status":3}})
       else: 
          curTableObj.update({"id":v['id']},{"$set":{"ctitle":tags}})
       i +=1
       if i%10:
          time.sleep(0.3)      
if __name__=='__main__':    
    getObj = videoDemo();
    dbObj = Dbobj('redio','re_')
    arr = [];
    curTableObj = dbObj.getTbname('redios')

    #pTrans(curTableObj,1);exit('5')
    #base = 'https://www.qq.com/'
       #_count = len(data)
    p = Pool(processes = 5)
    i = 5
    while i>0:
      p.apply_async(pTrans, args=(curTableObj,i))
      i -=1
    p.close()
    p.join()      
    print('成功')
    #    p.apply_async(curTableObj.vdetail, args=(curUrl,v['id']))
    # p.close()
    # p.join()
    # print('All subprocesses done.')