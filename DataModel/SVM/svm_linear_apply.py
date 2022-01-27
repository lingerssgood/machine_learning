#硬间隔、软间隔、非线性SVM以及分类间隔公式
#SVM既可以做回归也可以做分类器
#SVR或者LinearSVR;SVC或者LinearSVC
#linear/poly/rbf/sigmoid
# 线性核函数:
# 多项式核函数：从低维映射到高维，参数多
# 高斯核函数：可以将样本映射到高维空间，但相对于多项式核函数来说参数较少
# sigmoid核函数：多层神经网络的映射中
#model=svm.SVC(kernel='rbf',C='1.0',gamma='auto')
#1/n_features，代表核函数的系数
#C代表目标函数的惩罚系数，系数越大，分类准确性越高，容错率低，泛化能力变差。
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import svm
from sklearn import metrics
from sklearn.externals import joblib
import time
#import pickle 保存模型的方法
#加载数据
#绝对路径与相对路径
data=pd.read_csv("D:/development/AI/DataModel/data/data.csv")
#将数据列全部展现出来
pd.set_option('display.max_columns',None)
print(data.columns)
print(data.head(5))
print(data.describe())
#将特征字段分成3组
features_mean=list(data.columns[2:12])
features_se= list(data.columns[12:22])
features_worst=list(data.columns[22:32])
#数据清洗
#ID没有用删除该列
#axis=0代表往跨行（down)，而axis=1代表跨列（across)，
#跨列沿着横轴方向；跨行沿着纵轴方向
#对应的列标签沿着水平方向依次删除
data.drop("id",axis=1,inplace=True)
#将B良性替换为0，M恶性替换为1
data['diagnosis']=data['diagnosis'].map({'M':1,'B':0})
#将肿瘤诊断结果可视化
sns.countplot(data['diagnosis'],label='Count')
plt.show()
#热力图呈现特征字段之间的相关性
#可以通过分析数据之间的相关性进行特征选择--降维
#特征选择的目的是降维，用少量的特征代表数据的特性，
# 这样也可以增强分类器的泛化能力，避免数据过拟合。
corr=data[features_mean].corr()
plt.figure(figsize=(14,14))
#annot=True显示每个方格的数据
sns.heatmap(corr,annot=True)
plt.show()
# 特征选择，保留可用的特征
features_remain = ['radius_mean','texture_mean', 'smoothness_mean','compactness_mean','symmetry_mean', 'fractal_dimension_mean']
#对特征进行选择之后，准备训练集与测试集
#抽取30%作为测试集，其余作为训练集
train,test=train_test_split(data,test_size=0.3)
#抽取特征选择的数值作为训练和测试数据
train_X=train[features_remain]
train_Y=train['diagnosis']
test_X=test[features_remain]
test_Y=test['diagnosis']
#采用Z-Score规范化数据，保证每个特征维度的数据均值为0，方差为1
ss=StandardScaler()
train_X=ss.fit_transform(train_X)
test_X=ss.transform(test_X)
#创建SVM分类器
model=svm.SVC()
model.fit(train_X,train_Y)
#测试集做预测
prrediction=model.predict(test_X)
print("准确率：",metrics.accuracy_score(test_Y,prrediction))

#模型的保存
#给保存的模型的名字加上时间标签，以区分训练过程中产生的不同的模型
mdhms = time.strftime('%d%H%M', time.localtime(time.time()))
# 保存的模型的文件名
file = r'D:\development\AI\DataModel\data\svm.joblib' + '_' + mdhms
# 保存模型
joblib.dump(model,file)
# 读取模型
svm_model = joblib.load(file)