import datetime
import time
import numpy as np
import pandas as pd
import os

def readData(fileName):
    data = pd.read_excel(fileName)
    return np.array(data)


def dealData(data):
    res = {}
    for da in data:
        if da[1] in res:
            res[da[1]]['x'].append(da[0])  # wifitype
            res[da[1]]['y'].append(da[2])  # onOffStatus
            res[da[1]]['z'].append(da[3])  # ts
            res[da[1]]['w'].append(da[4])  # heatingStatus
            res[da[1]]['u'].append(da[5])  # runPower
        else:
            res[da[1]] = {}
            res[da[1]]['x'] = [da[0]]
            res[da[1]]['y'] = [da[2]]
            res[da[1]]['z'] = [da[3]]
            res[da[1]]['w'] = [da[4]]
            res[da[1]]['u'] = [da[5]]
    return res


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
            if int(w[i] == 306001):
                if int(w[i + 1] == 306001):
                    tempz.append(z[i])
                    continue
        if int(w[i]) == 306000:
            if int(w[i + 1]) == 306001:
                tempz.append(z[i + 1])
                continue;
            if int(w[i + 1]) == 0:
                if int(w[i + 2]) == 306001:
                    tempz.append(z[i + 2])
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
                rt.append(a - b)
                rz.append(z[i])
                rx.append(x[i])
                ru.append(u[i])
                if int(y[i])==306001:
                    ry.append('on')
                if int(y[i])==306000:
                    ry.append('off')
                tempz = []
                continue;
            if int(w[i + 1]) == 0:  # 当结束的值是空值时
                if int(w[i + 2]) == 306000:
                    a1 = datetime.datetime.strptime(z[i], "%Y-%m-%d %H:%M:%S")
                    a = time.mktime(a1.timetuple())
                    b1 = datetime.datetime.strptime(tempz[0], "%Y-%m-%d %H:%M:%S")
                    b = time.mktime(b1.timetuple())
                    rt.append(a - b)
                    rz.append(z[i])
                    rx.append(x[i])
                    ru.append(u[i])
                    if int(y[i])==306001:
                        ry.append('on')
                    if int(y[i])==306000:
                        ry.append('off')
                    tempz = []
    return rx, ry, rz, ru, rt


def plotGraph(data):
    df = pd.DataFrame(columns=('wifitype', 'mac', 'onOffStatus', 'time', 'runPower', 'timeValue'))
    for key in data:
        kx, ky, kz, ku, kt = changeData(data[key]['x'], data[key]['y'], data[key]['z'], data[key]['w'], data[key]['u'])
        df1 = pd.DataFrame({'wifitype': kx, 'mac': key, 'onOffStatus': ky,
                            'time': kz, 'runPower': ku, 'timeValue': kt})
        df = pd.concat([df, df1])
        inputdir = os.path.abspath(os.path.dirname(__file__))
        ouptdir = os.path.join(inputdir, 'outputf.xls')
        df.to_excel(ouptdir)


def main():
    basedir = os.path.abspath(os.path.dirname(__file__))  # 获取当前文件所在目录
    filenames = os.listdir(basedir)
    for file in filenames:
        if file == 'inputf.xls' or file == 'inputf.xlsx':
            print(os.path.abspath(file))
            data = readData(os.path.abspath(file));
            print(data)
            drawdata = dealData(data)
            plotGraph(drawdata)
        else:
            continue


if __name__ == '__main__':
    main()

