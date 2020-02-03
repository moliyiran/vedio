import sys
sys.path.append('..')
from commone.GoogleTranslator import GoogleTranslator
import time
from Dbobj import Dbobj 
import pymongo

def readFile(fileName):
    with open(fileName, 'r') as f:
        paragraph = ''
        for line in f:
            if line[0]!='\n':
                paragraph += line.strip('\n')
            else:
                if len(paragraph)>0:
                    yield paragraph
                    paragraph = ''
        if len(paragraph)>0:
            yield paragraph
def main():
    translator = GoogleTranslator()
    count = 0
    with open('C:\\dx\\python\\d.txt', 'w', encoding='utf-8') as df:
        for line in readFile('C:\\dx\\python\\s.txt'):
            if len(line) > 1:
                count += 1
                print('\r' + str(count), end = '', flush = True)
                df.write(line.strip() + "\n")
                result = translator.translate(line)
                df.write(result.strip() + "\n\n")

if __name__ == "__main__":
    startTime = time.time()
    # j = 10;
    # while j>0:
    #     e = g.translate('go home')
    #     print(e);
    #     j -=1
    # exit('5')    
    dbObj = Dbobj('redio','re_')
    arr = [];
    curTableObj = dbObj.getTbname('redios')
    newRe = _re = []
    i = 10000
    while i>0:
        data = curTableObj.find({"status":1,"ctitle":""}).sort('_id', pymongo.ASCENDING).limit(100)
        j = 0
        g = GoogleTranslator()
        for v in data:

            v['title']=v['title'].replace('&#039','').replace('&amp;','')

            s=ctitle = g.translate(v['title'])
            if s == '':
                #curTableObj.update({"id":v['id']},{"$set":{"ctitle":ctitle}})

                curTableObj.update({"id":v['id']},{"$set":{"status":3}})
            else:
                curTableObj.update({"id":v['id']},{"$set":{"ctitle":ctitle}})
            if j%10:
               time.sleep(0.5)
            #i +=1       
        #print(g.translate('how are you'))
        #time.sleep(1)
       #_re.append({'_id':v['_id'],'title':v['title']})
    # for f in _re:
    #     newRe.append({"_id":f['_id'],"title":g.translate(f['title'])})
    #     time.sleep(1)   
    # print(newRe)
       # if e != '':
       #    curTableObj.update({"id":v['id']},{"$set":{"ctitle":e}})
        
    # main()
    # print()
    # print('%.2f seconds' % (time.time() - startTime))