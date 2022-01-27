import pandas as pd
import matplotlib.pyplot as plt
#<<<<<<<<<<<<<<<<<<<<<<<<<加载购买的商品信息数据>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#1、导入数据
trade_info=pd.read_csv('../input/(sample)sam_tianchi_mum_baby_trade_history.csv',engine='python')
#2、数据清洗
#(1)删除无用数据列---属性是数字编号没法具体分析。
trade_info.drop(labels='property',axis=1,inplace=True)
#(2)数据格式转换---将day列转换成时间列,格式必须是如下：%Y%m%d。
trade_info['day']=pd.to_datetime(trade_info['day'],format='%Y%m%d')
#(3)查看数据的时间范围
print('最大时间：',trade_info['day'].min(),'最小时间：',trade_info['day'].max())
#(4)查看数据量,判断值是否异常，如果小于等于，返回1；大于返回0
print((trade_info['buy_mount']<=0).sum())
#(5)查看数据集用户购买的情况等价于distinct count(userid)
print(trade_info['user_id'].nunique())
print(trade_info.shape[0])
#<<<<<<<<<<<<<<<<<<<<<<<<<加载婴幼儿的信息表#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#(1)导入数据
baby_info=pd.read_csv('../input/(sample)sam_tianchi_mum_baby.csv',engine='python')
#(2)把birthday转换成时间列
baby_info['birthday']=pd.to_datetime(baby_info['birthday'],format='%Y%m%d')
#(3)查看gender列是否存在异常数据
print(baby_info['gender'].value_counts())
#(4)清除gender列中的异常数据
baby_info=baby_info.loc[~(baby_info['gender']==2)]
print((baby_info['gender']==2))
#(5)查看婴幼儿表中的男女比例
print(baby_info['gender'].value_counts())
#《《《《《《《《《《《《《《《汇总婴幼儿表和商品购买表》》》》》》》》》》》》》》
#(1)合并数据表
df=pd.merge(trade_info,baby_info,on='user_id',how='outer')
#(2)查看新老用户的数量
user_df=df.groupby(by='user_id')['day'].agg(['min','max'])#聚合的最大最小值
print((user_df[min]==user_df[max]).value_counts())
print('每个用户的数据：',user_df)
#(3)给数据添加新的一列为购买月份
df['month']=df['day'].astype('datetime64[M]')
print(df.head())
#(4)查看每个月商品的情况
month_sales=df.groupby(by='month')['buy_mount'].sum()#聚合的总和
#(5)展示销量数据
pd.plotting.register_matplotlib_converters()
plt.plot(month_sales.index,month_sales.values)
plt.xticks(rotation=30)#倾斜30度
plt.show()
#(6)查看每年每个月的销量
df['month_num']=df['day'].dt.month#月份的标号
df['year']=df['day'].astype('datetime64[Y]')
year_month_sales=df.groupby(by=['year','month_num'])['buy_mount'].sum()
#(7)单独取出每年的数据
sale_2012=year_month_sales['2012-01-01']
sale_2013=year_month_sales['2013-01-01']
sale_2014=year_month_sales['2014-01-01']
plt.plot(sale_2012.index,sale_2012.values,label='2012')
plt.plot(sale_2013.index,sale_2013.values,label='2013')
plt.plot(sale_2014,label='2014')
plt.legend()
plt.show()
#(8)查看每天的销量数据
df['day_num']=df['day'].dt.day
# 每年11销量 由于14年11月存在一笔很大的订单导致销量异常，现将其14年11排除
df_12_11 = df.query('year == "2012-01-01" & month_num == 11')
df_13_11 = df.query('year == "2013-01-01" & month_num == 11')
df_14_11 = df.query('year == "2014-01-01" & month_num == 11')

df_12_11_sale = df_12_11.groupby('day_num')['buy_mount'].sum()
df_13_11_sale = df_13_11.groupby('day_num')['buy_mount'].sum()
# 由于14年11月存在一笔很大的订单导致销量异常，现将其14年11月排除
df_14_11_sale = df_14_11.groupby('day_num')['buy_mount'].sum()
print(df_14_11_sale)
plt.plot(df_12_11_sale.index, df_12_11_sale.values, label='12-11')
plt.plot(df_13_11_sale, label='13-11')
plt.legend()

# 每年9月的销量
df_12_9_sale = df.query('year == "2012-01-01" & month_num == 9').groupby('day_num')['buy_mount'].sum()
df_13_9_sale = df.query('year == "2013-01-01" & month_num == 9').groupby('day_num')['buy_mount'].sum()
# 14年9月存在异常大单
df_14_9_sale = df.query('year == "2014-01-01" & month_num == 9').groupby('day_num')['buy_mount'].sum()

plt.plot(df_12_9_sale, label='12-9')
plt.plot(df_13_9_sale, label='13-9')
#plt.plot(df_14_9_sale, label='14-9')
plt.legend()
plt.show()
#(9)分析一级分类商品的销量情况,使用柱状图显示
cat1_sales = df.groupby('cat1')['buy_mount'].sum()
# 要将index转成str
plt.bar(cat1_sales.index.astype('str'), cat1_sales.values)
plt.xticks(rotation=30)
plt.show()
#（10）分析一级分类商品的购买用户人数,使用柱状图显示
cat1_user_count = df.groupby('cat1')['user_id'].nunique()
plt.bar(cat1_user_count.index.astype('str'), cat1_user_count.values)
plt.show()
#《《《《《《《
# 结论：从图中可以看出 68结尾的商品，购买用户人数是最大的，但是总销量低于28产品，按照我们对于热销产品的定义，
# 50008168为热销产品。热销产品为购买人数最多的产品而不是销量最高的产品，因为可能会有少量用户一次性购买大量的某种商品。
# 》》》》》》》