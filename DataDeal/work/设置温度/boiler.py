import pandas as pd
import numpy as np
df=pd.read_excel('D:\\8-采暖炉项目\\采暖炉热水量曲线\\test2.xlsx')
print(df)
df = df.sort_values(by='time', ascending=True)
# 1、计算前后两个值的时间间隔
df['change'] = df['time'] - df['time'].shift(1)
df['change'] =df['change'].dt.total_seconds()/60
print(df)
# print(df['change'])
# df=df[df['change'] <180]
list=[]
#2、遍历数据将时间间隔与水流数据相乘
for index, row in df.iterrows():
    if index!=0:
        list.append(row['change'])
    if index==df.index[-1]:
        list.append(0)
df['timeValue']=list
df=df[df['timeValue'] <180]
df['total']=df['timeValue']*df['waterFlux']
print(df['total'].sum())
df.to_csv('D:\\8-采暖炉项目\\采暖炉热水量曲线\\test2.csv')