# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 22:31:11 2018

@author: Rui Wenhao
@Copyright: Rui Wenhao, All rights reserved
@Mail:rui_wenhao@cueb.edu.cn
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

os.chdir('D:\\workspace python\\statContest\\')

df = pd.read_csv('clean_total.csv',encoding = 'gbk')

df = df[~df.工资.isin(['面议','未知'])]


## 工资统计
df['工资'] = df['工资'].apply(float)
df = df.loc[(df.工资 < 100000) & (df.工资 > 3000)]

## 取对数降低y的尺度
df['log工资'] = np.log(1 + df.工资)
y = df['log工资']

from sklearn.feature_extraction.text import TfidfVectorizer

tf = TfidfVectorizer(max_features = 400)
X = tf.fit_transform(df['岗位要求'])


## 划分训练集、测试集
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42)

from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import time

y_train.index = list(range(y_train.shape[0]))

X_t, X_v, y_t, y_v = train_test_split(
            X_train, y_train, test_size=0.3, random_state=227)

def get_ntree():  
    rmse_t_total, rmse_v_total = [], []
    for ntree in range(10, 500, 10):
        rf_base = RandomForestRegressor(n_estimators = ntree,criterion='mse',
                                        random_state=1234)
        print('此时 ntree = %s' % ntree)
        rf_base.fit(X_t, y_t)
        y_t_pre = rf_base.predict(X_t)
        y_v_pre = rf_base.predict(X_v)
        rmse_t_each = np.sqrt(mean_squared_error(y_t, y_t_pre))
        rmse_v_each = np.sqrt(mean_squared_error(y_v, y_v_pre))
        rmse_t_total.append(rmse_t_each)
        rmse_v_total.append(rmse_v_each)
        myfile = open('D:\\workspace python\\statContest\\save\\' + 'rfbbase_rmse_t.txt',
                      'a', encoding='utf-8')
        print(rmse_t_each,',',rmse_v_each,file = myfile)
        myfile.close()
    return rmse_t_total,rmse_v_total

rmse_t_total,rmse_v_total = get_ntree()

def tune_params(): 
    params_lst = []
    rmse_t_total, rmse_v_total = [], []
    for max_features in ['auto','log2']:
        for max_depth in range(6,15):
            rf_base = RandomForestRegressor(n_estimators = 120,criterion='mse',
                                random_state=1234,max_features = max_features,
                                max_depth= max_depth)
            _params = { 'max_features':max_features,
                'max_depth':max_depth
                    }
            rf_base.fit(X_t, y_t)
            y_t_pre = rf_base.predict(X_t)
            y_v_pre = rf_base.predict(X_v)
            rmse_t_each = np.sqrt(mean_squared_error(y_t, y_t_pre))
            rmse_v_each = np.sqrt(mean_squared_error(y_v, y_v_pre))
            rmse_t_total.append(rmse_t_each)
            rmse_v_total.append(rmse_v_each)
            print(_params)
            myfile1 = open('D:\\workspace python\\statContest\\save\\' + 'rfbase2_saveparams_rmse_0412.txt',
                          'a', encoding='utf-8')
            print(_params['max_features'],_params['max_depth'],file = myfile1)   
            params_lst.append([_params['max_features'],_params['max_depth']])
            myfile1.close()
            print(rmse_t_each,rmse_v_each)
            myfile = open('D:\\workspace python\\statContest\\save\\' + 'rfbase2_tunparms_rmse_0412.txt',
                          'a', encoding='utf-8')
            print(rmse_t_each,',',rmse_v_each,file = myfile)
            myfile.close()                   
    return params_lst,rmse_t_total,rmse_v_total


params_lst,rmse_t_total2,rmse_v_total2 = tune_params()

## 随机森林大概120棵树就够了
# rmse_t_total,rmse_v_total
plt.plot(range(10, 500, 10), rmse_t_total,
         color='blue', marker='o',
         markersize=5, label='training accuracy')
plt.plot(range(10, 500, 10), rmse_v_total,
         color='green', linestyle='--',
         marker='s', markersize=5,
         label='validation accracy')
plt.grid()
plt.xlabel('Number of trees')
plt.ylabel('RMSE')
plt.legend(loc='top right')
## 下边自己调整
plt.ylim([0.25, 0.7])
plt.show()


## 调参绘图
## auto 14
plt.plot(range(18), rmse_t_total2,
         color='blue', marker='o',
         markersize=1, label='training accuracy')
plt.plot(range(18), rmse_v_total2,
         color='green', linestyle='--',
         marker='s', markersize=1,
         label='validation accracy')
plt.grid()
plt.xlabel('Params')
plt.ylabel('RMSE')
plt.legend(loc='top right')

rmse_v_total2.index(min(rmse_v_total2)) ## 第8组最小
params_lst[8]