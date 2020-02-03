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
chrome_options.add_argument('--no-sandbox')

# 启动浏览器，获取网页源代码
browser = webdriver.Chrome('D:\\soft\\chromedriver_win32\\chromedriver.exe',chrome_options=chrome_options)
#print(type(browser))
 
url = 'https://www.qq.com/change-country/cn'
#url = 'https://www.qq.com/'
get_url = browser.get(url)
htmlContent = browser.page_source
browser.quit()
if htmlContent is None:
    exit(1)
#print(htmlContent.encode('gbk', 'ignore').decode('gbk'));exit('3');
dbObj = Dbobj('redio','re_')
#print(dbObj.getNextValue('trends'));exit('3')
pattern ='<nav aria-label="secondary">([.|\s|\S|\n]*?)</nav>'
trends = re.findall(pattern,htmlContent)
if trends is None:
    exit(1)
trends = trends[0]
pattern = '<li><a class="btn btn-default" href="([.|\s|\S|\n]*?)">([.|\s|\S|\n]*?)</a></li>'
trends = re.findall(pattern,trends)
#print(trends);#.encode('utf-8', 'ignore').decode('utf-8')
if trends is None or len(trends)<1:
    exit(2)
curTableObj = dbObj.getTbname('trends')
reTrends = []
for i in trends:
   curTitle = i[1].strip()
   curUrl = i[0].replace('&amp;','&').strip()
   curInfo = curTableObj.find_one({"$or":[{"title":curTitle},{"url":curUrl}]})

   if curInfo is None:
   	  #print(i[0].replace('&amp;','&'));exit('1')
   	  reTrends.append({'url':curUrl,'title':curTitle,'_id':dbObj.getNextValue('trends')})

if len(reTrends)>0:
	curTableObj.insert_many(reTrends)  