library(dplyr)
df <- read.csv('D:\\workspace python\\statContest\\save2\\data\\data_train.csv')
head(df)

y <- read.csv('D:\\workspace python\\statContest\\save2\\data\\y_train.csv',
              header = F)

df1 <- df[,1:27]
df2 <- df[,28:54]
df3 <- df[,55:84]
  
df1 <- cbind(df1,y)
df2 <- cbind(df2,y)
df3 <- cbind(df3,y)

dim(df1)
dim(df2)
dim(df3)

colnames(df1)[28] <- c('y')
colnames(df2)[28] <- c('y')
colnames(df3)[31] <- c('y')

lm_model_1 <- lm(y~.,data = df1)
lm_model_2 <- lm(y~.,data = df2)
lm_model_3 <- lm(y~.,data = df3)

res1 <- summary(lm_model_1)
res2 <- summary(lm_model_2)
res3 <- summary(lm_model_3)

summary(lm_model_1)$coefficients %>% data.frame() %>% write.csv('D:\\workspace python\\statContest\\save2\\data\\lr_res_1.csv')
summary(lm_model_2)$coefficients %>% data.frame() %>% write.csv('D:\\workspace python\\statContest\\save2\\data\\lr_res_2.csv')
summary(lm_model_3)$coefficients %>% data.frame() %>% write.csv('D:\\workspace python\\statContest\\save2\\data\\lr_res_3.csv')

md2_df <- summary(lm_model_2)$coefficients %>% data.frame()
md2_df <- md2_df[,c(1,4)]
md2_df$Estimate <- md2_df$Estimate * 10
md2_df <- md2_df[-1,]
md2_df <- md2_df[order(md2_df$Estimate),]
md2_df$Word <- row.names(md2_df)
dim(md2_df)

md2_df %>% write.csv('D:\\workspace python\\statContest\\save2\\data\\skill.csv')
