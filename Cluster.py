# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 23:52:53 2018

@author: Rui Wenhao
@Copyright: Rui Wenhao, All rights reserved
@Mail:rui_wenhao@cueb.edu.cn
"""
import numpy as np
import pandas as pd
import os
import re

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from sklearn.externals import joblib 

def word_count(df,col = '岗位要求',top = 30):
        describe = df.loc[:,col]
        word_dict = {}
        for line in describe:
            line = line.split(' ')
            for word in line:
                word_dict[word] = word_dict.get(word,0) + 1     
        result = sorted(word_dict.items(),key = lambda x:x[1],reverse = True) 
        return result[:top]
    
df = pd.read_csv('D:\\workspace python\\statContest\\' + 'clean_0423_2.csv',
                 encoding = 'gbk')
df[df.行业种类 == '互联网/电子商务/计算机软件']['行业种类'] = '计算机软件/互联网/电子商务/'
df = df[~(df.学历 == '学历不限')]
df['对数平均工资'] = np.log(1 + df.平均工资)

count_ = CountVectorizer(max_features=200)
聚类词语矩阵 = count_.fit_transform(df.岗位要求)


kmeans = KMeans(n_clusters = 4,random_state = 123)
kmeans.fit(聚类词语矩阵)

joblib.dump(kmeans,'D:\\workspace python\\statContest\\save2\\model\\kmeans.pkl')
kmeans = joblib.load('D:\\workspace python\\statContest\\save2\\model\\kmeans.pkl')

软件技能 = pd.read_csv('D:\\workspace python\\statContest\\save2\\data\\' + 'software.csv',
                   names = ['word','freq'])
软件技能word = 软件技能[:35].word.tolist()
del_soft = ['svm','css','javascript','html','web']
for word in del_soft:
    if word in 软件技能word:
        软件技能word.remove(word)

kmeans.inertia_
kmeans.labels_

df['标签'] =kmeans.labels_
df['标签'].value_counts()

def count_software(df,col = '岗位要求'):
    describe = df.loc[:,col]
    word_dict = {}
    for line in describe:
        line = line.split(' ')
        for word in line:
            if word in 软件技能word:
                word_dict[word] = word_dict.get(word,0) + 1
    result = sorted(word_dict.items(),key = lambda x:x[1],reverse = True) 
    return result


职责1 = pd.DataFrame(word_count(df.loc[df.标签 == 0,:],col = '岗位职责'))
职责2 = pd.DataFrame(word_count(df.loc[df.标签 == 1,:],col = '岗位职责'))
职责3 = pd.DataFrame(word_count(df.loc[df.标签 == 2,:],col = '岗位职责'))
职责4 = pd.DataFrame(word_count(df.loc[df.标签 == 3,:],col = '岗位职责'))


类别1 = pd.DataFrame(count_software(df.loc[df.标签 == 0,:],col = '岗位要求')) # java hadoop linux spark python mysql hive hbase sql oracle大数据分析类
类别2 = pd.DataFrame(count_software(df.loc[df.标签 == 1,:],col = '岗位要求')) # c++ java spark hadoop matlab tensorflow linux r caffe opencv 深度学习
类别3 = pd.DataFrame(count_software(df.loc[df.标签 == 2,:],col = '岗位要求')) # c++ sql c java hadoop r linux spark excel matlab mysql
类别4 = pd.DataFrame(count_software(df.loc[df.标签 == 3,:],col = '岗位要求')) # SQl Python R EXCEL SAS SPSS HADOOP SPARK PPT JAVA HIVE


聚类结果关键词 = pd.concat([类别1,类别2,类别3,类别4],axis = 1)
聚类结果关键词.to_csv('D:\\workspace python\\statContest\\save2\\data\\聚类结果关键词4类.csv',index = False)

岗位职责关键词 = pd.concat([职责1,职责2,职责3,职责4],axis = 1)
岗位职责关键词.to_csv('D:\\workspace python\\statContest\\save2\\data\\岗位职责关键词.csv',index = False)
