import numpy as np
import pandas as pd
data = pd.read_csv("D:\\development\\AI\\DataDeal\\input\\34.csv")
df=np.array(data.values)
# average
#1、求均值的方式
a=np.mean(df['power'])
#2、求方差的方式
b=np.var(df['power'])
#3、求标准差的方式
c=np.std(df['power'])
print("均值:",a,"方差",b,"标准差",c)