# coding:utf-8
import pandas as pd
import pymysql as ps
import json
db = ps.connect("47.104.130.213", "data_query", "Haier@2020","js_device_data" )

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# 使用 execute()  方法执行 SQL 查询
cursor.execute(" SELECT * from device_data_record_gxj_202107 limit 10")
# 使用 fetchone() 方法获取单条数据,此处数据为元组数据
data = cursor.fetchone()
#取出元组数据里面的内容
json_string=data[2]
#将字符串转成json格式
json_data=json.loads(json_string)
print(json_data)
#[1].直接写入参数test_dict
test_dict_df1 = pd.DataFrame(json_data,index = [0])
#[2].字典型赋值
test_dict_df2 = pd.DataFrame(data=json_data,index = [0])
print("test_dict_df1: ", test_dict_df1)
print("test_dict_df2: ", test_dict_df2)

# 关闭数据库连接
db.close()
