# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 11:56:02 2018

@author: Rui Wenhao
@Copyright: Rui Wenhao, All rights reserved
@Mail:rui_wenhao@cueb.edu.cn
"""
import numpy as np
import pandas as pd
import os
import re
import matplotlib.pyplot as plt
import seaborn as sns 
from pylab import *  
import random
mpl.rcParams['font.sans-serif'] = ['SimHei']


df = pd.read_csv('D:\\workspace python\\statContest\\' + 'clean_0423_2.csv',
                 encoding = 'gbk')

df[df.行业种类 == '互联网/电子商务/计算机软件']['行业种类'] = '计算机软件/互联网/电子商务/'
df = df[~(df.学历 == '学历不限')]
### 画图
### 行业种类分析(in R)
df.行业种类.value_counts().to_csv('D:\\workspace python\\statContest\\save2\\data\\' + '行业种类.csv')

### 词频统计
def word_count(df,col = '岗位要求',top = 30):
        describe = df.loc[:,col]
        word_dict = {}
        for line in describe:
            line = line.split(' ')
            for word in line:
                word_dict[word] = word_dict.get(word,0) + 1     
        result = sorted(word_dict.items(),key = lambda x:x[1],reverse = True) 
        return result[:top]


### 岗位职责(in R)
pd.DataFrame(word_count(df,col = '岗位职责',
                        top = 50)).to_csv('D:\\workspace python\\statContest\\save2\\data\\' 
                            + '岗位职责.csv',index = False)

### 岗位要求(in R)
pd.DataFrame(word_count(df,col = '岗位要求',
                        top = 50)).to_csv('D:\\workspace python\\statContest\\save2\\data\\' 
                            + '岗位要求.csv',index = False)


### 公司规模(in py)
公司规模 = df.公司规模.value_counts()
公司规模 = 公司规模.reindex(['少于50人','50-150人','150-500人',
                     '500-1000人','1000-5000人','5000-10000人' 
                     ,'10000人以上'])

plt.bar(range(公司规模.shape[0]),公司规模,color = ['aquamarine','greenyellow'])
plt.xticks(range(公司规模.shape[0]),公司规模.index,fontsize=9)
plt.xlabel('公司规模',fontsize=9)
plt.ylabel('频数',fontsize=9)
for i,value in enumerate(公司规模):
    plt.text(i,value-1, '%s'%value,ha='center',fontsize=9)
plt.show()

### 经验
经验 = df.经验.value_counts()
经验 = 经验.reindex(['不限','1-3年', '3-5年', '5-7年', '7年以上'])

plt.bar(range(经验.shape[0]),经验,color = ['aquamarine','greenyellow'])
plt.xticks(range(经验.shape[0]),经验.index,fontsize=9)
plt.xlabel('经验年限',fontsize=9)
plt.ylabel('频数',fontsize=9)
for i,value in enumerate(经验):
    plt.text(i,value-1, '%s'%value,ha='center',fontsize=9)
plt.show()

## 岗位(in py)
岗位 = df.岗位.value_counts().sort_values(ascending = True)
岗位 = 岗位[-10:]
plt.barh(range(岗位.shape[0]),岗位,color = ['aquamarine','greenyellow',
                                     'orange','deepskyblue'])
plt.yticks(range(岗位.shape[0]),岗位.index,fontsize=9)
plt.xlabel('频数',fontsize=9)
plt.ylabel('岗位名称',fontsize=9)
plt.show()

## 学历(in py)
学历 = df.学历.value_counts()
学历 = 学历.reindex(['专科及以上','本科及以上',
                 '硕士及以上','博士及以上'])

plt.bar(range(学历.shape[0]),学历,color = ['aquamarine','greenyellow'])
plt.xticks(range(学历.shape[0]),学历.index,fontsize=9)
plt.xlabel('学历',fontsize=9)
plt.ylabel('频数',fontsize=9)
for i,value in enumerate(学历):
    plt.text(i,value-1, '%s'%value,ha='center',fontsize=9)
plt.show()


## 城市(in py)
城市 = df.城市.value_counts().sort_values(ascending = True)
plt.barh(range(城市.shape[0]),城市,color = ['aquamarine','greenyellow',
                                     'orange','deepskyblue'])
plt.yticks(range(城市.shape[0]),城市.index.tolist(),fontsize=9)
plt.xlabel('频数',fontsize=9)
plt.ylabel('城市',fontsize=9)
plt.show()

## 工资分布
pd.DataFrame(df.最高工资.describe()).to_csv('D:\\workspace python\\statContest\\save2\\data\\' + '最高工资.csv')
pd.DataFrame(df.最低工资.describe()).to_csv('D:\\workspace python\\statContest\\save2\\data\\' + '最低工资.csv')
pd.DataFrame(df.平均工资.describe()).to_csv('D:\\workspace python\\statContest\\save2\\data\\' + '平均工资.csv')

## 技能提取与描述
def find_skill(text):
    pattern = re.compile(r'[a-zA-z|c\+\+]+')
    skil_list = pattern.findall(text)
    return skil_list


def combine_skills(df,col = '岗位要求'):
    res = []
    for line in df.岗位要求.apply(find_skill):
        res.extend(line)
    return pd.Series(res)

软件技能 = combine_skills(df,col = '岗位要求')
软件技能 = 软件技能.value_counts().sort_values(ascending = False)
pd.DataFrame(软件技能).to_csv('D:\\workspace python\\statContest\\save2\\data\\' 
            + '软件技能.csv')


软件技能 = 软件技能[:10].sort_values()
plt.barh(range(软件技能.shape[0]),软件技能,color = ['aquamarine','greenyellow',
                                     'orange','deepskyblue'])
plt.yticks(range(岗位.shape[0]),软件技能.index,fontsize=9)
plt.xlabel('频数',fontsize=9)
plt.ylabel('软件技能',fontsize=9)
plt.show()
#### 与工资的关系
## 取对数工资
df['对数平均工资'] = np.log(1 + df.平均工资)

## 软件技能与工资
技能与工资 = df.loc[:,['平均工资','岗位要求']]
技能与工资['岗位要求'] = 技能与工资.岗位要求.apply(find_skill)

def skill_salary(df):
    skill_lst = []
    salary_lst = []
    for idx,skills in enumerate(df.岗位要求):
        for eachSkill in skills:
            skill_lst.append(eachSkill)
            salary_lst.append(float(df.平均工资.iloc[idx]))
    res = pd.DataFrame({'skill':skill_lst,'salary':salary_lst})
    return res

技能与工资 = skill_salary(技能与工资)
技能与工资group = 技能与工资.groupby(技能与工资.skill)['skill','salary'].agg(['count',np.mean])

技能与工资 = pd.DataFrame(技能与工资group.values,
                     columns = ['计数','工资'],index = 技能与工资group.index)

技能与工资2 = 技能与工资.sort_values(by = '计数',ascending = False)[:30]


ax1 = plt.figure(figsize=(16, 10)).add_subplot(111)
ax1.scatter(技能与工资2.index, 技能与工资2.工资,技能与工资2.计数//7.5,
            color = 'red')
ax1.set_title('技能 vs 薪酬 需求量', fontsize=22)
ax1.set_xticklabels(sorted(技能与工资2.index.tolist()), fontsize=15, rotation=50)
ax1.set_ylabel('薪酬RMB/月', fontsize=10)
plt.show()

## 城市与工资（地域影响）
城市与工资 = df.groupby(df.城市)['平均工资'].mean().sort_values(ascending = False)
城市与工资 = 城市与工资.astype(int)
plt.bar(range(城市与工资.shape[0]),城市与工资,color = ['aquamarine','greenyellow'])
plt.xticks(range(城市与工资.shape[0]),城市与工资.index,fontsize=9)
plt.xlabel('城市与工资',fontsize=9)
plt.ylabel('频数',fontsize=9)
for i,value in enumerate(城市与工资):
    plt.text(i,value-1, '%s'%value,ha='center',fontsize=9)
plt.show()


## 学历与工资（学历影响）
学历与工资 = df.groupby(df.学历)['平均工资'].mean()
学历与工资 = 学历与工资.reindex(['学历不限','专科及以上','本科及以上',
                 '硕士及以上','博士及以上'])
学历与工资 = 学历与工资[~(学历与工资.index == '学历不限')]
学历与工资 = 学历与工资.astype(int)
plt.bar(range(学历与工资.shape[0]),学历与工资,color = ['aquamarine','greenyellow'])
plt.xticks(range(学历与工资.shape[0]),学历与工资.index,fontsize=9)
plt.xlabel('学历与工资',fontsize=9)
plt.ylabel('频数',fontsize=9)
for i,value in enumerate(学历与工资):
    plt.text(i,value-1, '%s'%value,ha='center',fontsize=9)
plt.show()


df['学历'] = df['学历'].astype('category')
df['学历'] = df['学历'].cat.reorder_categories(['专科及以上','本科及以上','硕士及以上','博士及以上'])
df.ix[df.平均工资 < 50000,['学历','平均工资']].boxplot(by = '学历')
plt.xticks(fontsize = 8)
plt.show()

## 经验与工资（经验影响）
df.groupby(df.经验)['平均工资'].mean()

df.ix[df.平均工资 < 50000,:].boxplot(column='平均工资', by='经验')
## 公司规模与工资（公司规模影响）
df.groupby(df.公司规模)['平均工资'].mean()

df['公司规模'] = df['公司规模'].astype("category")
df['公司规模'] = df['公司规模'].cat.reorder_categories(['少于50人','50-150人','150-500人',
                         '500-1000人','1000-5000人','5000-10000人','10000人以上'])
df.ix[df.平均工资 < 50000,:].boxplot(column='平均工资', by='公司规模')
plt.xticks(fontsize = 8)
