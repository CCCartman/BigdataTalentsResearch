# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 18:48:57 2018

@author: Rui Wenhao
@Copyright: Rui Wenhao, All rights reserved
@Mail:rui_wenhao@cueb.edu.cn
"""

import csv

def save_info_csv(content,count,savePath,fileName,webName):
    '''
    保存数据到csv
    '''
    with open(savePath + fileName,'a',newline='',encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if count == 0:      
            writer.writerow(('来源','关键词','链接','城市','公司名称','岗位',
                             '学历','工资','岗位描述'))
            print('===========变量名全部写入=========')
            csvfile.close()
        else:
            writer.writerow(['智联招聘',keyword,content['links'],content['city'],
                            content['company'],content['position'],
                            content['edu'],content['salary'],
                            content['description']])
            print('===========写了一行内容===========')
            csvfile.close()     