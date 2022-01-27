import datetime
import time
import numpy as np
import pandas as pd
import os
import pyecharts.options as opts
from pyecharts.charts import Line


def readData(fileName):
    data = pd.read_excel(fileName)
    datay = np.array(data)
    data['onOffStatus'].replace(306001, 100, inplace=True)
    data['onOffStatus'].replace(306000, 0, inplace=True)
    data['heatingStatus'].replace(306001, 90, inplace=True)
    data['heatingStatus'].replace(306000, 0, inplace=True)
    print(data['time'])
    plotGraph(data)
    return datay


def dealData(data):
    res = {}
    for da in data:
        if da[1] in res:
            res[da[1]]['x'].append(da[0])  # wifitype
            res[da[1]]['y'].append(da[2])  # onOffStatus
            res[da[1]]['z'].append(da[3])  # time
            res[da[1]]['w'].append(da[4])  # heatingStatus
            res[da[1]]['u'].append(da[5])  # runPower
            res[da[1]]['c'].append(da[6])  # currentTemperature
            res[da[1]]['d'].append(da[7])  # targetTemperature
            res[da[1]]['e'].append(da[8])  # currentWaterFlux
            res[da[1]]['b'].append(da[9])  # power
            res[da[1]]['v'].append(da[10])  # volume


        else:
            res[da[1]] = {}
            res[da[1]]['x'] = [da[0]]
            res[da[1]]['y'] = [da[2]]
            res[da[1]]['z'] = [da[3]]
            res[da[1]]['w'] = [da[4]]
            res[da[1]]['u'] = [da[5]]
            res[da[1]]['c'] = [da[6]]  # currentTemperature
            res[da[1]]['d'] = [da[7]]  # targetTemperature
            res[da[1]]['e'] = [da[8]]  # currentWaterFlux
            res[da[1]]['b'] = [da[9]]  # power
            res[da[1]]['v'] = [da[10]]  # volume

    return res
# 3、计算每个加热过程中对应的时间、时长、用水量、温度、体积
# x:wifiType,
# y:onOffStatus,
# z:time,
# w:heatingStatus,
# u:runPower,
# c:currentTemperature,
# d:targetTemperature,
# e:currentWaterFlux,
# b:power
def changeData(x, y, z, w, u, e, d, c, bb, v):
    rx = [];
    ry = [];
    rz = [];  # 结束加热时间
    rzz = [];  # 开始加热时间
    ru = [];
    rt = [];
    rc_s = [];  # 开始水温
    rc_e = []  # 结束水温
    rd_s = []  # 开始目标温度
    rd_e = []  # 结束目标温度
    rb_s = []  # 开始加热时是否变频
    rb_e = []  # 结束加热时是否变频
    rp = []  # 每次加热用电量
    rv = []  # 体积
    re = []  # 水量
    re_d = []  # 每天的用水量
    re_da = []  # 日期
    tempz = []
    tempm = []
    tempd = []
  ############################第一步：计算每个加热过程中对应的数据#############################################
    for i in range(len(x)):
        # 循环结束
        if (i == len(x) - 2):
            break;
        # 开始就出现加热的情况
        if i == 0:
            if int(w[i]) == 306001:
                if int(w[i + 1]) == 306001:
                    tempz.append(z[i])
                    rc_s.append(c[i])
                    rd_s.append(d[i])
                    rb_s.append(bb[i])
                    # 每个段的用水时间
                    start_use = time.mktime(datetime.datetime.strptime(z[i], "%Y-%m-%d %H:%M:%S").timetuple())
                    end_use = time.mktime(datetime.datetime.strptime(z[i + 1], "%Y-%m-%d %H:%M:%S").timetuple())
                    mid_use = round((end_use - start_use) / 60, 3)
                    tempm.append(round(e[i + 1] * mid_use,2))
                    continue
        # 1->2开始出现加热的情况
        if int(w[i]) == 306000:
            if int(w[i + 1]) == 306001:
                tempz.append(z[i + 1])
                rc_s.append(c[i])
                rd_s.append(d[i])
                rb_s.append(bb[i])
                # 每个段的用水时间
                start_use = time.mktime(datetime.datetime.strptime(z[i], "%Y-%m-%d %H:%M:%S").timetuple())
                end_use = time.mktime(datetime.datetime.strptime(z[i + 1], "%Y-%m-%d %H:%M:%S").timetuple())
                mid_use = round((end_use - start_use) / 60, 3)
                tempm.append(round(e[i + 1] * mid_use,2))

                continue;
            # 中间出现0的情况，判断下一条数据的情况
            if int(w[i + 1]) == 0:
                if int(w[i + 2]) ==306001:
                    tempz.append(z[i + 2])
                    rc_s.append(c[i])
                    rd_s.append(d[i])
                    rb_s.append(bb[i])
                    # 每个段的用水时间
                    start_use = time.mktime(datetime.datetime.strptime(z[i], "%Y-%m-%d %H:%M:%S").timetuple())
                    end_use = time.mktime(datetime.datetime.strptime(z[i + 1], "%Y-%m-%d %H:%M:%S").timetuple())
                    mid_use = round((end_use - start_use) / 60, 3)
                    tempm.append(round(e[i + 1] * mid_use,2))

        # 出现加热完成的情况
        if int(w[i]) == 306001:
            if int(w[i + 1]) == 306000:  # 当结束的值是保温字段时

                #            a1 = time.strptime(z[i], "%Y-%m-%d %H:%M:%S" )
                #            a = time.strftime( "%Y/%m/%d %H:%M:%S" , a1)
                #            b1 = time.strptime(tempz[0], "%Y-%m-%d %H:%M:%S" )
                #            b = time.strftime( "%Y/%m/%d %H:%M:%S" , b1)
                #            rt.append((a-b).seconds)
                a1 = datetime.datetime.strptime(z[i], "%Y-%m-%d %H:%M:%S")
                a = time.mktime(a1.timetuple())
                b1 = datetime.datetime.strptime(tempz[0], "%Y-%m-%d %H:%M:%S")
                b = time.mktime(b1.timetuple())
                rt.append(round((a - b) / 60, 1))  # 时长保留为分钟
                rz.append(z[i])  # 结束加热时间
                rzz.append(tempz[0])  # 开始加热时间
                rx.append(x[i])
                ru.append(u[i])
                rv.append(v[i])  # 体积
                #####################################1、不同功率下的取值情况################################
                # 额定功率等于3000,# 功率值，runPower或者actualPower,直接取功率值
                ux=u[i] / 1000
                if u[i] == 3000:
                    if bb[i] == 0 or bb[i] == 3:
                        ux = u[i] / 1000
                    elif bb[i] == 1:
                        ux = u[i] * 1 / 3 / 1000
                    elif bb[i] == 2:
                        ux = u[i] * 2 / 3 / 1000
                # 额定功率等于2000,# 功率值，runPower或者actualPower,直接取功率值
                elif u[i] == 2000:
                    if bb[i] == 0 or bb[i] == 3:
                        ux = u[i] / 1000
                    elif bb[i] == 1:
                        ux = u[i] * 2 / 5 / 1000
                    elif bb[i] == 2:
                        ux = u[i] * 3 / 5 / 1000
                # 额定功率等于2000,# 功率值，runPower或者actualPower,直接取功率值
                elif u[i] == 3300:
                    if bb[i] == 0 or bb[i] == 3:
                        ux = u[i] / 1000
                    elif bb[i] == 1:
                        ux = u[i] * 1 / 3 / 1000
                    elif bb[i] == 2:
                        ux = u[i] * 2 / 3 / 1000
                else:
                    if bb[i] == 0 or bb[i] == 3:
                        ux = u[i] / 1000
                    elif bb[i] == 1:
                        ux = u[i] * 1 / 3 / 1000
                    elif bb[i] == 2:
                        ux = u[i] * 2 / 3 / 1000
                rp.append(round(ux * (a - b) / 3600, 2))  # 每次用电量
                #####################################1、不同功率下的取值情况################################
                rc_e.append(c[i])
                rd_e.append(d[i])
                rb_e.append(bb[i])
                if y[i]:
                    ry.append('on')
                if not y[i]:
                    ry.append('off')
                #################################2、用水数据的处理情况######################################
                # 每个段的用水时间
                re.append(sum(tempm))  # 每次加热过程的用水量之和
                tempz = []
                tempm = []
                continue;
            # 当结束的值是空值时
            if int(w[i + 1]) == 0:
                if int(w[i + 2]) == 306000:
                    a1 = datetime.datetime.strptime(z[i], "%Y-%m-%d %H:%M:%S")
                    a = time.mktime(a1.timetuple())
                    b1 = datetime.datetime.strptime(tempz[0], "%Y-%m-%d %H:%M:%S")
                    b = time.mktime(b1.timetuple())
                    rt.append(round((a - b) / 60, 1))
                    rz.append(z[i])  # 结束加热时间
                    rzz.append(tempz[0])  # 开始加热时间
                    rx.append(x[i])
                    ru.append(u[i])  # 功率值
                    #####################################1、不同功率下的取值情况################################
                    # 额定功率等于3000,# 功率值，runPower或者actualPower,直接取功率值
                    ux = u[i] / 1000
                    print(ux)
                    if u[i] == 3000:
                        if bb[i] == 0 or bb[i] == 3:
                            ux = u[i] / 1000
                        elif bb[i] == 1:
                            ux = u[i] * 1 / 3 / 1000
                        elif bb[i] == 2:
                            ux = u[i] * 2 / 3 / 1000
                    # 额定功率等于2000,# 功率值，runPower或者actualPower,直接取功率值
                    elif u[i] == 2000:
                        if bb[i] == 0 or bb[i] == 3:
                            ux = u[i] / 1000
                        elif bb[i] == 1:
                            ux = u[i] * 2 / 5 / 1000
                        elif bb[i] == 2:
                            ux = u[i] * 3 / 5 / 1000
                    # 额定功率等于2000,# 功率值，runPower或者actualPower,直接取功率值
                    elif u[i] == 3300:
                        if bb[i] == 0 or bb[i] == 3:
                            ux = u[i] / 1000
                        elif bb[i] == 1:
                            ux = u[i] * 1 / 3 / 1000
                        elif bb[i] == 2:
                            ux = u[i] * 2 / 3 / 1000
                    else:
                        if bb[i] == 0 or bb[i] == 3:
                            ux = u[i] / 1000
                        elif bb[i] == 1:
                            ux = u[i] * 1 / 3 / 1000
                        elif bb[i] == 2:
                            ux = u[i] * 2 / 3 / 1000
                    rp.append(round(ux * (a - b) / 3600, 2))  # 每次用电量
                    #####################################1、不同功率下的取值情况################################
                    rc_e.append(c[i])
                    rd_e.append(d[i])
                    rb_e.append(bb[i])
                    rv.append(v[i])  # 体积
                    if y[i]:
                        ry.append('on')
                    if not y[i]:
                        ry.append('off')
                    #################################2、用水数据的处理情况######################################
                    # 每个段的用水时间
                    re.append(sum(tempm))  # 每次加热过程的用水量之和
                    tempm = []
                    tempz = []
        if int(w[i]) == 306001:
            if int(w[i + 1]) == 306001:
                # 每个段的用水时间
                start_use = time.mktime(datetime.datetime.strptime(z[i], "%Y-%m-%d %H:%M:%S").timetuple())
                end_use = time.mktime(datetime.datetime.strptime(z[i + 1], "%Y-%m-%d %H:%M:%S").timetuple())
                mid_use = round((end_use - start_use) / 60, 3)
                tempm.append(round(e[i + 1] * mid_use,2))


        # 用水量计算逻辑：
        # 1、机器加热/保温字段由1-》2，开始加热时需记录用水情况；
        # 2、机器加热/保温字段由2-》1，结束加热时需记录用水情况；
        # 3、机器处于加热过程中，需记录用水情况；
    #####################################第二步：计算每天的用水量################################################
    for i in range(len(x)):
        if (i == len(x) - 1):
            # 每天的用水量
            re_d.append(sum(tempd))
            # 每天的用水日期
            re_da.append(start_date)
            tempd = []
            break;
            # 截取字符串0:10
        start_date = z[i][0:10]
        end_date = z[i + 1][0:10]
        if start_date == end_date:
            start_use = time.mktime(datetime.datetime.strptime(z[i], "%Y-%m-%d %H:%M:%S").timetuple())
            end_use = time.mktime(datetime.datetime.strptime(z[i + 1], "%Y-%m-%d %H:%M:%S").timetuple())
            mid_use = round((end_use - start_use) / 60, 3)
            tempd.append(round(e[i + 1] * mid_use,2))

        if start_date != end_date:
            # 每天的用水量
            re_d.append(sum(tempd))
            # 每天的用水日期
            re_da.append(start_date)
            tempd = []
    return rx, ry, rz, ru, rt, rc_s, rd_s, rb_s, rc_e, rd_e, rb_e, rp, rzz, rv, re, re_d, re_da


# 输出结果
def outputData(data):
    df = pd.DataFrame(columns=(
        'wifitype', 'mac', '开关机状态', '加热开始时间', '加热结束时间', '运行功率', '加热时长', '加热时用电量', '开始水温', '结束水温', '开始目标温度', '结束目标温度',
        '开始变频标识', '结束变频标识', '体积', '加热时用水量'))
    for key in data:
        kx, ky, kz, ku, kt, kc_s, kd_s, kb_s, kc_e, kd_e, kb_e, kp, kzz, kv, ke, ke_d, ke_da = changeData(
            data[key]['x'], data[key]['y'],
            data[key]['z'], data[key]['w'],
            data[key]['u'], data[key]['e'],
            data[key]['d'], data[key]['c'],
            data[key]['b'], data[key]['v'])
        df1 = pd.DataFrame({'wifitype': kx, 'mac': key, '开关机状态': ky, '加热开始时间': kzz,
                            '加热结束时间': kz, '运行功率': ku, '加热时长': kt, '加热时用电量': kp, '开始水温': kc_s, '结束水温': kc_e,
                            '开始目标温度': kd_s,
                            '结束目标温度': kd_e,
                            '开始变频标识': kb_s, '结束变频标识': kb_e, '体积': kv, '加热时用水量': ke})
        df = pd.concat([df, df1])
        df2 = pd.DataFrame({'日期': ke_da, '每天用水量': ke_d})
        # 按天分组求每天的用电量之和,时间列转换成时间戳形式
        df['日期'] = pd.to_datetime(df['加热结束时间']).apply(lambda x: x.strftime("%Y-%m-%d"))
        # 直接在原数据框上添加某列的方式
        # 方案一：df.groupby(['日期']).count().reset_index()
        # 方案二：df.groupby(df['日期'])['用电量'].transform('sum')
        df['每天用电量'] = df.groupby(df['日期'])['加热时用电量'].transform('sum')
        result = pd.merge(df, df2, how="left", on="日期")
        inputdir = os.path.abspath(os.path.dirname(__file__))
        ouptdir = os.path.join(inputdir, 'outputf.xls')
        result.to_excel(ouptdir)


def plotGraph(data):
    # 采用pyecharts进行图形可视化展示
    c = (
        Line(init_opts=opts.InitOpts(width="100%", height="580px"))
            .add_xaxis(data['time'].values.tolist())
            .add_yaxis(series_name="目标温度",
                       y_axis=data['targetTemperature'].values.tolist(),
                       linestyle_opts=opts.LineStyleOpts(width=3, type_="dashed"),
                       )
            .add_yaxis(series_name="当前温度",
                       y_axis=data['currentTemperature'].values.tolist(),
                       linestyle_opts=opts.LineStyleOpts(width=3, type_="solid"),
                       )
            .add_yaxis(series_name="开关机状态",
                       y_axis=data['onOffStatus'].values.tolist(),
                       linestyle_opts=opts.LineStyleOpts(width=3, type_="solid"),
                       )
            .add_yaxis(series_name="加热状态",
                       y_axis=data['heatingStatus'].values.tolist(),
                       linestyle_opts=opts.LineStyleOpts(width=3, type_="solid"),
                       ).add_yaxis(series_name="水流量", y_axis=data['currentWaterFlux'].values.tolist(),
                                   linestyle_opts=opts.LineStyleOpts(width=3, type_="dashed"))
            .set_global_opts(title_opts=opts.TitleOpts(title="每天温度及加热变化(100表示开机；90表示加热)", pos_right="25%"),  # 设置标题
                             legend_opts=opts.LegendOpts(pos_left="7%"),  # 设置图例
                             tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type='cross'),
                             toolbox_opts=opts.ToolboxOpts(is_show=True, orient='horizontal',
                                                           feature={
                                                               "dataZoom": {"yAxisIndex": "none"},
                                                               "restore": {},
                                                               "saveAsImage": {},
                                                               "dataView": {},
                                                           },
                                                           ),
                             datazoom_opts=
                             opts.DataZoomOpts(
                                 range_start=0, range_end=3.17,
                             ),
                             xaxis_opts=opts.AxisOpts(
                                 name="时间",
                                 type_="category"
                             ),
                             )).render("line_basef.html")


def main():
    basedir = os.path.abspath(os.path.dirname(__file__))  # 获取当前文件所在目录
    filenames = os.listdir(basedir)
    for file in filenames:
        if file == 'inputf.xls' or file == 'inputf.xlsx':
            print(os.path.abspath(file))
            data = readData(os.path.abspath(file))
            print(data)
            drawdata = dealData(data)
            outputData(drawdata)
        else:
            continue


if __name__ == '__main__':
    main()
