
# encoding=utf-8
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_boston
from sklearn.metrics import r2_score,mean_absolute_error,mean_squared_error
from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import export_graphviz
import graphviz
#准备数据集
boston=load_boston()
#探索数据
print(boston.feature_names)
#获取特征集和房间
features=boston.data
prices=boston.target
#随机抽取33%的数据作为测试集，其余为训练集
train_features,test_features,train_price,test_price=train_test_split(features,prices,test_size=0.33)
#创建CART回归树
dtr=DecisionTreeRegressor()
#拟合构造CART回归树
dtr.fit(train_features,train_price)
#预测测试集中的房价
predict_price=dtr.predict(test_features)
#测试集的结果评价
print('回归树二乘偏差均值：',mean_squared_error(test_price,predict_price))
print('回归树绝对值偏差均值：',mean_absolute_error(test_price,predict_price))

# dot_data = export_graphviz(dtr, out_file=None)
# graph = graphviz.Source(dot_data)
# # render 方法会在同级目录下生成 Boston PDF文件，内容就是回归树。
# graph.render('Boston')