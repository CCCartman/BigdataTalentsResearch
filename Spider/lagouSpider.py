# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 18:17:56 2018

@author: Rui Wenhao
@Copyright: Rui Wenhao, All rights reserved
@Mail:rui_wenhao@cueb.edu.cn
"""
import math
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

'''拉勾网'''

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

def GetPagnum(url,keyword,headers):
    data = {'first': 'true','pn': '1', 'kd': keyword} 
    html = requests.post(url,headers = headers,data = data)
    totalCount = int(json.loads(str(html.text))['content']['positionResult']['totalCount'])
    print('***本次搜索到%d个职位***'%totalCount)
    pagenum =  int (math.ceil(totalCount/15) )
    return pagenum

def process_page(keyword,city):
    global cookie_index_page,cookie_each_page
    keyword_url = parseString(keyword)
    city_url = parseString(city)
    url = 'https://www.lagou.com/jobs/positionAjax.json?city=' + city_url + '&needAddtionalResult=false&isSchoolJob=0'
    Referer = 'https://www.lagou.com/jobs/list_'+keyword_url+'?city='+city_url+'=false&fromSearch=true&labelWords=&suginput='
              
    headers= {
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
            'Connection':'keep-alive',
            'Content-Length':'55',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie':cookie_index_page,
            #'Cookie':'user_trace_token=20180207113204-7744cd5f-0bb7-11e8-af98-5254005c3644; LGUID=20180207113204-7744d610-0bb7-11e8-af98-5254005c3644; X_HTTP_TOKEN=6c081ddd3140608e11f880fb052784d2; JSESSIONID=ABAAABAACDBABJBC8F7F250110B34C7B9653564A16E634F; _gat=1; PRE_UTM=m_cf_cpt_baidu_pc; PRE_HOST=bzclk.baidu.com; PRE_SITE=http%3A%2F%2Fbzclk.baidu.com%2Fadrc.php%3Ft%3D06KL00c00f7Ghk60yUKm0FNkUsasALVp00000PW4pNb00000xnSg-j.THL0oUhY1x60UWdBmy-bIfK15yFBm1NbnAc1nj0snjTvPHc0IHYYnD7KfHb4nWTkwWPDrjFanjfznjf3Pj0vPbNAPbnvPsK95gTqFhdWpyfqn101n1csPHnsPausThqbpyfqnHm0uHdCIZwsT1CEQLILIz4_myIEIi4WUvYE5LNYUNq1ULNzmvRqUNqWu-qWTZwxmh7GuZNxTAn0mLFW5HmsP1Tk%26tpl%3Dtpl_10085_15730_11224%26l%3D1500117464%26attach%3Dlocation%253D%2526linkName%253D%2525E6%2525A0%252587%2525E9%2525A2%252598%2526linkText%253D%2525E3%252580%252590%2525E6%25258B%252589%2525E5%25258B%2525BE%2525E7%2525BD%252591%2525E3%252580%252591%2525E5%2525AE%252598%2525E7%2525BD%252591-%2525E4%2525B8%252593%2525E6%2525B3%2525A8%2525E4%2525BA%252592%2525E8%252581%252594%2525E7%2525BD%252591%2525E8%252581%25258C%2525E4%2525B8%25259A%2525E6%25259C%2525BA%2526xp%253Did%28%252522m6c247d9c%252522%29%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FH2%25255B1%25255D%25252FA%25255B1%25255D%2526linkType%253D%2526checksum%253D220%26ie%3Dutf-8%26f%3D8%26tn%3Dbaidu%26wd%3D%25E6%258B%2589%25E5%258B%25BE%25E7%25BD%2591%26oq%3DPython%252520%2525E6%25258B%252589%2525E5%25258B%2525BE%2525E7%2525BD%252591%2525E8%252581%25258C%2525E4%2525BD%25258D%2525E6%25258F%25258F%2525E8%2525BF%2525B0%26rqlang%3Dcn%26inputT%3D3697%26bs%3DPython%2520%25E6%258B%2589%25E5%258B%25BE%25E7%25BD%2591%25E8%2581%258C%25E4%25BD%258D%25E6%258F%258F%25E8%25BF%25B0; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F%3Futm_source%3Dm_cf_cpt_baidu_pc; _putrc=1EB89C8FC3968DCC; login=true; unick=%E8%8A%AE%E6%96%87%E8%B1%AA; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; gate_login_token=6b16eae67cd5a417f9e418767162e334fca4c554cc867f69; TG-TRACK-CODE=index_search; _gid=GA1.2.1095870113.1517974326; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1517974326,1517985314,1518017461; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1518017468; _ga=GA1.2.775610052.1517974326; LGSID=20180207233059-e5e0da28-0c1b-11e8-be26-525400f775ce; LGRID=20180207233106-ea2630fe-0c1b-11e8-af9a-5254005c3644; SEARCH_ID=3745f989f98c49929b7343aba726102d; index_location_city=%E5%8C%97%E4%BA%AC',
            'Host':'www.lagou.com',
            'Origin':'https://www.lagou.com',
            'Referer':Referer,
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'X-Anit-Forge-Code':'0',
            'X-Anit-Forge-Token':'None',
            'X-Requested-With':'XMLHttpRequest'
            }

    pagenum = GetPagnum(url,keyword,headers)
    return url,headers,pagenum

def parse_all_page(url,keyword,headers,city,pagenum):
    keyword_url = parseString(keyword)
    city_url = parseString(city)
    _num = 1

    for i in range(273,pagenum):
        time.sleep(16 + random.uniform(0,5))
        if i == 0: # 第一页和后边的页data不一样
            data = {'first': 'true','pn': '1', 'kd': keyword} 
            html = requests.post(url,headers = headers,data = data)
        else: 
            data = {'first': 'false','pn': (i+1), 'kd': keyword} 
            html = requests.post(url,headers = headers,data = data)
        
        try:
            pageContent = json.loads(html.text)
            ## 为了获取职位描述，需要获取每一个公司提供的职位编码
            companyCount = len(pageContent['content']["positionResult"]['result'])
            positionID = [pageContent['content']['positionResult']['result'][i]['positionId']
            for i in range(companyCount)]
            print(positionID)

        except:
            continue
    
        
        for eachID in positionID:
            time.sleep(5 + random.uniform(0,2))
            Referer2 = 'https://www.lagou.com/jobs/list_'+keyword_url+'?city='+city_url+'+&cl=false&fromSearch=true&labelWords=&suginput='
            headers2= {
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding':'gzip, deflate, sdch, br',
                'Accept-Language':'zh-CN,zh;q=0.8',
                'Cache-Control':'max-age=0',
                'Connection':'keep-alive',
                'Cookie':cookie_each_page,
                #'Cookie':'user_trace_token=20180207113204-7744cd5f-0bb7-11e8-af98-5254005c3644; LGUID=20180207113204-7744d610-0bb7-11e8-af98-5254005c3644; X_HTTP_TOKEN=6c081ddd3140608e11f880fb052784d2; JSESSIONID=ABAAABAACDBABJBC8F7F250110B34C7B9653564A16E634F; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_%25E6%2595%25B0%25E6%258D%25AE%25E6%258C%2596%25E6%258E%2598%3Fpx%3Ddefault%26city%3D%25E5%258C%2597%25E4%25BA%25AC; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2F3939924.html; _putrc=1EB89C8FC3968DCC; login=true; unick=%E8%8A%AE%E6%96%87%E8%B1%AA; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; gate_login_token=9d4ffaabc6a5c3220a32d32579c6fed58b26cd0d7e392617; TG-TRACK-CODE=index_search; SEARCH_ID=2492311f7e994cf7a79fd1f1eadb2d3e; index_location_city=%E5%8C%97%E4%BA%AC; _gid=GA1.2.1095870113.1517974326; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1517974326,1517985314; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1518005921; _ga=GA1.2.775610052.1517974326; LGSID=20180207200747-8299bfc1-0bff-11e8-af98-5254005c3644; LGRID=20180207201839-078da2db-0c01-11e8-bde7-525400f775ce',
                'Host':'www.lagou.com',
                'Referer':Referer2,
                'Upgrade-Insecure-Requests':'1',
                'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                    }
            url2 = 'https://www.lagou.com/jobs/' + str(eachID) +'.html'
            try:
                 html2 = requests.get(url2,headers = headers2)
                 soup = BeautifulSoup(html2.text,'lxml')
            except:
                continue

            print('正在爬第 %s 个公司的岗位信息' % _num)
            print(url2)
            try:
                company = soup.findAll('h2',
                        {'class':'fl'})[0].get_text().strip().split('\n')[0]
                print('公司名称',company)
            except:
                company = ''
            try:
                position = soup.findAll('div',
                        {'class':'job-name'})[0].find('span').get_text()
                print('岗位',position)
            except:
                position = ''
            try: # 这个是爬取的核心内容
                description = soup.findAll('dd',{'class':
                    'job_bt'})[0].get_text().strip().replace('\r','').replace('\n','') 
                print('描述','\n',description)
            except:
                description = ''
            try:
                edu = soup.findAll('dd',{'class':
                    'job_request'})[0].find('p').get_text().replace('\n','').split('/')[3]
                print('学历','\n',edu)
            except:
                edu= ''
            try:
                salary = soup.findAll('dd',{'class':
                    'job_request'})[0].find('p').get_text().replace('\n','').split('/')[0]
                print('工资','\n',salary)
            except:
                salary = ''
            try:
                city_ = soup.findAll('dd',{'class':
                    'job_request'})[0].find('p').get_text().replace('\n','').split('/')[1]
                print('城市','\n',city_)
            except:
                city_ = ''
                
            _num += 1
            yield { 'source':'拉勾网',
                   'keyword':keyword,
                    'links':url2,
                    'city':city_,
                    'company':company,
                  'position':position,
                  'edu':edu,
                  'salary':salary,
                  'description':description,
                  }
           
           
            
def save_info_csv(content,count,fileName):
    '''
    保存数据到csv
    '''
    with open('D:\\workspace python\\statContest\\lagou\\' + fileName,'a',newline='',encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if count == 0:      
            writer.writerow(('来源','关键词','链接','城市','公司名称','岗位',
                             '学历','工资','岗位描述'))
            print('===========变量名全部写入=========')
            csvfile.close()
        else:
            writer.writerow([content['source'],content['keyword'],content['links'],content['city_'],
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
    mySql_.create_table('lagou1')
    
    keyword = '数据科学'
    cookie_index_page = 'user_trace_token=20170728152014-6582c8ba-9319-4806-a6ff-d0a1b8fd3df7; LGUID=20180208173649-96772d8d-0cb3-11e8-afaa-5254005c3644; WEBTJ-ID=2018-3-21101310-1624654df26143-011519c2875466-37624605-1327104-1624654df27857; _gat=1; PRE_UTM=m_cf_cpc_baidu_pc; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Fbaidu.php%3Fsc.af0000jT6JN_mhQrXDLoNr4XNbaHDQWu01zTOfAQpK_BhtYO07OGousk8b9cxYKf9tlygNk-_VTHIoHJsvrO7eB9x9-lN49ayIcrJhtq44mxs5tHVH6vUhiYjZ4LseXF7wRuqRQxB2YW_S5qdJ5Q2QN-3c_njae_3Y0iXBuCBUJLNupAT6.Db_NR2Ar5Od663rj6tJQrGvKD7ZZKNfYYmcgpIQC8xxKfYt_U_DY2yP5Qjo4mTT5QX1BsT8rZoG4XL6mEukmryZZjzL4XNPIIhExzSPxWYtpSgj4qrZul3IhOj4e_r1dsSEM9tOZjlOQjEoONsSxH9vX8Zxl3x5u9vN3ISki_nYQZZWvNe-0.U1Yk0ZDqs2v4VnL3FHcsdIjA80KspynqnfKY5TaV8UHPSaRznPgfko60pyYqnWcd0ATqmhNsT100Iybqmh7GuZR0TA-b5HD0mv-b5Hn3nsKVIjYknjDLg1DsnH-xnH0zndt1njDdg1nvnjD0pvbqn0KzIjYknWm0uy-b5HDYnW7xnHndPHKxnWDknjIxnH6dPWKxnHTsnj7xnW04nWT0mhbqnW0Y0AdW5HTzn10zPHbsPNtLnWndPjfvPHFxnNtknjFxn0KkTA-b5H00TyPGujYs0ZFMIA7M5H00mycqn7ts0ANzu1Ys0ZKs5H00UMus5H08nj0snj0snj00Ugws5H00uAwETjYs0ZFJ5H00uANv5gKW0AuY5H00TA6qn0KET1Ys0AFL5HDs0A4Y5H00TLCq0ZwdT1Ykn1R4PWb4n1bYP1m1PHTsn1TdPsKzug7Y5HDdnWDdrH61rjDdrHb0Tv-b5y7BPjFBnHT1nj0snjFBnWT0mLPV5H6YnRm4f1-anjbzf1FKPjn0mynqnfKsUWYs0Z7VIjYs0Z7VT1Ys0ZGY5H00UyPxuMFEUHYsg1Kxn7tsg100uA78IyF-gLK_my4GuZnqn7tsg1Kxn1D4rHcsg100TA7Ygvu_myTqn0Kbmv-b5H00ugwGujYVnfK9TLKWm1Ys0ZNspy4Wm1Ys0Z7VuWYs0AuWIgfqn0KhXh6qn0Khmgfqn0KlTAkdT1Ys0A7buhk9u1Yk0Akhm1Ys0APzm1YYnHD1P0%26ck%3D8842.8.78.196.184.464.165.284%26shh%3Dwww.baidu.com%26us%3D1.0.1.0.1.301.0.101%26ie%3Dutf-8%26f%3D8%26tn%3Dbaidu%26wd%3D%25E6%258B%2589%25E5%258B%25BE%25E7%25BD%2591%2520%25E6%258B%259B%25E8%2581%2598%26rqlang%3Dcn%26sht%3Dbaidu%26bc%3D110101; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Flp%2Fhtml%2Fcommon.html%3Futm_source%3Dm_cf_cpc_baidu_pc%26m_kw%3Dbaidu_cpc_bj_e110f9_717631_%25E6%258B%2589%25E5%258B%25BE%25E7%25BD%2591%2B%25E6%258B%259B%25E8%2581%2598; _putrc=1EB89C8FC3968DCC; JSESSIONID=ABAAABAAAGFABEFD8D9706BD123D0ABA8E6723C921FFFEA; login=true; unick=%E8%8A%AE%E6%96%87%E8%B1%AA; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; gate_login_token=7e608213bfac45efbc691b1c2a81a6dcc843f949de401ca0; hideSliderBanner20180305WithTopBannerC=1; TG-TRACK-CODE=index_search; _gid=GA1.2.905753604.1521553315; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1521553315,1521598390; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1521598402; _ga=GA1.2.763059274.1518082612; LGSID=20180321101305-6403d68d-2cad-11e8-91d1-525400f775ce; LGRID=20180321101317-6b445e2f-2cad-11e8-b565-5254005c3644; SEARCH_ID=8ae5ba9c06dc4382afbeea054082ab35; index_location_city=%E5%8C%97%E4%BA%AC'
    cookie_each_page = 'user_trace_token=20170728152 014-6582c8ba-9319-4806-a6ff-d0a1b8fd3df7; LGUID=20180208173649-96772d8d-0cb3-11e8-afaa-5254005c3644; WEBTJ-ID=2018-3-21101310-1624654df26143-011519c2875466-37624605-1327104-1624654df27857; _gat=1; PRE_UTM=m_cf_cpc_baidu_pc; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Fbaidu.php%3Fsc.af0000jT6JN_mhQrXDLoNr4XNbaHDQWu01zTOfAQpK_BhtYO07OGousk8b9cxYKf9tlygNk-_VTHIoHJsvrO7eB9x9-lN49ayIcrJhtq44mxs5tHVH6vUhiYjZ4LseXF7wRuqRQxB2YW_S5qdJ5Q2QN-3c_njae_3Y0iXBuCBUJLNupAT6.Db_NR2Ar5Od663rj6tJQrGvKD7ZZKNfYYmcgpIQC8xxKfYt_U_DY2yP5Qjo4mTT5QX1BsT8rZoG4XL6mEukmryZZjzL4XNPIIhExzSPxWYtpSgj4qrZul3IhOj4e_r1dsSEM9tOZjlOQjEoONsSxH9vX8Zxl3x5u9vN3ISki_nYQZZWvNe-0.U1Yk0ZDqs2v4VnL3FHcsdIjA80KspynqnfKY5TaV8UHPSaRznPgfko60pyYqnWcd0ATqmhNsT100Iybqmh7GuZR0TA-b5HD0mv-b5Hn3nsKVIjYknjDLg1DsnH-xnH0zndt1njDdg1nvnjD0pvbqn0KzIjYknWm0uy-b5HDYnW7xnHndPHKxnWDknjIxnH6dPWKxnHTsnj7xnW04nWT0mhbqnW0Y0AdW5HTzn10zPHbsPNtLnWndPjfvPHFxnNtknjFxn0KkTA-b5H00TyPGujYs0ZFMIA7M5H00mycqn7ts0ANzu1Ys0ZKs5H00UMus5H08nj0snj0snj00Ugws5H00uAwETjYs0ZFJ5H00uANv5gKW0AuY5H00TA6qn0KET1Ys0AFL5HDs0A4Y5H00TLCq0ZwdT1Ykn1R4PWb4n1bYP1m1PHTsn1TdPsKzug7Y5HDdnWDdrH61rjDdrHb0Tv-b5y7BPjFBnHT1nj0snjFBnWT0mLPV5H6YnRm4f1-anjbzf1FKPjn0mynqnfKsUWYs0Z7VIjYs0Z7VT1Ys0ZGY5H00UyPxuMFEUHYsg1Kxn7tsg100uA78IyF-gLK_my4GuZnqn7tsg1Kxn1D4rHcsg100TA7Ygvu_myTqn0Kbmv-b5H00ugwGujYVnfK9TLKWm1Ys0ZNspy4Wm1Ys0Z7VuWYs0AuWIgfqn0KhXh6qn0Khmgfqn0KlTAkdT1Ys0A7buhk9u1Yk0Akhm1Ys0APzm1YYnHD1P0%26ck%3D8842.8.78.196.184.464.165.284%26shh%3Dwww.baidu.com%26us%3D1.0.1.0.1.301.0.101%26ie%3Dutf-8%26f%3D8%26tn%3Dbaidu%26wd%3D%25E6%258B%2589%25E5%258B%25BE%25E7%25BD%2591%2520%25E6%258B%259B%25E8%2581%2598%26rqlang%3Dcn%26sht%3Dbaidu%26bc%3D110101; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Flp%2Fhtml%2Fcommon.html%3Futm_source%3Dm_cf_cpc_baidu_pc%26m_kw%3Dbaidu_cpc_bj_e110f9_717631_%25E6%258B%2589%25E5%258B%25BE%25E7%25BD%2591%2B%25E6%258B%259B%25E8%2581%2598; _putrc=1EB89C8FC3968DCC; JSESSIONID=ABAAABAAAGFABEFD8D9706BD123D0ABA8E6723C921FFFEA; login=true; unick=%E8%8A%AE%E6%96%87%E8%B1%AA; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; gate_login_token=7e608213bfac45efbc691b1c2a81a6dcc843f949de401ca0; hideSliderBanner20180305WithTopBannerC=1; SEARCH_ID=8ae5ba9c06dc4382afbeea054082ab35; index_location_city=%E5%8C%97%E4%BA%AC; TG-TRACK-CODE=search_code; _gid=GA1.2.905753604.1521553315; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1521553315,1521598390; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1521598435; _ga=GA1.2.763059274.1518082612; LGSID=20180321101305-6403d68d-2cad-11e8-91d1-525400f775ce; LGRID=20180321101350-7ea1128a-2cad-11e8-91d2-525400f775ce'
    #count = 0
    #save_info_csv(count,count,fileName = 'lagou-shujukexue.csv')
    count = 4102
    city_list = ['全国']
    for city in city_list:
        url_,headers_,pagenum_ = process_page(keyword,city)
        for content in parse_all_page(url_,keyword,headers_,city,pagenum_):
            print(content)
            mySql_.innsert_data(content,'lagou1')
            #save_info_csv(content,count,fileName = 'lagou-shujukexue.csv')
            myfile = open("findWhere.txt", 'a')
            print('现在已经爬取第 %d||%d 个公司' % (count, pagenum_ * 15))
            print('现在已经爬取第 %d||%d 个公司' % (count,pagenum_ * 15),file = myfile)
            count += 1

# 大数据 2745 数据挖掘 1114 机器学习462 + 346 数据分析 2865 数据科学 4102

