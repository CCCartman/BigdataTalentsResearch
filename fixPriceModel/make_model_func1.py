# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 16:27:03 2018

@author: Rui Wenhao
@Copyright: Rui Wenhao, All rights reserved
@Mail:rui_wenhao@cueb.edu.cn
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import pickle
os.chdir('D:\\workspace python\\statContest\\')

df = pd.read_csv('clean_total.csv',encoding = 'gbk')

## 去掉工资面议和未知
df = df[~df.工资.isin(['面议','未知'])]

## 岗位要求词汇长度直方图
df.岗位要求.apply(lambda x:len(x.split())).hist()

df.岗位要求.apply(lambda x:len(x.split())).describe() # 最长285 最短8

## 工资统计
df['工资'] = df['工资'].apply(float)
df['工资'].describe()

df = df.loc[(df.工资 < 100000) & (df.工资 > 3000)]
df.工资.hist()

## 取对数降低y的尺度
df['log工资'] = np.log(1 + df.工资)
y = df['log工资']

## 建模
### 特征工程
from sklearn.feature_extraction.text import TfidfVectorizer  
from sklearn.feature_extraction.text import CountVectorizer 

tf = TfidfVectorizer(max_features = 400)
X = tf.fit_transform(df['岗位要求'])

## 划分训练集、测试集
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42)

y_train.index = list(range(y_train.shape[0]))

output = open('D:\\workspace python\\statContest\\save\\' + 'tf.pkl','wb') 
pickle.dump(tf,output)
output.close()

from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import KFold  
from xgboost.sklearn import XGBRegressor
from sklearn.metrics import mean_squared_error
import time
import random      
        
def get_cv(y,n_splits = 5,random_state = 42):
    kf = KFold(n_splits=n_splits,shuffle=True,random_state = random_state)  
    kf = kf.split(y) 
    for train,test in kf:
        yield train,test
        

## 先确定n_estimators

def get_ntree():
    rmse_t_total,rmse_v_total = [],[]
    for ntree in range(10,500,10):
        xgb_base = XGBRegressor(objective='reg:linear',n_estimators=ntree,random_state=1234,
                              silent = 0,booster = 'gbtree',
                              eval_metric='rmse')
        rmse_t_1,rmse_v_1 = [],[]
        print('此时 ntree = %s' % ntree)
        for train,test in get_cv(y = y_train,n_splits = 5,random_state = 42):
            X_t,y_t = X_train[train],y_train[train]
            X_v,y_v = X_train[test],y_train[test]
            xgb_base.fit(X_t,y_t)
            y_t_pre = xgb_base.predict(X_t)
            y_v_pre = xgb_base.predict(X_v)
            rmse_t_each = np.sqrt(mean_squared_error(y_t,y_t_pre))
            rmse_v_each = np.sqrt(mean_squared_error(y_v,y_v_pre))
            rmse_t_1.append(rmse_t_each)
            rmse_v_1.append(rmse_v_each)
        rmse_t = np.mean(rmse_t_1)
        rmse_v = np.mean(rmse_v_1)
        rmse_t_total.append(rmse_t)
        rmse_v_total.append(rmse_v)
    
    return rmse_t_total,rmse_v_total

rmse_t_total,rmse_v_total = get_ntree()

with open('D:\\workspace python\\statContest\\save\\' + 'xgbbase_rmse_t.txt','a',encoding = 'utf-8') as f:
    for num in rmse_t_total:
        f.write(str(num))
        f.write('\n')
        
with open('D:\\workspace python\\statContest\\save\\' + 'xgbbase_rmse_v.txt','a',encoding = 'utf-8') as f:
    for num in rmse_v_total:
        f.write(str(num))
        f.write('\n')

#rmse_t_total,rmse_v_total
plt.plot(range(10,500,10),rmse_t_total,
         color = 'blue',marker = 'o',
         markersize = 5,label = 'training accuracy')        
plt.plot(range(10,500,10),rmse_v_total,
         color = 'green',linestyle = '--',
         marker = 's',markersize = 5,
         label = 'validation accracy')        
plt.grid()
plt.xlabel('Number of trees')
plt.ylabel('RMSE')
plt.legend(loc = 'top right')
plt.ylim([0.25,0.7])
plt.show()        

### tree的个数定为 250   

def get_params(i):
    
    random.seed(i)
    random_state = i
    reg_alpha = [j for j in range(1,6)]
    reg_lambda = [j for j in range(1,6)]
    learning_rate = [j/100 for j in range(1,11)]
    max_depth = [6,7,8,9,10]
    subsample = [0.7,0.8,0.9]
    colsample_bytree= [0.7,0.8,0.9]   
    random.shuffle(reg_alpha)
    random.shuffle(reg_lambda)
    random.shuffle(learning_rate)
    random.shuffle(max_depth)
    random.shuffle(subsample)
    random.shuffle(colsample_bytree)
    
    params = {
            'objective':'reg:linear',
            'n_estimators':250,
            'silent' : 0,
            'booster' :'gbtree',
            'eval_metric' :'rmse',
            'random_state' : random_state ,
            'reg_alpha' :reg_alpha[0],
            'reg_lambda':reg_lambda[0],
            'learning_rate' :learning_rate[0],
            'max_depth':max_depth[0],
            'subsample':subsample[0],
            'colsample_bytree':colsample_bytree[0]     
            }
    return params


from sklearn.externals import joblib
def xgb_bagging(savepath = 'D:\\workspace python\\statContest\\save\\model\\'):
    os.chdir(savepath)
    bag_v_rmse_0 = []
    bag_t_rmse_0 = []
    i = 0
    while i < 30:
        print('模型%s正在训练'%i)
        start = time.time()
        xgb_randparams = XGBRegressor(**get_params(random.choice(list(range(1234)))),n_jobs = 2)  
        bag_v_rmse_1 = []
        bag_t_rmse_1 = []
        for train,test in get_cv(y = y_train,n_splits = 5,random_state = 42):
            X_t,y_t = X_train[train],y_train[train]
            X_v,y_v = X_train[test],y_train[test]
            xgb_randparams.fit(X_t,y_t)
            y_t_pre = xgb_randparams.predict(X_t)
            y_v_pre = xgb_randparams.predict(X_v)
            bag_t_rmse_1.append(np.sqrt(mean_squared_error(y_t,y_t_pre)))
            bag_v_rmse_1.append(np.sqrt(mean_squared_error(y_v,y_v_pre)))
        if np.mean(bag_t_rmse_1) > 0.5 or np.mean(bag_v_rmse_1) > 0.5:
            continue
        else:
            bag_t_rmse_0.append(np.mean(bag_t_rmse_1))
            bag_v_rmse_0.append(np.mean(bag_v_rmse_1))
            joblib.dump(xgb_randparams,'xgb_randparams_%s.pkl' % i)
            with open('D:\\workspace python\\statContest\\save\\' + 'xgb_randparams_0412.txt',
                      'a',encoding = 'utf-8') as f:
                f.write(str(np.mean(bag_t_rmse_1)))
                f.write(',')
                f.write(str(np.mean(bag_v_rmse_1)))
                f.write('\n')
            end = time.time()
            print('模型训练时间为',end-start,'秒')
            i += 1
    return bag_t_rmse_0,bag_v_rmse_0
        
bag_t_rmse_0,bag_v_rmse_0 = xgb_bagging()


def model1_test(X = X_test,n = y_test.shape[0],filepath = 'D:\\workspace python\\statContest\\save\\model\\'):
    res = np.zeros(30 * n).reshape(30,n)
    for i in range(30):
        print('模型 %s 正在计算中' % i)
        model = joblib.load(filepath + 'xgb_randparams_%s.pkl'%i)
        res[i] = model.predict(X)
    res = res.mean(axis = 0)
    return res

pre = np.zeros(1 * y_train.shape[0])
for train,test in get_cv(y = y_train,n_splits = 5,random_state = 42):
    X_v,y_v = X_train[test],y_train[test]
    pre[test] += model1_test(X = X_v,n = y_v.shape[0],filepath = 'D:\\workspace python\\statContest\\save\\model\\')


res1 = model1_test(X = X_test,n = X_test.shape[0])   
 
pd.DataFrame(res1,columns = ['xgb_bagging']).to_csv('res_model1_test.csv',index = False)
pd.DataFrame(pre,columns = ['xgb_bagging_v']).to_csv('res_xgb_bagging_v.csv',index = False)

