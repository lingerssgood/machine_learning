# coding:utf-8
import pandas as pd
import psycopg2
import time


def main():
    conn = psycopg2.connect(database='haieredw', user='r_wh', password='r_wh123', host='10.199.127.124', port='5432')
    sql_getall = '''
    select
	statistics_dt,
	mac_id,
	wifi_type,
	to_timestamp(cast(start_water_time_stamp as bigint)/ 1000) as start_time,
	to_timestamp(cast(end_water_time_stamp as bigint)/ 1000) as end_time,
	water_qty,
	hotwater_qty,
	pdate
from
	u_ads_wh.v_t05_ndev_wh_onewateruse_cycle_di 
	where pdate='20211105' 
order by mac_id,pdate,to_timestamp(cast(start_water_time_stamp as bigint)/ 1000) asc
limit 1000
                 '''
    df = pd.read_sql(sql=sql_getall, con=conn)
    #按照设备MAC与日期分组计算
    totalWater = []  # 总的用水量
    totalHotWater = []  # 总的热水量
    totalTime = []  # 总的用水时间
    recordNum = []  # 记录的分组
    minUseWaterTime = []  # 记录的最小用水时间
    maxUseWaterTime = []  # 记录的最大用水时间
    mac_set = []
    pdate_set=[]
    #第一步按照mac,日期分组
    for (K1, K2), group in df.groupby(['mac_id', 'pdate']):
    # 第二步：数据进行错位计算
        ##方法一：
        # (df['end_time'].shift(1) -df['start_time']).values/np.timedelta64(1,'h')
        # 方法二：(df['start_time']-df['end_time'].shift(1)).dt.seconds<=60)
        group['biaoshi'] = ((group['start_time'] - group['end_time'].shift(1)).dt.seconds <= 60)
        group['shichang'] = (group['end_time'] - group['start_time']).dt.seconds
        print( group['shichang'])
        print(group['end_time'].shift(1))
        print(group['start_time'])
        # len()一共多少行
        # at(通过行名、列名来取值)/iat（通过行号、列号来取值）
        midWater = 0;
        midHotWater = 0;
        midTime = 0;
        minNum = 0;
        minTime = '';
        maxTime = '';
    #第三步：计算小于60的时间
        for i in range(len(group)):
            # 当前值等于False，下一个值是True，直接记录
            if i==len(group)-1:
                if (group.iat[i, 8]) == True:
                    midWater += group.iat[i, 5]  # 用水量
                    midHotWater += group.iat[i, 6]  # 热水量
                    midTime += group.iat[i, 9]  # 用水时长
                    maxTime = group.iat[i, 4]  # 结束用水时间
                    minNum += 1
                    totalHotWater.append(midHotWater)
                    totalWater.append(midWater)
                    totalTime.append(midTime)
                    minUseWaterTime.append(minTime)
                    maxUseWaterTime.append(maxTime)
                    recordNum.append(minNum)
                    mac_set.append(group.iat[i, 1])
                    pdate_set.append(group.iat[i, 7])
                    midWater = 0;
                    midHotWater = 0;
                    midTime = 0;
                    minTime = '';
                    maxTime = '';
                break;
            if (group.iat[i, 8]) == False:
                if (group.iat[i + 1, 8]) == True:
                    midWater += group.iat[i, 5]  # 用水量
                    midHotWater += group.iat[i, 6]  # 热水量
                    midTime += group.iat[i, 9]  # 用水时长
                    minTime = group.iat[i, 3]  # 开始用水时间
            # 当前值等于True，下一个值是True，直接记录
            if (group.iat[i, 8]) == True:
                if (group.iat[i + 1, 8]) == True:
                    midWater += group.iat[i, 5]  # 用水量
                    midHotWater += group.iat[i, 6]  # 热水量
                    midTime += group.iat[i, 9]  # 用水时长
            # 当前值等于True,下一个值是False,记录后编码重新统计另一组数据
            if (group.iat[i, 8]) == True:
                if (group.iat[i + 1, 8]) == False:
                    midWater += group.iat[i, 5]  # 用水量
                    midHotWater += group.iat[i, 6]  # 热水量
                    midTime += group.iat[i, 9]  # 用水时长
                    maxTime = group.iat[i, 4]  # 结束用水时间
                    minNum += 1
                    totalHotWater.append(midHotWater)
                    totalWater.append(midWater)
                    totalTime.append(midTime)
                    minUseWaterTime.append(minTime)
                    maxUseWaterTime.append(maxTime)
                    recordNum.append(minNum)
                    mac_set.append(group.iat[i, 1])
                    pdate_set.append(group.iat[i,7])
                    midWater = 0;
                    midHotWater = 0;
                    midTime = 0;
                    minTime = '';
                    maxTime = '';
    df1=pd.DataFrame({'totalHotWater':totalHotWater,'totalWater':totalWater,'totalTime':totalTime,'minUseWaterTime':minUseWaterTime,'maxUseWaterTime':maxUseWaterTime,
                  'maxUseWaterTime':maxUseWaterTime,'recordNum':recordNum,'mac_set':mac_set,'pdate_set':pdate_set})
    df1.to_csv('./b.csv')
    # 第三步：判断是否如果小于1的值记为True;然后判断形成新的数据后遍历判断是否存在False变为True的情况，是的话每次
    # 重新记录发生变化的点


if __name__ == '__main__':
    main()
