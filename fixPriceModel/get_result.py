# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 23:38:27 2018

@author: Rui Wenhao
@Copyright: Rui Wenhao, All rights reserved
@Mail:rui_wenhao@cueb.edu.cn
"""
import os
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from xgboost.sklearn import XGBRegressor
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import matplotlib.pyplot as plt
os.chdir('D:\\workspace python\\statContest\\')


y_test = pd.read_csv('y_test.csv')
res1 = pd.read_csv('res_model1_test.csv')
res2 = pd.read_csv('res_model2_test.csv')

res_total = pd.concat([res1,res2,y_test],axis = 1)
res_total.columns = ['model1', 'model2', 'logy']
res_total['y_true'] = np.exp(res_total.logy) 

res_total['y_true_low'] = res_total['y_true'] - np.std(res_total.y_true)
res_total['y_true_high'] = res_total['y_true'] + np.std(res_total.y_true)

res_total['logy_pre'] = res_total.iloc[:,:2].mean(axis = 1)
res_total['y_pre'] = np.exp(res_total['logy_pre'])



logy_low = res_total.logy.values - np.std(res_total.logy)
logy_high = res_total.logy.values + np.std(res_total.logy)



count = 0
for i in range(res_total.shape[0]):
    if res_total.logy_pre.values[i] > logy_low[i] and res_total.logy_pre.values[i] < logy_high[i]:
        count += 1

count / res_total.shape[0] # 80%的样本预测误差在一个标准差内

np.sqrt(mean_squared_error(res_total['logy_pre'],y_test))

########## 测试一下
def model1_test(X,n = y_test.shape[0],filepath = 'D:\\workspace python\\statContest\\save\\model\\'):
    res = np.zeros(30 * n).reshape(30,n)
    for i in range(30):
        print('模型 %s 正在计算中' % i)
        model = joblib.load(filepath + 'xgb_randparams_%s.pkl'%i)
        res[i] = model.predict(X)
    res = res.mean(axis = 0)
    return res

def model2_test(X,n = y_test.shape[0],filepath = 'D:\\workspace python\\statContest\\save\\model\\'):
    res = np.zeros(3 * n).reshape(3,n)
    xgb = joblib.load(filepath + 'xgb_best.pkl')
    lgb = joblib.load(filepath + 'lgb_best.pkl')
    rf = joblib.load(filepath + 'rf_best.pkl')
    clfs = [xgb,lgb,rf]
    for i,clf in enumerate(clfs):
        print('模型 %s 正在计算中' % clf)
        res[i] = clf.predict(X)
    res =  0.3 * res[0] + 0.5 * res[1] + 0.2 * res[2] 
    return res

output = open('D:\\workspace python\\statContest\\save\\' + 'tf.pkl','rb') 
tf = pickle.load(output)
output.close()

mytest = np.array(['硕士 统计学 数据挖掘 sql python'])
   
x_test2 = tf.transform(mytest)

res_out_m1 = model1_test(X = x_test2 ,n = x_test2.shape[0],filepath = 'D:\\workspace python\\statContest\\save\\model\\')
res_out_m2 = model2_test(X = x_test2 ,n = x_test2.shape[0],filepath = 'D:\\workspace python\\statContest\\save\\model\\')   

np.exp((res_out_m1 + res_out_m2) / 2)