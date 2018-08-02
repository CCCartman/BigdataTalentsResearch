# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 18:17:56 2018

@author: Rui Wenhao
@Copyright: Rui Wenhao, All rights reserved
@Mail:rui_wenhao@cueb.edu.cn
"""
import json
import pandas as np
import numpy as np

if __name__ == '__main__':
    file = open('D:\\workspace python\\statContest\\city.json',"rb",encoding = 'utf-8')
    fileJson = json.load(file)
    print(fileJson)
