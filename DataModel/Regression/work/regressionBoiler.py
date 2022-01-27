import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

x = [13854,12213,11009,10655,9503] #程序员工资，顺序为北京，上海，杭州，深圳，广州
x = np.reshape(x,newshape=(5,1)) / 10000.0
y =  [21332, 20162, 19138, 18621, 18016] #算法工程师，顺序和上面一致
y = np.reshape(y,newshape=(5,1)) / 10000.0
# 调用模型
lr = LinearRegression()
# 训练模型
lr.fit(x,y)
# 计算R平方
print(lr.score(x,y))
# 计算y_hat
y_hat = lr.predict(x)
# 打印出图
plt.scatter(x,y)
plt.plot(x, y_hat)
plt.show()


import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np
import pymysql
#数据数据为两列数据x和y，有表头
df = pd.read_table('d:/LinearRegression.txt')
#通过pandas读取为DataFrame，回归用的是矩阵数据而不是列表，数据为n个样品点和m个特征值，这里特征值只有一个因此换证nx1的矩阵
dataSet_x = df.loc[:, 'X'].as_matrix(columns=None)
#T为矩阵转置把1xn变成nx1
dataSet_x = np.array([dataSet_x]).T
dataSet_y = df.loc[:, 'Y'].as_matrix(columns=None)
dataSet_y = np.array([dataSet_y]).T
#regr为回归过程，fit(x,y)进行回归
regr = LinearRegression().fit(dataSet_x, dataSet_y)
#输出R的平方
print(regr.score(dataSet_x, dataSet_y))
plt.scatter(dataSet_x, dataSet_y,  color='black')
#用predic预测，这里预测输入x对应的值，进行画线
plt.plot(dataSet_x, regr.predict(dataSet_x), color='red', linewidth=1)
plt.show()
