#coding:utf-8
import pymongo

client=pymongo.MongoClient('localhost',27017)#链接数据库

#创建dbdb数据库
db =client['redio']

#创建username_id集合
username_id = db['table_id']

#自增函数
def getNextValue(user_Name):
    ret = username_id.find_and_modify({"_id": user_Name}, {"$inc": {"sequence_value": 1}}, safe=True, new=True)
    new = ret["sequence_value"]
    return new

if __name__=='__main__':
    #插入username_id
    username_id.insert_one(({'_id': "re_redios", 'sequence_value': 0}))
