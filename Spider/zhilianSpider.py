# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 18:17:56 2018

@author: Rui Wenhao
@Copyright: Rui Wenhao, All rights reserved
@Mail:rui_wenhao@cueb.edu.cn
"""
import requests
from bs4 import BeautifulSoup
import random
import time
from fake_useragent import UserAgent
import re
import csv
import urllib
from content2SQL import mySql

'''智联招聘'''

def rawCookie2Cookie(raw_cookies):
    '''
    返回Dict形式的cookies
    '''
    cookies = {}
    for line in raw_cookies.split(';'):
        key, value = line.split('=',1) #1代表只分一次，得到两个数据
        cookies[key]=value
    return cookies

def parseString(string):
    urlcode = urllib.request.quote(string)
    return urlcode

def GetPagnum(keyword):
    keyword_url = parseString(keyword)
    url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%e9%80%89%e6%8b%a9%e5%9c%b0%e5%8c%ba&kw=' + keyword_url + '&isadv=0&sg=9b51c6d393a64675b18791aedf3fdc84&p=1'
    
    response = session.get(url)
    soup = BeautifulSoup(response.text,'lxml')
    totalCount = int(soup.find('span',{'class':'search_yx_tj'}).find('em').get_text())
    print('***本次搜索到%d个职位***'%totalCount)
    pagenum =  int (totalCount // 60)
    print('***本次搜索到%d个页面***'%pagenum)
    return pagenum

def parse_all_page(keyword,pagenum):
    keyword_url = parseString(keyword)
    for i in range(1,pagenum + 1):
        try:
            url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%e9%80%89%e6%8b%a9%e5%9c%b0%e5%8c%ba&kw=' + keyword_url + '&isadv=0&sg=9b51c6d393a64675b18791aedf3fdc84&p=' + str(i)
            response = session.get(url)
            soup = BeautifulSoup(response.text,'lxml')
            total_ = soup.findAll('table',{'class':'newlist'})[1:]
            
            urls = [each.find('td',{'class':'zwmc'}).find('a').get('href')
            for each in total_]
            print(urls)
            #time.sleep(20 + random.uniform(0,10))
        except:
            continue
        
        for url2 in urls:
            #time.sleep(3.5 + random.uniform(0,4))
            try:
                response2 = requests.get(url2,headers = headers2)              
                soup2 = BeautifulSoup(response2.text,'lxml')
            except:
                continue
            
            if 'xiaoyuan' not in url2:
                try:    
                    company = soup2.find('div',{'class':'fl'}).find('h2').get_text() # 公司名称
                    print(company)
                except:
                    company = ''
                try:                   
                    position = soup2.find('div',{'class':'fl'}).find('h1').get_text()# 岗位名称
                    print(position)
                except:
                    position = ''
                try:
                    description = soup2.find('div',{'class':
                        'tab-inner-cont'}).get_text().strip().replace('\r'
                                            ,'').replace('\n','') # 具体要求
                    print(description)
                except:
                    description = ''
                try: # 工作地点
                    city = soup2.find('ul',{'class':'terminal-ul clearfix'}).findAll('li')[1].get_text().split('：')[1] 
                    print(city)
                except:
                    city = ''
                try:
                    edu = soup2.find('ul',{'class':'terminal-ul clearfix'}).findAll('li')[5].find('strong').get_text()
                    print(edu)
                except:
                    edu = ''
                try:
                    salary = soup2.find('ul',{'class':'terminal-ul clearfix'}).findAll('li')[0].find('strong').get_text().replace('\xa0','')
                    print(salary)
                except:
                    salary = ''
            else:

                try:    
                    company = soup2.find('li',{'id':'jobCompany'}).get_text().strip() # 公司名称
                    print(company)
                except:
                    company = ''
                try:                   
                    position = soup2.find('h1',{'id':'JobName'}).get_text().strip()# 岗位名称
                    print(position)
                except:
                    position = ''
                try:
                    description = soup2.find('div',{'class':
                        'j_cJob_Detail'}).find('p').get_text().strip().replace('\r'
                                            ,'').replace('\n','')  # 具体要求
                    print(description)
                except:
                    description = ''
                try: # 工作地点
                    city = soup2.find('li',{'id':'currentJobCity'}).get_text().strip()# 工作地点
                    print(city)
                except:
                    city = ''
                    
                edu = '校园招聘' ## 校园招聘edu标注为校园招聘
                salary = ''
            
            yield {'source':'智联招聘',
                   'keyword':keyword,
                    'links':url2,
                   'city':city,
                   'company':company,
                   'position':position,
                   'edu':edu,
                  'salary':salary,
                   'description':description}
            
def save_info_csv(content,count,fileName):
    '''
    保存数据到csv
    '''
    with open('D:\\workspace python\\statContest\\zhilian\\' + fileName,'a',newline='',encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if count == 0:      
            writer.writerow(('来源','关键词','链接','城市','公司名称','岗位',
                             '学历','工资','岗位描述'))
            print('===========变量名全部写入=========')
            csvfile.close()
        else:
            writer.writerow([content['source'],content['keyword'],content['links'],content['city'],
                            content['company'],content['position'],
                            content['edu'],content['salary'],
                            content['description']])
            print('===========写了一行内容===========')
            csvfile.close()     
  
          
if __name__ == '__main__':
    
    sql_params = {
                'host':'localhost',
                'port':3306,
                'user':'root',
                'passwd':'mysql123',
                'db':'bigData',
                'charset':'utf8'
                }
    mySql_ = mySql(**sql_params)
    
    del sql_params

    mySql_.create_table('zhilian')
    
    session = requests.Session()
    session.headers['referer'] = 'https://www.zhaopin.com/'
    session.headers['user-agent'] = \
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    
    keyword = '机器学习'
    pagenum = GetPagnum(keyword)
    #count = 0
    #save_info_csv(count,count,fileName = 'zhilian-dsjfx.csv')
    count = 1
    ua = UserAgent()
    headers2 = {'User-Agent':ua.random}
    for content in parse_all_page(keyword,pagenum):
        
        print(content)
        mySql_.innsert_data(content,'zhilian')
        #save_info_csv(content,count,fileName = 'zhilian-dsjfx.csv')
        print('现在已经爬取第 %d 个公司' % count)
        count += 1

 ## 大数据分析 数据科学 数据挖掘 机器学习
## 爬到了1623 + 2460