from multiprocessing import Pool
import os, time, random
from GoogleTranslator import GoogleTranslator
import time
from Dbobj import Dbobj 
import pymongo

def long_time_task(curPage):
    skip = (curPage-1)*10000
    data = curTableObj.find({"status":1,"ctitle":""}).sort('_id', pymongo.ASCENDING).limit(100).skip()
    j = 0
    g = GoogleTranslator()
    for v in data:

        v['title']=v['title'].replace('&#039','').replace('&amp;','')

        s=ctitle = g.translate(v['title'])
        if s == '':

            curTableObj.update({"id":v['id']},{"$set":{"status":3}})
        else:
            curTableObj.update({"id":v['id']},{"$set":{"ctitle":ctitle}})
        if j%10:
           time.sleep(0.5)
        j +=1

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = Pool(5)
    for i in range(5):
        j = i + 1
        p.apply_async(long_time_task, args=(j,))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')