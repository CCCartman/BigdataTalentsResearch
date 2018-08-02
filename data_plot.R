library(wordcloud)
library(xlsx)
library(Rwordseg)
library(dplyr)
library(wordcloud2)  

## 行业种类
df <- read.csv('D:\\workspace python\\statContest\\save2\\data\\行业种类.csv',
               header = F,col.names = c('word','freq'))
df <- head(df,20)
wordcloud2(df, size = 0.6,fontFamily = "微软雅黑")

## 岗位职责
df <- read.csv('D:\\workspace python\\statContest\\save2\\data\\岗位职责.csv',
               header = T,col.names = c('word','freq'))
#df <- head(df,20)
wordcloud2(df, size = 0.5,fontFamily = "微软雅黑")

## 岗位要求
df <- read.csv('D:\\workspace python\\statContest\\save2\\data\\岗位要求.csv',
               header = T,col.names = c('word','freq'))
df <- df[df$freq < 30000,]
wordcloud2(df, size = 0.5,fontFamily = "微软雅黑")

## 软件技能
df <- read.csv('D:\\workspace python\\statContest\\save2\\data\\软件技能.csv',
               header = F,col.names = c('word','freq'))
df <- df[1:80,]
wordcloud2(df, size = 0.6,fontFamily = "微软雅黑")

