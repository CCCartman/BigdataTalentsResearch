# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 19:44:09 2018

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
    
    url = 'https://www.liepin.com/zhaopin/?init=1&imscid=R000000058&d_sfrom=search_fp_bar&key=%s' %keyword_url
    
    response = session.get(url)
    soup = BeautifulSoup(response.text,'lxml')
    
    last_ = soup.find('div',{'class':'pagerbar'}).find('a',{'class':'last'})
    pagenum = int(re.findall(r'.*?d_curPage.*?curPage=(.*?)" title=.*?',str(last_),re.S)[0])
    
    #print('***本次搜索到%d个页面***'%totalCount)
    #pagenum =  int (totalCount // 50)
    print('***本次搜索到%d个页面***'%pagenum)
    return pagenum

def parse_all_page(keyword,pagenum):
    global session,headers2
    
    keyword_url = parseString(keyword)
    
    for i in range(2,pagenum + 1):
        if i == 1:
            url = 'https://www.liepin.com/zhaopin/?init=1&imscid=R000000058&d_sfrom=search_fp_bar&key=%s' %keyword_url
        else:
            url = 'https://www.liepin.com/zhaopin/?ckid=807423f6b1937b5a&fromSearchBtn=2&degradeFlag=0&init=-1&key=' + keyword_url +'&imscid=R000000058&headckid=807423f6b1937b5a&d_pageSize=40&siTag=g7ncQVyJkg3z1_MbYtHi6w%7EfA9rXquZc5IkJpXC-Ycixw&d_headId=4d57f20d22490ea1f91690b1c2aed196&d_ckId=4d57f20d22490ea1f91690b1c2aed196&d_sfrom=search_fp_bar&d_curPage='+str(i-1)+'&curPage=' + str(i)
        
        try:
            response = session.get(url)
            soup = BeautifulSoup(response.text,'lxml')
            total_ = len(soup.find('ul',{'class':'sojob-list'}).findAll('li'))
            urls_ = [soup.find('ul',{'class':'sojob-list'}).findAll('li')[i].find('div',{'class':'job-info'}).find('a').get('href') for
                         i in range(total_)]
        except:
            continue
        
        for url2 in urls_:
            try:
                response2 = requests.get(url2,headers = headers2)
                soup2 = BeautifulSoup(response2.text,'lxml')
            except:
                continue
            try:
                city = soup2.find('div',{'class':'job-title-left'}).find('a').get_text()
                print(city)
            except:
                city = ''
            try:
                company = soup2.find('div',{'class':'title-info'}).find('h3').get_text().strip()
                print(company)
            except:
                company = ''
            try:
                position = soup2.find('div',{'class':'title-info'}).find('h1').get_text()
                print(position)
            except:
                position = ''
            try:
                edu = soup2.find('div',{'class':
                        'job-title-left'}).find('div',
                    {'class':'job-qualifications'}).findAll('span')[0].get_text()
                print(edu)
            except:
                edu = ''
            try:
                salary = soup2.find('div',{'class':'job-title-left'}).find('p',{'class':
                        'job-item-title'}).get_text().split('\r')[0] 
                print(salary)
            except:
                salary = ''
            try:
                description = soup2.find('div',{'class':
                    'job-item main-message job-description'}).get_text().strip().replace('\r',
                            '') .replace('\n','').replace('\t','')
                print(description)
            except:
                description = ''
            
            yield {'source':'猎聘网',
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
    with open('D:\\workspace python\\statContest\\liepin\\' + fileName,'a',newline='',encoding='utf-8') as csvfile:
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

    mySql_.create_table('liepin')
    
    session = requests.Session()
    session.headers['referer'] = 'https://c.liepin.com/?time=%s' % str(int(float(time.time()) * 1000))
    session.headers['user-agent'] = \
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'

 
    keyword = '机器学习'
    pagenum = GetPagnum(keyword)
    #count = 0
    #save_info_csv(count,count,fileName = 'wuyou-dsjfx.csv')
    count = 1
    ua = UserAgent()
    headers2 = {'User-Agent':ua.random}
    for content in parse_all_page(keyword,pagenum):
        #save_info_csv(content,count,fileName = 'zhilian-dsjfx.csv')
        print(content)
        mySql_.innsert_data(content,'liepin')
        print('现在已经爬取第 %d 个公司' % count)
        count += 1

# 大数据分析 数据挖掘 机器学习