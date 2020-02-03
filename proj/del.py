import sys
sys.path.append('..')
from commone.GoogleTranslator import GoogleTranslator
import time
from Dbobj import Dbobj 
import pymongo

if __name__ == "__main__":
    startTime = time.time()
    dbObj = Dbobj('redio','re_')
    arr = [];
    curTableObj = dbObj.getTbname('tags')
    newRe = _re = []
    data = curTableObj.find({"cname":""}).sort('_id', pymongo.ASCENDING).limit(1000)
    j = 0
    g = GoogleTranslator()
    for v in data:

        #v['title']=v['title'].replace('&#039','').replace('&amp;','')

        s=ctitle = g.translate(v['name'])
        curTableObj.update({"_id":v['_id']},{"$set":{"cname":ctitle}})
        if j%10:
           time.sleep(0.5)