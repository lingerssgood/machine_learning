# coding:utf-8
#1、从数据库中查询出近30天的数据
#（1）转换开始时间为整点数据
#（2）转换预热时长为分钟
'''
'''
import pymysql
import numpy as np
import pandas as pd
from pandas import DataFrame

#1、数据库连接
def getSqlConn(host, user, password, db):
    conn = pymysql.connect(host=host, user=user, password=password, db=db)
    cursor = conn.cursor()
    return conn, cursor
#2、获取全部数据
def getDataUnionSQL(cursor, sql):
    cursor.execute(sql)
    data = cursor.fetchall()
    df= pd.DataFrame(list(data),
                    columns=['id', 'statistics_dt', 'mac_id', 'wifi_type', 'warmup_starttime', 'warmup_endtime',
                             'target_temperature', 'etl_date', 'time_interval', 'timegroup'])
    return df
#4、删除不满足小于30的数据
def getLess30Value(df):
    # dfc=df.drop_duplicates(subset=['mac_id'], keep='first', inplace=False)
    dfc=pd.DataFrame()
    for name, group in df.groupby('mac_id'):
        # dfy=group['time_interval'].groupby(group['timegroup']).mean()
        dfy=group.groupby(group['timegroup']).filter(lambda x: (abs(x.time_interval.mean()-x.time_interval) <=30).all())
        # if dfc.isnull:
        #     dfc=dfy
        # else:
        #     dfc=pd.merge(dfc,dfy)
        #     print('222222222222222222222222222222',dfc)
        # # print(name)
        # # print(group, end='\n-------------------------------\n')
        dfc = pd.concat([dfc, dfy], axis=0)
    # print(dfc)
    return dfc
    # dfc = pd.DataFrame()
    # for (key1, key2), group in df.groupby(['mac_id', 'timegroup']):
    #     # a=group['time_interval'].apply(lambda x:abs(x.mean-x) <=30)
    #     print(key1, key2)
    #     print(group, end='\n-------------------------------\n')
    #     # print(a)
    #     s = group['time_interval'].mean()
    #     m = (group['time_interval'].lt(s + 30, axis=0)) & (group['time_interval'].gt(s - 30, axis=0))
    #     dfc = group['time_interval'].loc[:, m.all()]
    #     print(dfc)
        # dfc=group['mac_id']
        # dfc=group['timegroup']
        # gt 大于
        # egt大于等于
        # lt 小于
        # elt 小于等于
        # check all Trues per columns
        # df = df.loc[:, m.all()]
    # return
#5、求最终的用户分组并输出
def printFinalResult(df):
    dx=df['time_interval'].groupby([df['mac_id'],df['timegroup']]).mean()
    # list = ['00:00', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00',
    #         '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
    # for name, group in df.groupby('mac_id'):
    #     group.append
    print(dx)
    return dx
def main():
    conn, cursor = getSqlConn('rm-2zecv8dqo91px1y7j0o.mysql.rds.aliyuncs.com', 'bigdata', 'big_data20200210','bigdata')
    data = getDataUnionSQL(cursor,'''
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
                                                                 '''
                           )
    df=getLess30Value(data)
    df=printFinalResult(df)
    # print(df)
    # drawdata = dealData(data)
    # outputdata(drawdata)
if __name__ == '__main__':
    main()
#2、按照用户、预测开始时间点分组，计算分组中的平均时长
#3、求每个分组中可以预留的数据序列。
#4、按照用户、预测开始时间计算最终的预测时长。
#5、将预测出的开始时间按照分组找到指定的预测时长
#6、预测开始时间+预测时长为最终的预测结束时间
#7、最终输出预测开始时间、预测结束时间、预测时长、预测温度