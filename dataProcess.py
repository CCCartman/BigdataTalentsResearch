# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 22:19:25 2018

@author: Rui Wenhao
@Copyright: Rui Wenhao, All rights reserved
@Mail:rui_wenhao@cueb.edu.cn
"""
import random
import numpy as np
import pandas as pd
import jieba
import os
import re

class dataProcesser:
    def __init__(self,df,filePath):
        self.df = df
        self.filePath = filePath
        
    def filter_by_edu(self,col = '学历'):
        self.df[col].replace(np.nan,'未知',inplace = True)
        self.df[col] = self.df[col].apply(lambda x:x[:2])
        idx_lst = []
        print('===========正在按照学历过滤数据集=============')
        for idx,edu in enumerate(self.df[col]):
            if edu in ['硕士','博士','本科']:
                idx_lst.append(idx)
                print(idx,'-->>',edu)  
        print('===========按照学历过滤数据集完毕=============')       
        self.df = self.df.iloc[idx_lst,:]
        self.df = self.df.loc[~self.df.岗位描述.isnull(),:]
        self.df.index = list(range(len(self.df.index)))    
        return self.df
    
    def text_transform(self):
        self.df['岗位描述'] = self.df['岗位描述'].apply(lambda x:x.lower())
        self.df['岗位'] = self.df['岗位'].apply(lambda x:x.lower())      
        return self.df
    
    def load_words(self,filename):
        __words = []
        try:
            with open(self.filePath + filename,'r',encoding = 'gbk') as f:
                for word in f:
                    word = word.rstrip()
                    __words.append(word)
        except:
            with open(self.filePath + filename,'r',encoding = 'utf-8') as f:
                for word in f:
                    word = word.rstrip()
                    __words.append(word)
        return __words
    
    def split_describe(self,col = '岗位描述'):
        split_words = self.load_words('split_words.txt')
        __idx,__duty,__require = [],[],[]
        for idx,line in enumerate(self.df[col]):
            line = line.strip()           
            for word in split_words:
                if word in line:
                    line = line.split(word)               
                    if len(line) == 2:
                        print('岗位职责\t %s \n' %line[0])
                        print('岗位要求\t %s \n' %line[1])
                        __idx.append(idx)
                        __duty.append(line[0])
                        __require.append(line[1])
                        break
        
        print('共筛选出 %d 个拥有岗位职业与岗位要求的岗位' % len(__idx))
        
        self.df = self.df.loc[__idx]
        self.df['岗位职责'] = __duty
        self.df['岗位要求'] = __require
        self.df.index = list(range(len(self.df.index)))
        return self.df
    
    def filter_by_pos(self,col = '岗位'):
        positions = self.load_words('pos_words.txt')
        idx_lst = []
        for i,j in enumerate(self.df[col]):
            for pos in positions:
                if pos in j:
                    print(i,'-->',j)
                    idx_lst.append(i)
                    break
        print('======共筛选出 %s 个职位======' % len(idx_lst))
        self.df = self.df.loc[idx_lst]
        self.df = self.df.loc[~self.df[col].isnull()]
        self.df.index = list(range(len(self.df.index))) 
        return self.df
    
    def clean_pos(self,cols = ['岗位描述','岗位职责','岗位要求']):
        for col in cols:
            self.df[col] = self.df[col].apply(lambda x:re.sub(r'<.*?>','',x))
            self.df[col] = self.df[col].str.replace('\t','').replace('\r','').replace('\n','')
            self.df[col] = self.df[col].apply(lambda x:re.sub(r'&.*?;','',x))
            self.df[col] = self.df[col].apply(lambda x:re.sub(r'\d+','',x))
            self.df[col] = self.df[col].apply(lambda x:re.sub(r'xa','',x))
            print('%s 变量清洗完毕' % col)
            self.df[col] = self.df[col].apply(lambda x:' '.join(jieba.cut(x)))
        return self.df
    
    def filter_by_words(self,cols = ['岗位职责','岗位要求']):
        __stop_words_chinese = self.load_words('stopwords.txt')
        __stop_words_eng = self.load_words('stopwords-eng.txt')
        __city = self.load_words('city.txt')
        for col in cols:
            word_list = self.df[col].apply(lambda x:x.split(' ')).tolist()
            word_list_new = []
            if col == '岗位职责':
                for idx,words in enumerate(word_list):
                    words_new = []
                    for word in words:
                        if len(word) <= 1:
                            continue
                        elif word in __stop_words_chinese:
                            continue
                        elif word in __stop_words_eng:
                            continue
                        elif word in __city:
                            continue
                        else:
                            words_new.append(word)                
                    print(idx,'------------->>>>',words_new)
                    word_list_new.append(words_new)
            elif col =='岗位要求':
                for idx,words in enumerate(word_list):
                    words_new = []
                    for word in words:
                        if len(word) <= 1 and word not in ['r','bi','c']:
                            continue
                        if word in __stop_words_chinese:
                            continue
                        elif word in __stop_words_eng:
                            continue
                        elif word in __city:
                            continue
                        else:
                            words_new.append(word)                
                    print(idx,'------------->>>>',words_new)
                    word_list_new.append(words_new)                       
            self.df[col] = word_list_new  
            self.df[col] = self.df[col].apply(lambda x:' '.join(x))
        return self.df
    
    def drop_dump_twice(self,col = '岗位职责'):
        lst_ = [] # 删除相同的岗位职责 因为同一公司可能重复发布招聘信息
        index_ = []
        for i,content in enumerate(self.df[col]):
            if content not in lst_:
                lst_.append(content)
                index_.append(i)
            else:
                continue
            print(i,'\t',content)
            
        print('去重复前的列表共有 %d 条文本' % self.df[col].shape[0])
        print('去重复后的列表共有 %d 条文本' % len(lst_))        
        self.df = self.df.iloc[index_,:]
        self.df.index = list(range(len(self.df.index)))
        return self.df
    
    def filter_by_words_twice(self,col = '岗位要求'):   
        synonym = ['本科','硕士','博士']
        __del_words = self.load_words('del_words.txt')
        res = []
        for idx,line in enumerate(self.df[col]):
            line = line.split(' ')
            new_line = []
            for word in line:
                if word in __del_words:
                    continue
                else:
                    for subword in synonym:
                        if subword in word:
                            word = subword
                new_line.append(word)
            print(new_line)
            res.append(new_line) 
            
        self.df[col] = res
        __idx = self.df[col].apply(lambda x:len(x) < 1000 and len(x) >= 50) 
        self.df = self.df.ix[__idx]
        self.df[col] = self.df[col].apply(lambda x:' '.join(x))
        self.df = self.df[~self.df[col].isnull()]
        self.df.index = list(range(len(self.df.index)))
        return self.df
    
    @staticmethod
    def __process_wage(x):
        date_dict = {'天':22,
                   '月':1,
                   '小时':8 * 22,
                   '年':1/12}
        salary_dict = {
                '元':1,
                'K':1000,
                '万':10000,
                '千':1000}
        if x is np.nan:
            x = '未知'
            return x
        elif x == '面议':
            return x
        else:
            x = x.upper()
            x = x.strip()
            for word in ['以上','以下','+']:
                if word in x:
                    x = x.replace(word,'')
            if '/' in x:
                _salary,_date = x.split('/')
            else:
                if '万' in x:
                    _salary,_date = x,'年'
                else:
                    _salary,_date = x,'月'
            for key1 in salary_dict:
                if _salary[-1] == key1:
                   _salary = _salary[:-1]                    
                   if '-' in _salary:                
                       _salary = _salary.split('-')                
                       if 'K' in _salary[0]:
                           key1 = 'K'
                           _salary[0] = _salary[0].replace('K','')
                           _salary[1] = _salary[1].replace('K','')
                       #print(x,'\t',_salary)
                       _salary = list(map(lambda x:
                           float(x) * salary_dict[key1],_salary))
                       avgSalary = np.mean(_salary)
                       ### 以月为量纲度量工资
                       for key2 in date_dict.keys():
                           if _date == key2:
                               avgSalary *= date_dict[key2]
                               break
                       break
                   else:
                       if 'K' in _salary:
                           key1 = 'K'
                           _salary = _salary.replace('K','') 
                       avgSalary = float(_salary) * salary_dict[key1]
                       for key2 in date_dict.keys():
                           if _date == key2:
                               avgSalary *= date_dict[key2]
                               break 
                   break                                        
            return avgSalary
    
    @staticmethod
    def __process_city(x):
        if x is np.nan:
            x = '未知'
            return x
        else:
            for kw in ['省','市']:
                if kw in x:
                    x = x.replace(kw,'')
                    break
            if '-' in x:
                x = x.split('-')
                return x[0]
            elif ' ' in x:
                x = x.split(' ')
                return x[0]
            else:
                return x
        
    @staticmethod
    def word_count(df,col = '岗位要求',top = 30,keyword = '大数据分析',isall = False):
        if isall:
            describe = df.loc[:,col]
        else:
            describe = df.loc[df.关键词 == keyword,col]
        word_dict = {}
        for line in describe:
            line = line.split(' ')
            for word in line:
                word_dict[word] = word_dict.get(word,0) + 1
        
        result = sorted(word_dict.items(),key = lambda x:x[1],reverse = True) 
        return result[:top]
    
    def run_all(self):
        self.df.drop_duplicates('链接',inplace = True)
        print('------------正在按学历筛选------------')
        self.filter_by_edu(col = '学历')
        print('---------正在转换岗位描述大小写------------')
        self.text_transform()
        print('----------正在切分岗位描述并筛选----------')
        self.split_describe(col = '岗位描述')
        print('---------正在按职位标签筛选------------')
        self.filter_by_pos()
        print('---------正则表达式清洗数据------------')
        self.clean_pos()
        print('---------过滤停用词、短词汇------------')
        self.filter_by_words()
        print('---------按岗位职责过滤重复数据------------')
        self.drop_dump_twice()        
        print('---------过滤长度不合适数据以及删除无用词----')
        self.filter_by_words_twice()
        self.filter_by_words_twice(col = '岗位职责')
        print('-------------处理工资特征----------------')
        self.df['工资'] = self.df['工资'].apply(self.__process_wage)
        print('-------------处理城市特征----------------')
        self.df['城市'] = self.df['城市'].apply(self.__process_city)
        return self.df


    
    
if __name__ == '__main__':
    def add_words():
        import jieba
        jieba.add_word('大数据')
        jieba.add_word('深度学习')
        jieba.add_word('机器学习')
        jieba.add_word('数据分析')
    add_words()
    df = pd.read_csv('D:\\workspace python\\statContest\\lagou.csv',header = None,
                 names = ['来源','关键词','链接','城市','公司名称','岗位',
                             '学历','工资','岗位描述'],encoding = 'utf-8')
    samp = random.sample(range(1,4000),2000)
    df = df.loc[samp]
    dp = dataProcesser(df,'D:\\workspace python\\statContest\\')
    df_ = dp.run_all()
    dp.word_count(df_,top = 100,isall = True)
                
                
            
            
   
    
    
    
    
        
        