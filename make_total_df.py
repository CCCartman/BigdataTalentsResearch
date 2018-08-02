# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 14:51:00 2018

@author: Rui Wenhao
@Copyright: Rui Wenhao, All rights reserved
@Mail:rui_wenhao@cueb.edu.cn
"""

import pandas as pd
import os

df = pd.read_csv('zhilian.csv',header = None,
 names = ['来源','关键词','链接','城市','公司名称','岗位',
             '学历','工资','岗位描述'],encoding = 'utf-8')

df2 = pd.read_csv('lagou.csv',header = None,
 names = ['来源','关键词','链接','城市','公司名称','岗位',
             '学历','工资','岗位描述'],encoding = 'utf-8')

df3 = pd.read_csv('dajie.csv',header = None,
 names = ['来源','关键词','链接','城市','公司名称','岗位',
             '学历','工资','岗位描述'],encoding = 'utf-8')

df4 = pd.read_csv('liepin.csv',header = None,
 names = ['来源','关键词','链接','城市','公司名称','岗位',
             '学历','工资','岗位描述'],encoding = 'utf-8')

df5 = pd.read_csv('51job.csv',header = None,
 names = ['来源','关键词','链接','城市','公司名称','岗位',
             '学历','工资','岗位描述'],encoding = 'utf-8')

pd.concat([df,df2,df3,df4,df5],axis = 0).to_csv('total.csv',index = False)
