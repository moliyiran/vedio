#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import pymongo

class Dbobj:
    def __init__(self, dbname, prefix='', idTable="table_id",host='127.0.0.1', port='27117'):
       self.__dbName = dbname
       self.__host = host
       # self.__user = user
       # self.__pwd = pwd
       self.myclient = pymongo.MongoClient("mongodb://"+host+":"+port+"/")#root:123456@
       self.mydb = self.myclient[dbname]
       self.__prefix = prefix 
       self.idTable = idTable
    #自增函数
    def getNextValue(self, user_Name):
       obj = self.getTbname(self.idTable);
       user_Name = self.__prefix+user_Name
       #print(user_Name)
       ret = obj.find_and_modify({"_id": user_Name}, {"$inc": {"sequence_value": 1}}, new=True)
       new = ret["sequence_value"]
       return int(new)
    #eg:user_name.insert_one({'_id':getNextValue('name'),'myname':n})
    # if __name__=='__main__':
    #    #插入username_id
    #    username_id.insert_one(({'_id': "name", 'sequence_value': 0}))
    def getTbname(self, name):
        curTable = self.mydb[self.__prefix+name]
        return curTable
# dobj = Dbobj('redio','re_')
# id = dobj.getNextValue('tags')
# print(id)
 
