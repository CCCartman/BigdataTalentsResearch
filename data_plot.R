library(wordcloud)
library(xlsx)
library(Rwordseg)
library(dplyr)
library(wordcloud2)  

## ��ҵ����
df <- read.csv('D:\\workspace python\\statContest\\save2\\data\\��ҵ����.csv',
               header = F,col.names = c('word','freq'))
df <- head(df,20)
wordcloud2(df, size = 0.6,fontFamily = "΢���ź�")

## ��λְ��
df <- read.csv('D:\\workspace python\\statContest\\save2\\data\\��λְ��.csv',
               header = T,col.names = c('word','freq'))
#df <- head(df,20)
wordcloud2(df, size = 0.5,fontFamily = "΢���ź�")

## ��λҪ��
df <- read.csv('D:\\workspace python\\statContest\\save2\\data\\��λҪ��.csv',
               header = T,col.names = c('word','freq'))
df <- df[df$freq < 30000,]
wordcloud2(df, size = 0.5,fontFamily = "΢���ź�")

## ��������
df <- read.csv('D:\\workspace python\\statContest\\save2\\data\\��������.csv',
               header = F,col.names = c('word','freq'))
df <- df[1:80,]
wordcloud2(df, size = 0.6,fontFamily = "΢���ź�")
