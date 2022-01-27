import datetime
import time
import numpy as np
import pandas as pd
import os
import pyecharts.options as opts
from pyecharts.charts import Line
# from pandas.plotting import register_matplotlib_converters
# 内置主题类型可查看 pyecharts.globals.ThemeType
# import matplotlib.pyplot as plt
from pyecharts.globals import ThemeType


# register_matplotlib_converters()
# plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
# plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 1、读取文件数据，然后绘图
def readData(fileName):
    data = pd.read_excel(fileName)
    datay=np.array(data)
    data['onOffStatus'].replace(True, 100, inplace=True)
    data['onOffStatus'].replace(False, 0, inplace=True)
    data['heatingStatus'].replace(2, 90, inplace=True)
    data['heatingStatus'].replace(1, 0, inplace=True)
    # data['time'] = pd.to_datetime(data['time'])
    # data['date'] = pd.to_datetime(data['time'], format='%Y-%m-%d')
    # print(data['date'])
    #
    plotGraph(data)
    return datay


# 2、数据加工处理
def dealData(data):
    res = {}
    for da in data:
        if da[1] in res:
            res[da[1]]['x'].append(da[0])  # wifitype
            res[da[1]]['y'].append(da[2])  # onOffStatus
            res[da[1]]['z'].append(da[3])  # ts
            res[da[1]]['w'].append(da[4])  # heatingStatus
            res[da[1]]['u'].append(da[5])  # runPower
            # res[da[1]]['a'].append(da[6])  # actualPower
            # res[da[1]]['b'].append(da[7])  # power
            res[da[1]]['c'].append(da[6])  # currentTemperature
            res[da[1]]['d'].append(da[7])  # targetTemperature
            # res[da[1]]['e'].append(da[10])  # currentWaterFlux
        else:
            res[da[1]] = {}
            res[da[1]]['x'] = [da[0]]
            res[da[1]]['y'] = [da[2]]
            res[da[1]]['z'] = [da[3]]
            res[da[1]]['w'] = [da[4]]
            res[da[1]]['u'] = [da[5]]
            # res[da[1]]['a']=[da[6]]# actualPower
            # res[da[1]]['b']=[da[7]]  # power
            res[da[1]]['c'] = [da[6]]  # currentTemperature
            res[da[1]]['d'] = [da[7]]  # targetTemperature
            # res[da[1]]['e']=[da[10]]  # currentWaterFlux
    return res


# 3、计算时长
def changeData(x, y, z, w, u):
    rx = [];
    ry = [];
    rz = [];
    ru = [];
    rt = [];
    tempz = []

    for i in range(len(x)):
        if (i == len(x) - 2):
            break;
        if i == 0:
            if int(w[i] == 2):
                if int(w[i + 1] == 2):
                    tempz.append(z[i])
                    continue
        if int(w[i]) == 1:
            if int(w[i + 1]) == 2:
                tempz.append(z[i + 1])
                continue;
            if int(w[i + 1]) == 0:
                if int(w[i + 2]) == 2:
                    tempz.append(z[i + 2])
        if int(w[i]) == 2:
            if int(w[i + 1]) == 1:  # 当结束的值是保温字段时

                #            a1 = time.strptime(z[i], "%Y-%m-%d %H:%M:%S" )
                #            a = time.strftime( "%Y/%m/%d %H:%M:%S" , a1)
                #            b1 = time.strptime(tempz[0], "%Y-%m-%d %H:%M:%S" )
                #            b = time.strftime( "%Y/%m/%d %H:%M:%S" , b1)
                #            rt.append((a-b).seconds)
                a1 = datetime.datetime.strptime(z[i], "%Y-%m-%d %H:%M:%S")
                a = time.mktime(a1.timetuple())
                b1 = datetime.datetime.strptime(tempz[0], "%Y-%m-%d %H:%M:%S")
                b = time.mktime(b1.timetuple())
                rt.append(a - b)
                rz.append(z[i])
                rx.append(x[i])
                ru.append(u[i])
                if y[i]:
                    ry.append('on')
                if not y[i]:
                    ry.append('off')
                tempz = []
                continue;
            if int(w[i + 1]) == 0:  # 当结束的值是空值时
                if int(w[i + 2]) == 1:
                    a1 = datetime.datetime.strptime(z[i], "%Y-%m-%d %H:%M:%S")
                    a = time.mktime(a1.timetuple())
                    b1 = datetime.datetime.strptime(tempz[0], "%Y-%m-%d %H:%M:%S")
                    b = time.mktime(b1.timetuple())
                    rt.append(a - b)
                    rz.append(z[i])
                    rx.append(x[i])
                    ru.append(u[i])
                    if y[i]:
                        ry.append('on')
                    if not y[i]:
                        ry.append('off')
                    tempz = []
    return rx, ry, rz, ru, rt


# 输出结果
def outputData(data):
    df = pd.DataFrame(columns=('wifitype', 'mac', 'onOffStatus', 'time', 'runPower', 'timeValue'))
    for key in data:
        kx, ky, kz, ku, kt = changeData(data[key]['x'], data[key]['y'], data[key]['z'], data[key]['w'], data[key]['u'])
        df1 = pd.DataFrame({'wifitype': kx, 'mac': key, 'onOffStatus': ky,
                            'time': kz, 'runPower': ku, 'timeValue': kt})
        df = pd.concat([df, df1])
        inputdir = os.path.abspath(os.path.dirname(__file__))
        ouptdir = os.path.join(inputdir, 'output.xls')
        df.to_excel(ouptdir)


def plotGraph(data):
    # 1、采用matplotlib进行图形可视化
    # x_data = data['time']
    # y_d1 = data['onOffStatus']
    # y_d2 = data['heatingStatus']
    # y_d3 = data['targetTemperature']
    # y_d4 = data['currentTemperature']
    #
    # plt.plot(x_data, y_d1, color='red', linewidth=1.0, linestyle='--',label='开关机状态')
    # plt.plot(x_data, y_d2, color='blue', linewidth=1.0, linestyle='-.',label='加热状态')
    # plt.plot(x_data, y_d3, color='green', linewidth=1.0, linestyle=':',label='目标温度')
    # plt.plot(x_data, y_d4, color='purple', linewidth=1.0, linestyle='-',label='当前温度')
    # plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='3',title='每天温度及加热情况分析表',
    #            ncol=4, mode="expand", borderaxespad=0.)

    # plt.savefig('test.jpg',dpi=500,bbox_inches='tight')

    # 采用pyecharts进行图形可视化展示
    c = (
        Line(init_opts=opts.InitOpts(width="100%", height="580px"))
            .add_xaxis(data['time'].values.tolist())
            .add_yaxis(series_name="目标温度",
                       y_axis=data['targetTemperature'].values.tolist(),
                       linestyle_opts=opts.LineStyleOpts(width=3, type_="dashed"),

                       # markpoint_opts=opts.MarkPointOpts(
                       #     data=[
                       #         opts.MarkPointItem(type_="max", name="最大值"),
                       #         opts.MarkPointItem(type_="min", name="最小值"),
                       #     ]
                       # )
                       # ,
                       # markline_opts=opts.MarkLineOpts(
                       #     data=[opts.MarkLineItem(type_="average", name="平均值")]
                       # )
                       )
            .add_yaxis(series_name="当前温度",
                       y_axis=data['currentTemperature'].values.tolist(),
                       linestyle_opts=opts.LineStyleOpts(width=3, type_="solid"),
                       # markpoint_opts=opts.MarkPointOpts(
                       #     data=[
                       #         opts.MarkPointItem(type_="max", name="最大值"),
                       #         opts.MarkPointItem(type_="min", name="最小值"),
                       #     ]
                       # )
                       # ,
                       # markline_opts=opts.MarkLineOpts(
                       #     data=[opts.MarkLineItem(type_="average", name="平均值")]
                       # )
                       )
            .add_yaxis(series_name="开关机状态",
                       y_axis=data['onOffStatus'].values.tolist(),
                       linestyle_opts=opts.LineStyleOpts(width=3, type_="solid"),
                       # markpoint_opts=opts.MarkPointOpts(
                       #     data=[
                       #         opts.MarkPointItem(type_="max", name="最大值"),
                       #         opts.MarkPointItem(type_="min", name="最小值"),
                       #     ]
                       # )
                       # ,
                       # markline_opts=opts.MarkLineOpts(
                       #     data=[opts.MarkLineItem(type_="average", name="平均值")]
                       # )
                       )
            .add_yaxis(series_name="加热状态",
                       y_axis=data['heatingStatus'].values.tolist(),
                       linestyle_opts=opts.LineStyleOpts(width=3, type_="solid"),

                       # label_opts=opts.LabelOpts(is_show=False),
                       # markpoint_opts=opts.MarkPointOpts(
                       #     data=[
                       #         opts.MarkPointItem(type_="max", name="最大值"),
                       #         opts.MarkPointItem(type_="min", name="最小值"),
                       #     ]
                       # )
                       # ,
                       # markline_opts=opts.MarkLineOpts(
                       #     data=[opts.MarkLineItem(type_="average", name="平均值")]
                       # )
                       )
            .set_global_opts(title_opts=opts.TitleOpts(title="一个月温度及加热变化(100表示开机；90表示加热)"),  # 设置标题
                             legend_opts=opts.LegendOpts(pos_right="25%"),  # 设置图例
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

                             # axispointer_opts=opts.AxisPointerOpts(
                             #     is_show=True, link=[{"xAxisIndex": "all"}]
                             # ),

                             # xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
                             xaxis_opts=opts.AxisOpts(
                                 name="时间",
                                 type_="category"
                             ),

                             # yaxis_opts=opts.AxisOpts(name="数值"),

                             )).render("line_base.html")


def main():
    basedir = os.path.abspath(os.path.dirname(__file__))  # 获取当前文件所在目录
    filenames = os.listdir(basedir)
    for file in filenames:
        if file == 'input.xls' or file == 'input.xlsx':
            print(os.path.abspath(file))
            data = readData(os.path.abspath(file))
            print(data)
            drawdata = dealData(data)
            outputData(drawdata)
        else:
            continue

    # print(drawdata)
    # plotGraph(drawdata)

    # print(basedir)
    # print(os.getcwd())  # 获取当前工作目录路径
    # print(os.path.abspath('.'))  # 获取当前工作目录路径
    # print(os.path.abspath('input.txt'))  # 获取当前目录文件下的工作目录路径
    # print(os.path.abspath('..'))  # 获取当前工作的父目录 ！注意是父目录路径
    # print(os.path.abspath(os.curdir))  # 获取当前工作目录路径

    # def file_name(file_dir):
    #     L = []
    #     for root, dirs, files in os.walk(file_dir):
    #         for file in files:
    #             if os.path.splitext(file)[1] == '.jpeg':
    #                 L.append(os.path.join(root, file))
    #     return L


if __name__ == '__main__':
    main()
