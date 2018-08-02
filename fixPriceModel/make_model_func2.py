# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 21:19:40 2018

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
from xgboost.sklearn import XGBRegressor
from lightgbm.sklearn import LGBMRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.externals import joblib
import time

xgb_best = XGBRegressor(objective='reg:linear',n_estimators=120,
        random_state=1234,silent = 0,booster = 'gbtree',subsample = 0.8,
        colsample_bytree = 0.8,reg_alpha = 1,
        reg_lambda = 0,learning_rate = 0.1,
        max_depth = 6, eval_metric='rmse')


lgb_best = LGBMRegressor(n_estimators = 150,objective = 'regression',
                      random_state=1234,n_jobs = 2,colsample_bytree=0.8, reg_alpha=1,
                      max_depth = 10, subsample = 0.8)

rf_best = RandomForestRegressor(n_estimators = 120,criterion='mse',
                                        random_state=1234,max_features = 'sqrt',
                                        max_depth= 10)


os.chdir('D:\\workspace python\\statContest\\')

df = pd.read_csv('clean_total.csv',encoding = 'gbk')
df = df[~df.工资.isin(['面议','未知'])]
df['工资'] = df['工资'].apply(float)
df = df.loc[(df.工资 < 100000) & (df.工资 > 3000)]
df['log工资'] = np.log(1 + df.工资)
y = df['log工资']

tf = TfidfVectorizer(max_features = 400)

X = tf.fit_transform(df['岗位要求'])
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42)

X_t, X_v, y_t, y_v = train_test_split(
            X_train, y_train, test_size=0.3, random_state=227)

joblib.dump(X,'X.pkl')
joblib.dump(X_train,'X_train_seed42.pkl')
joblib.dump(X_test,'X_test_seed42.pkl')
joblib.dump(y_train,'y_train_seed42.pkl')
joblib.dump(y_test,'y_test_seed42.pkl')

joblib.dump(X_t,'X_train_seed227.pkl')
joblib.dump(X_v,'X_test_seed227.pkl')
joblib.dump(y_t,'y_train_seed227.pkl')
joblib.dump(y_v,'y_test_seed227.pkl')



def fit_model():
    for clf in [xgb_best,lgb_best,rf_best]:
        start = time.time()
        print('正在训练模型  %s' %clf)
        clf.fit(X_t,y_t)
        end = time.time()
        print(end - start,'seconds')
        


def save_model(filepath = 'D:\\workspace python\\statContest\\save\\model\\'):
    os.chdir(filepath)
    names_ = ['xgb_best','lgb_best','rf_best']
    for i,clf in enumerate([xgb_best,lgb_best,rf_best]):
        start = time.time()
        print('正在保存模型  %s' %clf)
        joblib.dump(clf,'%s.pkl'%names_[i])
        end = time.time()
        print(end - start,'seconds')

save_model(filepath = 'D:\\workspace python\\statContest\\save\\model\\')


def model2_test(X = X_test,n = y_test.shape[0],filepath = 'D:\\workspace python\\statContest\\save\\model\\'):
    res = np.zeros(3 * n).reshape(3,n)
    xgb = joblib.load(filepath + 'xgb_best.pkl')
    lgb = joblib.load(filepath + 'lgb_best.pkl')
    rf = joblib.load(filepath + 'rf_best.pkl')
    clfs = [xgb,lgb,rf]
    for i,clf in enumerate(clfs):
        print('模型 %s 正在计算中' % clf)
        res[i] = clf.predict(X)
    return res



res_m2_v = model2_test(X = X_v,n = y_v.shape[0],filepath = 'D:\\workspace python\\statContest\\save\\model\\')
res_m2_v_df = pd.DataFrame(res_m2_v.T,columns = ['xgb','lgb','rf'])
res_m2_v_df['y_v'] = y_v.values

res_m2_v = pd.DataFrame(res_m2_v,columns = ['model2']).to_csv('res_model2_test.csv',index = False)

mean_squared_error(res_m2_v_df.xgb,res_m2_v_df.y_v)
mean_squared_error(res_m2_v_df.lgb,res_m2_v_df.y_v)
mean_squared_error(res_m2_v_df.rf,res_m2_v_df.y_v)

mse_lst = []
tune_lst = []
for i in np.arange(0.3,1,0.1):
    for j in np.arange(0.3,1,0.1):
        k = 1 - i -j
        if k > 0 :
            res_m2_v_df['sum_'] = i*res_m2_v_df.xgb + j*res_m2_v_df.lgb + k*res_m2_v_df.rf
            print(mean_squared_error(res_m2_v_df['sum_'],res_m2_v_df.y_v))
            print(i,j,k)
            mse_lst.append(mean_squared_error(res_m2_v_df['sum_'],res_m2_v_df.y_v))
            tune_lst.append((i,j,k))

plt.plot(range(len(mse_lst)),mse_lst,
         color = 'blue',marker = 'o',
         markersize = 5,label = 'training accuracy')   
     
tune_lst[26]   
np.min(mse_lst) + np.std(mse_lst)

## 根据一倍标准差原则 3 5 2
     
os.chdir('D:\\workspace python\\statContest\\')
res2 = model2_test(X = X_test,n = y_test.shape[0],filepath = 'D:\\workspace python\\statContest\\save\\model\\')
res2 = 0.3 * res2[0] + 0.5 * res2[1] + 0.2 * res2[2] 

pd.DataFrame(res2,columns = ['model2']).to_csv('res_model2_test.csv',index = False)
y_test.to_csv('y_test.csv',index = False) 


