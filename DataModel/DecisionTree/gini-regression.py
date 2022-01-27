#encodeing=utf-8
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_iris
#准备数据集
iris=load_iris()
#获取特征集和分类标识
features=iris.data
labels=iris.target
print(iris)
#随机抽取33%的数据作为测试集，其余为训练集
train_features,test_features,train_labels,test_labels=train_test_split(features,labels,test_size=0.33,random_state=0)
#创建CART分类树
clf=DecisionTreeClassifier(criterion='gini')
#拟合CART分类树
clf=clf.fit(train_features,train_labels)
#用CART分类树做预测
test_predict=clf.predict(test_features)
#预测结果与测试集结果比较
score=accuracy_score(test_labels,test_predict)
#%a.bf 至少输出a位数（少了会用空格补充，保留小数点后b位数） f是float、lf就是double
print("CART分类树准确率%.4lf"%score)
