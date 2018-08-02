# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 14:06:36 2018

@author: Rui Wenhao
@Copyright: Rui Wenhao, All rights reserved
@Mail:rui_wenhao@cueb.edu.cn
"""

import dataProcess as dp
import os
import pandas as pd

def add_words():
    import jieba
    jieba.add_word('大数据')
    jieba.add_word('深度学习')
    jieba.add_word('机器学习')
    jieba.add_word('数据分析')
    
if __name__ == '__main__':
    add_words()
    os.chdir('D:\\workspace python\\statContest\\')
    
    df = pd.read_csv('total.csv',encoding = 'gbk')
    myProcesser = dp.dataProcesser(df,'D:\\workspace python\\statContest\\')
    new_df = myProcesser.run_all().to_csv('clean_total.csv',index = False)