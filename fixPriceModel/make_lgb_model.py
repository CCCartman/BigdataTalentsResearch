# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 11:37:25 2018

@author: Rui Wenhao
@Copyright: Rui Wenhao, All rights reserved
@Mail:rui_wenhao@cueb.edu.cn
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import KFold
from lightgbm.sklearn import LGBMRegressor
from sklearn.metrics import mean_squared_error
import time
os.chdir('D:\\workspace python\\statContest\\')

def get_data():
    df = pd.read_csv('clean_total.csv',encoding = 'gbk')
    df = df[~df.工资.isin(['面议','未知'])]

    ## 工资统计
    df['工资'] = df['工资'].apply(float)
    df = df.loc[(df.工资 < 100000) & (df.工资 > 3000)]
    ## 取对数降低y的尺度
    df['log工资'] = np.log(1 + df.工资)
    y = df['log工资']
    tf = TfidfVectorizer(max_features=400)
    X = tf.fit_transform(df['岗位要求'])
    return X,y


def split_data():
    X, y = get_data()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42)
    y_train.index = list(range(y_train.shape[0]))
    return X_train,X_test,y_train,y_test


def split_data2():
    X_train, X_test, y_train, y_test = split_data()
    X_t, X_v, y_t, y_v = train_test_split(
                X_train, y_train, test_size=0.25, random_state=227)
    return X_t, X_v, y_t, y_v

X_t, X_v, y_t, y_v = split_data2()

def get_ntree():  
    rmse_t_total, rmse_v_total = [], []
    for ntree in range(10, 500, 10):
        lgb_base = LGBMRegressor(n_estimators = ntree,objective = 'regression',
                      random_state=1234,n_jobs = 2,colsample_bytree=0.8, reg_alpha=1,
                      max_depth = 10, subsample = 0.8)

        print('此时 ntree = %s' % ntree)
        lgb_base.fit(X_t, y_t)
        y_t_pre = lgb_base.predict(X_t)
        y_v_pre = lgb_base.predict(X_v)
        rmse_t_each = np.sqrt(mean_squared_error(y_t, y_t_pre))
        rmse_v_each = np.sqrt(mean_squared_error(y_v, y_v_pre))
        rmse_t_total.append(rmse_t_each)
        rmse_v_total.append(rmse_v_each)
        myfile = open('D:\\workspace python\\statContest\\save\\' + 'lgbbase2_rmse_0412.txt',
                      'a', encoding='utf-8')
        print(rmse_t_each,',',rmse_v_each,file = myfile)
        myfile.close()
    return rmse_t_total,rmse_v_total


rmse_t_total,rmse_v_total = get_ntree()

def tune_params():  
    rmse_t_total, rmse_v_total = [], []
    for max_depth in range(6,11):
        for subsample in [0.6,0.7,0.8]:
            for colsample_bytree in [0.6,0.7,0.8]:
                for reg_alpha in [0.1,1,10]:
                    lgb_base = LGBMRegressor(n_estimators = 150,objective = 'regression',
                                      random_state=1234,n_jobs = 3,colsample_bytree=colsample_bytree, 
                                      reg_alpha=reg_alpha,
                                      max_depth = max_depth, subsample = subsample)
                    _params = { 'max_depth':max_depth,
                        'subsample':subsample,
                            'colsample_bytree':colsample_bytree,
                                'reg_alpha':reg_alpha,
                            }
                    lgb_base.fit(X_t, y_t)
                    y_t_pre = lgb_base.predict(X_t)
                    y_v_pre = lgb_base.predict(X_v)
                    rmse_t_each = np.sqrt(mean_squared_error(y_t, y_t_pre))
                    rmse_v_each = np.sqrt(mean_squared_error(y_v, y_v_pre))
                    rmse_t_total.append(rmse_t_each)
                    rmse_v_total.append(rmse_v_each)
                    print(_params)
                    myfile1 = open('D:\\workspace python\\statContest\\save\\' + 'lgbbase2_saveparams_rmse_0412.txt',
                                  'a', encoding='utf-8')
                    print(_params['max_depth'],_params['subsample'],_params['colsample_bytree'],
                          _params['reg_alpha'],file = myfile1)
                    
                    myfile1.close()
                    print(rmse_t_each,rmse_v_each)
                    myfile = open('D:\\workspace python\\statContest\\save\\' + 'lgbbase2_tunparms_rmse_0412.txt',
                                  'a', encoding='utf-8')
                    print(rmse_t_each,',',rmse_v_each,file = myfile)
                    myfile.close()                   
    return rmse_t_total,rmse_v_total


rmse_t_total2,rmse_v_total2 = tune_params()

'''
file =  open('D:\\workspace python\\statContest\\save\\' + 'lgbbase_rmse_t'.txt',
                      'r', encoding='utf-8')
rmse_t_total,rmse_v_total = [],[]
for line in file:
    line = line.split(',')
    rmse_t_total.append(line[0])
    rmse_v_total.append(line[1])
file.close()

rmse_t_total = list(map(float,[i.rstrip() for i in rmse_t_total]))
rmse_v_total = list(map(float,[i.rstrip() for i in rmse_v_total]))
'''
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


## lgb 大约150棵树
# rmse_t_total,rmse_v_total
plt.plot(range(135), rmse_t_total2,
         color='blue', marker='o',
         markersize=1, label='training accuracy')
plt.plot(range(135), rmse_v_total2,
         color='green', linestyle='--',
         marker='s', markersize=1,
         label='validation accracy')
plt.grid()
plt.xlabel('Number of trees')
plt.ylabel('RMSE')
plt.legend(loc='top right')
## 下边自己调整
plt.ylim([0.25, 0.7])
plt.show()


file =  open('D:\\workspace python\\statContest\\save\\' + 'lgbbase2_saveparams_rmse_0412.txt',
                      'r', encoding='utf-8')
params_lst = []
for line in file:
    line = line.strip().split()
    params_lst.append(line)
file.close()

rmse_v_total2.index(min(rmse_v_total2)) # 第127组最小

'''
lgb_best = LGBMRegressor(n_estimators = 150,objective = 'regression',
                                      random_state=1234,n_jobs = 3,colsample_bytree=0.6, 
                                      reg_alpha=1,
                                      max_depth = 10, subsample = 0.8)
'''