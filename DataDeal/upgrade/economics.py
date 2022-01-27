# http://tushare.org/---财经数据地址
#https://waditu.com/document/2
import tushare as ts
import pandas as pd
print('版本信息：',ts.__version__)
# token:7f5ffbb9bd2b3b45bbe0e07212c0713772f748a3a2cfa001314135eb
token='7f5ffbb9bd2b3b45bbe0e07212c0713772f748a3a2cfa001314135eb'
pro = ts.pro_api(token)
#1、指数基本信息
#-------------输入参数------------
# ts_code	str	N	指数代码
# name	str	N	指数简称
# market	str	N	交易所或服务商(默认SSE)
# publisher	str	N	发布商
# category	str	N	指数类别
#------------输出参数----------------
# 名称	类型	描述
# ts_code	str	TS代码
# name	str	简称
# fullname	str	指数全称
# market	str	市场
# publisher	str	发布方
# index_type	str	指数风格
# category	str	指数类别
# base_date	str	基期
# base_point	float	基点
# list_date	str	发布日期
# weight_rule	str	加权方式
# desc	str	描述
# exp_date	str	终止日期
#-----------市场说明-----------------
#市场代码	说明
# MSCI	MSCI指数
# CSI	中证指数
# SSE	上交所指数
# SZSE	深交所指数
# CICC	中金指数
# SW	申万指数
# OTH	其他指数
# df=pro.index_basic(market='SW')
# print(df)

# df = pro.trade_cal(exchange='', start_date='20180901', end_date='20181001', fields='exchange,cal_date,is_open,pretrade_date', is_open='0')

df = pro.index_basic(market='SW')
print(df)
#
# #获取财经历史数据
# df=ts.get_k_data(code='600159',start='1999-01-10')
# #历史数据持久化到本地
# df.to_csv('./output/maotai.csv')
# #加载外部数据到df中
# df=pd.read_csv('./output/maotai.csv')
# df.head()
