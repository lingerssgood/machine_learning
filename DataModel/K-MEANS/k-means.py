#Mean-shift,DBSCAN,Spectral clustering(谱聚类)
from sklearn.cluster import KMeans
#n_clusters: 即 K 值，一般需要多试一些 K 值来保证更好的聚类效果，你可以随机设置一些 K 值，然后选择聚类效果最好的作为最终的 K 值。
#max_iter 最大迭代次数，如果聚类很难收敛的话，设置最大迭代次数可以让我们及时得到反馈结果，否则程序运行时间会非常长。
#n_init：初始化中心点的运算次数，默认是 10。程序是否能快速收敛和中心点的选择关系非常大，所以在中心点选择上多花一些时间，
# 来争取整体时间上的快速收敛还是非常值得的。由于每一次中心点都是随机生成的，这样得到的结果就有好有坏，非常不确定，
# 所以要运行 n_init 次, 取其中最好的作为初始的中心点。如果 K 值比较大的时候，你可以适当增大 n_init 这个值。
#init： 即初始值选择的方式，默认是采用优化过的 k-means++ 方式，你也可以自己指定中心点，或者采用 random 完全随机的方式。
# 自己设置中心点一般是对于个性化的数据进行设置，很少采用。random 的方式则是完全随机的方式，一般推荐采用优化过的 k-means++ 方式。
#algorithm：k-means 的实现算法，有“auto” “full”“elkan”三种。一般来说建议直接用默认的"auto"。
#简单说下这三个取值的区别，如果你选择"full"采用的是传统的 K-Means 算法，“auto”会根据数据的特点自动选择是选择“full”还是“elkan”。我们一般选择默认的取值，即“auto”。
# coding: utf-8
from sklearn.cluster import KMeans
from sklearn import preprocessing
import pandas as pd
import numpy as np
#输入数据
data=pd.read_csv('D:\\development\\AI\\DataModel\\data\\data_means.csv',encoding='gbk')
train_x=data[["2019年国际排名","2018世界杯","2015亚洲杯"]]
df=pd.DataFrame(train_x)
kmeans=KMeans(n_clusters=3)
# 规范化到[0,1]空间
min_max_scaler=preprocessing.MinMaxScaler()
train_x=min_max_scaler.fit_transform(train_x)
#kmeans算法
kmeans.fit(train_x)
predict_y=kmeans.predict(train_x)
#合并聚类结果，插入到原数据中
#1:表示横轴，方向从左到右，表现为列的增加或者减少；0表示纵轴，方向从上到下，表示为行的增加或者减少
result = pd.concat((data,pd.DataFrame(predict_y)),axis=1)
#inplace=True 原结果发生改变，无需将结果赋值给新变量。
result.rename({0:u'聚类'},axis=1,inplace=True)
print(result)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sklearn.cluster import KMeans
from sklearn import preprocessing
import pandas as pd
import numpy as np
#输入数据
data=pd.read_csv('data.csv',encoding='gbk')
train_x=data[["2019年国际排名","2018年世界杯","2015亚洲杯"]]
df=pd.DataFrame(train_x)
kmeans=KMeans(n_clusters=3)
#规范化到[0,1]空间
min_max_scaler=preprocessing.MinMaxScaler()
train_x=min_max_scaler.fit_transform(train_x)
#kmeans算法
kmeans.fit(train_x)
predict_y=kmeans.predict(train_x)
#合并聚类结果，插入原数据中
result=pd.concat((data,pd.DataFrame(predict_y)),axis=1)
result.rename({0:u'聚类'},axis=1,inplace=True)
print(result)






