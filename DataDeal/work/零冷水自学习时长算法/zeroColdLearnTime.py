# coding:utf-8
#1、从数据库中查询出近30天的数据，转成数据框形式
#（1）转换开始时间为整点数据
#（2）转换预热时长为分钟
'''
'''
#2、按照用户、开始预测整点分组，删除各分组中每一条与分组平均值之差绝对值大于30的数据
#3、（1）剩余的数据按照用户、开始预测整点分组求平均值；
# （2）按照用户分组，求分组之后的平均值，用户else代替用户整点分组中没有的值。

import pymysql
import numpy as np
import pandas as pd
from pandas import DataFrame
import datetime


#1、数据库连接
def getSqlConn(host, user, password, db):
    conn = pymysql.connect(host=host, user=user, password=password, db=db)
    cursor = conn.cursor()
    return conn, cursor


#2、获取全部数据
def getDataUnionSQL(cursor, sql):
    cursor.execute(sql)
    data = cursor.fetchall()
    df = pd.DataFrame(list(data),
                      columns=[
                          'id', 'statistics_dt', 'mac_id', 'wifi_type',
                          'warmup_starttime', 'warmup_endtime',
                          'target_temperature', 'etl_date', 'time_interval',
                          'timegroup'
                      ])
    # df.to_excel("/Users/qianyiming/Desktop/test.xlsx", index=True)
    return df


#3、删除每个分组中平均值与单个值的绝对值大于30的数据
def getLess30Value(df):
    # dfc=df.drop_duplicates(subset=['mac_id'], keep='first', inplace=False)
    df.dropna(axis=0, how='any', inplace=True)
    dfc = pd.DataFrame()
    for name, group in df.groupby('mac_id'):
        #（1）组删除，即只要组里面有一个不满足条件就会删除
        # dfy = group['time_interval'].groupby(group['timegroup']).mean()
        # dfy = group.groupby(group['timegroup']).filter(lambda x: (abs(
        #     x.time_interval.mean() - x.time_interval) <= 30).any())
        #（2）组内每一条删除，即组里哪个不满足条件就删除掉哪个，采用第二种。
        dfy = group.groupby(group['timegroup']).apply(
            lambda x: x[abs(x.time_interval - x.time_interval.mean()) <= 30])
        dfc = pd.concat([dfc, dfy], axis=0)
        # dfc.drop_index
    #（3）因为分组有重名的timegroup,故删除掉重名的timegroup索引
    dfc.reset_index(drop=True, inplace=True)
    return dfc


#4、不同用户不同时长分组
def printFinalResult(df):
    # dx = df['time_interval'].groupby([df['mac_id'], df['timegroup']]).mean()
    #第一步：按照mac_id,timegroup分组，计算出平均值
    data1 = df[['mac_id', 'timegroup',
                'time_interval']].groupby(['mac_id', 'timegroup'
                                           ]).agg({'mean'}).reset_index()
    data1.columns = (['mac_id', 'timegroup', 'time_interval'])
    #第二步：按照mac_id求每个设备的平均值，并用该值代替未计算出的平均值,未计算出时间用else代替
    data2 = data1[['mac_id', 'time_interval'
                   ]].groupby(['mac_id']).agg({'mean'}).reset_index()
    data2.columns = (['mac_id', 'time_interval'])
    data2.insert(1, 'timegroup', 'else')
    #第三步：按照将第一步和第二步的数据合并
    dff = pd.concat([data1, data2], axis=0, ignore_index=True)
    today = datetime.datetime.now()
    # 计算偏移量
    offset = datetime.timedelta(days=+1)
    # 获取修改后的时间并格式化
    re_date = (today + offset).strftime('%Y-%m-%d')
    dff.insert(3, 'statistict', re_date)
    dff.sort_values(by=['mac_id', 'statistict'], ascending=False, inplace=True)
    return dff


def main():
    conn, cursor = getSqlConn('rm-2zecv8dqo91px1y7j0o.mysql.rds.aliyuncs.com',
                              'bigdata', 'big_data20200210', 'bigdata')
    data = getDataUnionSQL(
        cursor, '''
                              select
                                id,
                                statistics_dt,
                                mac_id,
                                wifi_type,
                                warmup_starttime,
                                warmup_endtime,
                                target_temperature,
                                etl_date,
                                TIMESTAMPDIFF(minute,
                                date_format(CONCAT(statistics_dt, " ", warmup_starttime, ":00"), '%Y-%m-%d %H:%i:%s'),
                                date_format(CONCAT(statistics_dt, " ", warmup_endtime, ":00"), '%Y-%m-%d %H:%i:%s')) as "time_interval",
                                CONCAT_WS(":", SUBSTRING_INDEX(warmup_starttime, ':', 1), "00")as "timegroup"
                            from
                                bigdata.opn_msg_remind_gwh_learn_day
                            where
                                DATE_SUB(CURDATE(), interval 30 day) <= date(statistics_dt)
                                order by mac_id,CONCAT_WS(":", SUBSTRING_INDEX(warmup_starttime, ':', 1), "00")
                                 limit 100;
                                                                 ''')
    #测试用的直接导入满足某些临界条件的数据
    # data = pd.read_excel("/Users/qianyiming/Desktop/test.xlsx")
    df_30 = getLess30Value(data)
    df_final = printFinalResult(df_30)
    df_final.to_excel("/Users/qianyiming/Desktop/zeroColdLearnTime.xlsx",
                      index=True)


if __name__ == '__main__':
    main()
