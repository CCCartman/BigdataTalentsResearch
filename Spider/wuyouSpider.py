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

'''前程无忧'''

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
    global session
    keyword_url = parseString(keyword)
    url = 'http://search.51job.com/list/000000,000000,0000,00,9,99,' + keyword_url + ',2,1.html'
    
    response = session.get(url)
    soup = BeautifulSoup(response.text,'lxml')
    totalCount = int(re.findall(r'\d+',soup.find('div',{'class':
            'dw_tlc'}).find('div',{'class':'rt'}).get_text().strip())[0])
    
    print('***本次搜索到%d个职位***'%totalCount)
    pagenum =  int (totalCount // 50)
    print('***本次搜索到%d个页面***'%pagenum)
    return pagenum,totalCount

def parse_all_page(keyword,pagenum):
    global session,headers2
    keyword_url = parseString(keyword)
    for i in range(1,pagenum):
        try:
            url = 'http://search.51job.com/list/000000,000000,0000,00,9,99,' + keyword_url + ',2,' + str(i) + '.html'
            response = session.get(url)
            soup = BeautifulSoup(response.text,'lxml')
            total_ = soup.find('div',{'class':
                        'dw_table'}).findAll('div',{'class':'el'})[1:]
            
            urls = [each.find('p',{'class':'t1'}).find('a').get('href')
                for each in total_]
            print(urls)
            #time.sleep(20 + random.uniform(0,10))
            
        except:
            continue
        
        for url2 in urls:
            if 'jobs.51job.com' in url2:
                #time.sleep(3.5 + random.uniform(0,4))
                try:
                    response2 = requests.get(url2,headers = headers2) 
                    response2.encoding = 'gbk'            
                    soup2 = BeautifulSoup(response2.text,'lxml')
                    cn = soup2.find('div',{'class':'cn'})
                except:
                    continue
                try:    # 公司名称
                    company = cn.find('p',{'class':'cname'}).get_text().strip() 
                    print(company)
                except:
                    company = ''
                try:     # 岗位名称            
                    position = cn.find('h1').get('title')
                    print(position)
                except:
                    position = ''
                try: # 工作地点
                    city = cn.find('span',{'class':'lname'}).get_text().strip() 
                    print(city)
                except:
                    city = ''
                try:# 具体要求
                    description = re.findall(r'<div class="bmsg job_msg inbox">(.*?)<div class="mt10">',
                                             response2.text,
                                             re.S)[0].strip().replace('<br>','').replace('\r'
                                            ,'').replace('\n','') .replace('</p>'
                                                        ,'').replace('<p>','')
                    print(description)
                except:
                    description = ''
                try:
                    salary = cn.find('strong').get_text()
                    print(salary)
                except:
                    salary = ''
                try:
                    edu = re.findall(r'<em class="i2"></em>(.*?)</span>',
                                     response2.text,re.S)[0]
                    print(edu)
                except:
                    edu = ''

            else:
                continue
            
           
            yield {'source':'前程无忧',
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
    with open('D:\\workspace python\\statContest\\wuyou\\' + fileName,'a',newline='',encoding='utf-8') as csvfile:
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

    mySql_.create_table('51job')
    
    session = requests.Session()
    session.headers['referer'] = 'http://www.51job.com/?from=baidupz'
    session.headers['user-agent'] = \
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
 
    keyword = '数据分析'
    pagenum,totalCount = GetPagnum(keyword)
    count = 0
    save_info_csv(count,count,fileName = 'wuyou-test.csv')
    count = 1
    ua = UserAgent()
    headers2 = {'User-Agent':ua.random}
    for content in parse_all_page(keyword,pagenum):
        save_info_csv(content,count,fileName = 'wuyou-test.csv')
        print(content)
        mySql_.innsert_data(content,'51job')
        print('现在已经爬取第 %d|%d 个公司' % (count,totalCount))
        count += 1
# 大数据分析 数据科学 数据挖掘 机器学习

