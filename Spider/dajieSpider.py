# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 18:17:56 2018

@author: Rui Wenhao
@Copyright: Rui Wenhao, All rights reserved
@Mail:rui_wenhao@cueb.edu.cn
"""
#import math
import json
import requests
from bs4 import BeautifulSoup
import random
import time
#from fake_useragent import UserAgent
#import re
import csv
import urllib
from content2SQL import mySql

'''大街网'''

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


def getPageNum(url,keyword,headers,cookies):
    global session
    #response = requests.get(url,headers = headers,cookies = cookies)
    session.get('https://so.dajie.com/job/search')
    response = session.get(url)
    print(response.text)
    totalCount = json.loads(str(response.text))['data']['total']
    totalCount = int(totalCount)
    print('*****本次搜索到%d个职位*****'%totalCount)
    pagenum =  totalCount // 30
    print('*****本次要爬取%d个页面*****'%pagenum)
    return pagenum


def process_page(keyword):
    global raw_cookies
    keyword_url = parseString(keyword)
    url = 'https://so.dajie.com/job/ajax/search/filter?keyword=' + keyword_url + '&order=0&city=&recruitType=&salary=&experience=&page=' + str(1) +'&positionFunction=&_CSRFToken=ZRoYUF9-7KKO4pQjVSac0hGEBPAcQ02aJgWELZg*&ajax=1'
    headers = {
    #'cookie': 'DJ_UVID=MTUxODE3OTYwNDM5OTM1ODM2; dj_auth_v3=M-6X0LP3RwUcfWUXZ_8SpAOlhEKUIUw_8Yhc8UDpTE5_W2frwqIzgxxFywvodpcXCA**; dj_auth_v4=40536249967b8dce54978e455c110245_pc; uchome_loginuser=39354520; _check_isqd=no; DJ_RF=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DnwOtLu0jni42jw0unOlup3F-aYb6Jek6xEvutYjrxSG%26wd%3D%26eqid%3Df6da71cd00011592000000025a7daae9; DJ_EU=http%3A%2F%2Fwww.dajie.com%2F; SO_COOKIE_V2=97b05vtNvqU/2l7C2bs/tdI/z25FryNzDgAo9YgXAqDMgi88U9BZ8VyklL93UyFDW1CWeTsj5+c6lXEqrFOahA5qOBRCO2c9aVQ4',
    'referer': 'https://so.dajie.com/job/search?keyword=' + keyword_url + '&from=job&clicktype=blank',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    
    #raw_cookies = 'SO_COOKIE_V2=6450VEzt58B2+w1Lnpu3LCkcNZmXNx0yT4zE1sgqKTCPBaRCqLKv6SO+0og9iOa5J5Bhfmf0WYOKWiJfF9xsixqSKCy2+cSALb84'
    cookies = rawCookie2Cookie(raw_cookies)
    
    pagenum = getPageNum(url,keyword,headers,cookies)
    print('***********一共有 %s 页***********' % pagenum)
    return headers,cookies,pagenum

def parse_all_page(keyword,headers,pagenum):
    global cookies_,cookie2_,session
    keyword_url = parseString(keyword)
    #headers,cookies,pagenum = process_page(keyword)
    for i in range(1,pagenum + 1):
        print('*****************正在爬取第 %s 页**********************' % i)
        print('*****************正在爬取第 %s 页**********************' % i)
        
        try:
            url = 'https://so.dajie.com/job/ajax/search/filter?keyword=' + keyword_url + '&order=0&city=&recruitType=&salary=&experience=&page=' + str(i) +'&positionFunction=&_CSRFToken=ZRoYUF9-7KKO4pQjVSac0hGEBPAcQ02aJgWELZg*&ajax=1'
            #response = session.get(url,headers = headers,cookies = cookies_)
            session.get('https://so.dajie.com/job/search')
            response = session.get(url)
            pageContent = json.loads(str(response.text))

            jobHrefLinks = []
            for eachContent in pageContent['data']['list']:
                jobHrefLinks.append('https:' + eachContent['jobHref'])

            print(jobHrefLinks)
        except:
            continue
        #time.sleep(15 + random.randint(0,8))
        
        for url2 in jobHrefLinks:
            #time.sleep(5 + random.randint(0,3))
            headers2 = {
                   'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'accept-encoding':'gzip, deflate, sdch, br',
                   'accept-language':'zh-CN,zh;q=0.8',
                   'cache-control':'max-age=0',
                   #'cookie':'DJ_UVID=MTUxODI1OTcxMDcxOTYxMjYx; dj_auth_v3=MVqlsuauZBBDoVxK_iZuBTCGpFb2VXROsqcknRCJc3eSpVLBvi8sEuvcf8wgGH4*; dj_auth_v4=f6ded454d61b901da717c2b7749b3f4c_pc; uchome_loginuser=39354520; _check_isqd=no; __guid=92263169.3423973329360860000.1518260184439.874; DJ_RF=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DPCOJl4oEXiHi3VF9C3DsZjMxfk8fUVbWCVVbYqhJniMFrtfksQlOmHSVQyh3KMZd%26wd%3D%26eqid%3Dfe0e1199000557e9000000025a7ed821; DJ_EU=http%3A%2F%2Fwww.dajie.com%2Faccount%2Flogin; monitor_count=10; USER_ACTION="request^ACampus^AAUTO^Ajobdetail:^A-"',
                   'cookie':cookie2_,
                   'upgrade-insecure-requests':'1',
                   'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
                   } 
            try:
                response2 = requests.get(url2,headers = headers2)
                soup = BeautifulSoup(response2.text,'lxml')
            except:
                continue
            try:
                company = soup.find('p',{'class':'title'}).find('a').get_text().strip()
                print(company)
            except:
                company = ''
            try:
                city = soup.find('li',{'class':'ads'}).get_text()
                print(city)
            except:
                city = ''
            try:
                position = soup.find('span',{'class':'job-name'}).get_text()
                print(position)
            except:
                position = ''
            try:
                description = soup.find('div',{'class':
                    'position-data'}).findAll('pre')[1].get_text().replace('\r','').replace('\n','') 
                print(description)
            except:
                description = ''
            try:
                edu = soup.find('div',{'class':'job-msg-center'}).find('li',
                               {'class':'edu'}).get_text()
                print(edu)
            except:
                edu = ''
            try:
                salary = soup.find('span',{'class':'job-money'}).get_text()
                print(salary)
            except:
                salary = ''
            yield { 'source':'大街网',
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
    with open('D:\\workspace python\\statContest\\dajie\\' + fileName,'a',newline='',encoding='utf-8') as csvfile:
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
    mySql_.create_table('dajie')
    
    keyword = '数据分析'
    raw_cookies = 'SO_COOKIE_V2=efe7XgUOJm3BAXUtMnkEU++cq6mQLRtsxXryUKMAHiBUU3YYucspeOFycQT8tZ3UTAKUwixi/23N2FCSKRqWw3pYNZ5/bE10BRSl'
    cookie2_ = 'DJ_UVID=MTUxODI1OTcxMDcxOTYxMjYx; dj_auth_v3=MVqlsuauZBBDoVxK_iZuBTCGpFb2VXROsqcknRCJc3eSpVLBvi8sEuvcf8wgGH4*; dj_auth_v4=f6ded454d61b901da717c2b7749b3f4c_pc; uchome_loginuser=39354520; _check_isqd=no; __guid=92263169.3423973329360860000.1518260184439.874; DJ_RF=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D2fqb7OND2-GWyt-duaHJ6rfnVjZABVQrQiYGaHxXrkm%26wd%3D%26eqid%3Debe3ec2a0006d5fe000000025a7f9a17; DJ_EU=http%3A%2F%2Fwww.dajie.com%2F; monitor_count=14; USER_ACTION="request^ACampus^AAUTO^Ajobdetail:^A-"'
    #count = 0
    #save_info_csv(count,count,fileName = 'dajie-shujufenxi.csv')
    count = 1

    session = requests.Session()
    session.headers['referer'] = 'https://so.dajie.com/job/search'
    session.headers['user-agent'] = \
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'

    headers,cookies_,pagenum = process_page(keyword)
    for content in parse_all_page(keyword,headers,pagenum):
        #save_info_csv(content,count,fileName = 'dajie-shujufenxi.csv')
        mySql_.innsert_data(content,'dajie')
        print(content)
        print('现在已经爬取第 %d 个公司' % count)
        count += 1

# 大数据 数据挖掘 数据科学 机器学习 数据分析