# coding:utf-8
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# import pymysql
import psycopg2


def main():
    conn = psycopg2.connect(database='haieredw', user='r_wh', password='r_wh123', host='10.199.127.124', port='5432')
#非零冷水
    # sql_getall =  '''select mac_id,index_value,province_desc FROM u_ads_wh.v_opn_washer_water_rep_mon where prod_group_cd ='FB' and index_code ='0118OB0104'
    # and device_model_desc in('JSQ31-16CQ1BDU1','JSQ25-13JM6(12T)U1','JSQ30-16JM6(12T)U1','JSQ31-16JM6(12T)U1')
    #
    #              '''
#零冷水
    sql_getall = '''select mac_id,index_value,province_desc FROM u_ads_wh.v_opn_washer_water_rep_mon where prod_group_cd ='FB' and index_code ='0118OB0104'
      and device_model_desc in(
'JSQ31-16CR5SWU1',
'JSQ30-16JR1(12T)U1',
'JSQ30-16TR1(12T)U1',
'JSQ31-16WRS(12T)U1',
'JSQ31-16M6S(12T)',
'JSQ30-16R3BWU1')

                  '''
    df = pd.read_sql(sql=sql_getall, con=conn)
    print(df)
    # pandas某一列中每一行拆分成多行的方法
    # 第一步拆分
    index_value = df['index_value'].str.split(',', expand=True)
    # 第二步行转列
    index_value = index_value.stack()
    # 第三步重置索引，并命名
    index_value = index_value.reset_index(level=1, drop=True).rename('index_value')
    # 第四步和原始数据合并
    temp = df.drop(['index_value'], axis=1).join(index_value)
    # df.drop(['index_value'], axis=1).join(df['index_value'].str.split(',', expand=True).stack().reset_index(level=1, drop=True).rename('index_value'))
    #按照日期、温度分组

    counts = temp.drop_duplicates().groupby('province_desc')['index_value'].value_counts().to_frame('count').reset_index()
    counts.to_excel("C:\\Users\\01517007\\Desktop\\温度_deal_2.xls")
    #按照日期分组
    # countx = temp.drop_duplicates().groupby('pdate')['mac_id'].value_counts().to_frame('count').reset_index()
    # countx.to_excel("C:\\Users\\01517007\\Desktop\\设备数_deal.xls")

    # print(counts)


if __name__ == '__main__':
    main()
