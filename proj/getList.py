#分页抓取视频url
from videoDemo import videoDemo 
from Dbobj import Dbobj 
import json
from multiprocessing import Pool,Process
import time

def _getList(getObj,curTableObj,url):
    print(url)
    i=0
    for v in getObj.getVedioUrl(url):
        if v['id']!='':
           v['_id'] = dbObj.getNextValue('redios')
           v['tags']=v['cates']=''
           v['status']=0
           curTableObj.update({"id":v['id'].strip()},{"$setOnInsert":v}, upsert=True);	
           i +=1
    print(i) 
def deRange(num):
    url="https://www.qq.com/new/1";
    getObj = videoDemo();
    dbObj = Dbobj('redio','re_')
    arr = [];
    curTableObj = dbObj.getTbname('redios')
    i = num-10000
    while num>=i:
        url="https://www.qq.com/new/"+str(i);
        for v in getObj.getVedioUrl(url):
            if v['id']!='':
               v['_id'] = dbObj.getNextValue('redios')
               v['tags']=v['cates']=''
               v['status']=0
               curTableObj.update({"id":v['id'].strip()},{"$setOnInsert":v}, upsert=True);
        #p.apply_async(_getList, args=(getObj,curTableObj,url))
        i -=1;
        if i%10 == 0:
           time.sleep(0.5)	    
if __name__=='__main__':
    #g = {"type":"EN2ZH_CN","errorCode":0,"elapsedTime":1,"translateResult":[[{"src":"english","tgt":"英语"}]]};
    pageList = range(30,100000,10000)
    pageCount = len(pageList)
    p = Pool(pageCount)
    for i in pageList:
        p.apply_async(deRange, args=(i,))
    p.close()
    p.join()


        	

    # p.close()
    # p.join()
    #        arr.append(v)
    # if len(arr)>0:
    #    re = dbObj.getTbname('redios').insert_many(arr)
        
#'id': '52398905', 'rel': '/video52398905/big_ass_asian_girlfriend_moaning_for_creampie', 'title': 'Big ass asian girlfriend moaning for creampie', 'ctitle': '', 'show_time': '21 min', 'real_time': 21}
