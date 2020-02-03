#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import sys
sys.path.append('..')
from commone.Dbobj import Dbobj 
import re
 
urls = ('https://www.qq.com/change-country/cn')
 
#browser=webdriver.Chrome('C:\\Users\Abb\\Downloads\\chromedriver_win32\\chromedriver.exe')# 注意大写！！

chrome_options = webdriver.ChromeOptions()
# 使用headless无界面浏览器模式
chrome_options.add_argument('--headless') #增加无界面选项
chrome_options.add_argument('--disable-gpu') #如果不加这个选项，有时定位会出现问题

# 启动浏览器，获取网页源代码
browser = webdriver.Chrome('D:\\soft\\chromedriver_win32\\chromedriver.exe',chrome_options=chrome_options)
#print(type(browser))
 
url = 'https://www.qq.com/change-country/cn'
get_url = browser.get(url)
htmlContent = browser.page_source
browser.quit()
if htmlContent is None:
    exit(1)
print(htmlContent.encode('gbk', 'ignore').decode('gbk'));exit('3');
dbObj = Dbobj('redio','re_')

pattern ='<li class="sub-list mobile-hide" id="main-cat-sub-list"><ul>([.|\s|\S|\n]*?)</ul></li>'
tags = re.findall(pattern,htmlContent)
#print(tags);exit(88)
if tags is None or len(tags)<1:
    exit(2)
tags =tags[0]
#print(tags)
#pattern = '<a href="(.*)"(.*)>(.*)</a>'
pattern ='<a href="([.|\s|\S|\n]*?)" class="btn btn-default">([.|\s|\S|\n]*?)</a>'
listTags = re.findall(pattern,tags)
#print(listTags);exit(557)
#&amp;top &
reTags = []
for i in listTags:
    if len(i[1])>0:
       reTags.append({'url':i[0].replace('&amp;','&'),'title':i[1],'_id':dbObj.getNextValue('category')})
curTableObj = dbObj.getTbname('category')
curTableObj.insert_many(reTags)
arr = [];

pattern = '<div class="home-trends ordered-label-list">([.|\s|\S|\n]*?)</div>'
trends = re.findall(pattern,htmlContent)
if trends is None or len(trends[0])<0:
    exit(3)
pattern = '<a class="btn btn-default" href="([.|\s|\S|\n]*?)">([.|\s|\S|\n]*?)</a>'
tags = re.findall(pattern,trends[0])

if tags is None or len(tags)<1:
    exit(4)
curTableObj = dbObj.getTbname('trends')
reTrends = []
for i in tags:
    if len(i[1])>0:
       reTrends.append({'url':i[0].replace('&amp;','&'),'title':i[1],'_id':dbObj.getNextValue('trends')})
curTableObj.insert_many(reTrends)


