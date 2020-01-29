import random
import pandas as pd
import numpy as np
import os
import pymysql
import sys
import xgboost as xgb
import matplotlib.pyplot as plt
import pywt

file_path = 'C:/Users/10507/Desktop/tmp/'
amplitude = 0.85


"""
小波变化 去除基线
"""
def wavelet(wave):
    sym = pywt.Wavelet('sym6')  # 小波基
    coeffs = pywt.wavedec(wave, sym)
    coeffs[0] *= 0  # 去除基线漂移
    meta = pywt.waverec(coeffs, sym)
    return meta


"""
计算ppt 通过两路数据的峰值点来计算ptt

"""
def diffByDouble(peek1, peek2, threshold):
    peek1 = [(_, 1) for _ in peek1]
    peek2 = [(_, 2) for _ in peek2]
    peek = peek1 + peek2
    peek.sort()
    count = 0
    sum = 0
    cur_1 = -1
    cur_2 = -1
    ret = []
    if len(peek) > 1:
        if peek[0][1] == 1:
            cur_1 = 0
        else:
            cur_2 = 0
        for i in range(1, len(peek)):
            if peek[i][1] == 1:
                cur_1 = i
            else:
                cur_2 = i
            if cur_1 != -1 and cur_2 != -1:
                diff = abs(peek[cur_1][0] - peek[cur_2][0])
                if diff <= threshold:
                    # ret.append((peek[cur_1][0],peek[cur_2][0]))
                    sum += diff
                    count += 1
    if count == 0:
        count = 1
    return round(sum / count, 6)


"""
计算一组波形的R间期

"""
def rr_part(peek):
    diff = 0
    count = 0
    for i in range(len(peek) - 1):
        diff += peek[i + 1] - peek[i]
        count += 1
    if count == 0: count = 1
    return round(diff / count, 6)


"""
计算一组波形的特征
"""
def upAndDown(peek, vally):
    peek = [(_, 1) for _ in peek]
    vally = [(_, 2) for _ in vally]
    total = peek + vally
    total.sort()
    # print(total)
    cur1 = -1
    cur2 = -1
    uptime = 0
    downtime = 0
    countup = 0
    countdown = 0
    sum = 0
    countsum = 0
    for i in range(len(total) - 1):
        if (total[i][1] == 1):
            cur1 = i
        else:
            if cur2 != -1 and 0 < total[i][0] - total[cur2][0] < 350:
                sum += total[i][0] - total[cur2][0]
                countsum += 1
            cur2 = i

        if cur1 != -1 and cur2 != -1 and 0 < total[cur1][0] - total[cur2][0] < 150:
            uptime += total[cur1][0] - total[cur2][0]
            countup += 1
        if cur1 != -1 and cur2 != -1 and 0 < total[cur2][0] - total[cur1][0] < 150:
            downtime += total[cur2][0] - total[cur1][0]
            countdown += 1
    if countsum == 0: countsum = 1
    if countup == 0: countup = 1
    if countdown == 0: countdown = 1
    return round(sum / countsum, 6), round(uptime / countup, 6), round(downtime / countdown, 6)


"""
寻找单路数据的峰值
"""
def find_peek(data):
    # find one serials peeks
    peek_list = []
    max_value = data.max()
    threshold = amplitude * max_value
    for i in range(2, len(data) - 2):
        if data[i] > data[i + 1] and data[i] > data[i - 1] and data[i] > threshold:
            if len(peek_list) > 1:
                diff = i - peek_list[-1]
            else:
                diff = 101
            if diff < 100:
                old = data[peek_list[-1]]
                new = data[i]
                if old > new:
                    continue
                else:
                    peek_list.pop()
                    peek_list.append(i)
            else:
                peek_list.append(i)

    return peek_list


"""
寻找所有特征值
"""
def find_indicators(data):
    peek_list_01 = find_peek(data.red1)
    # plot_peek(data.red1, peek_list_01) # 绘制峰值

    peek_list_02 = find_peek(data.red2)
    plot_peek(data.red2, peek_list_02) # 绘制峰值

    valley_list_01 = find_peek(abs(data.red1-max(data.red1)))
    plot_peek(data.red1, valley_list_01) # 绘制峰值

    valley_list_02 = find_peek(abs(data.red2-max(data.red2)))
    plot_peek(data.red2, valley_list_02) # 绘制峰值

    ptt = diffByDouble(peek_list_01, peek_list_02, 50)
    vally_ptt = diffByDouble(valley_list_01, valley_list_02, 50)
    rr1 = rr_part(peek_list_01)
    rr2 = rr_part(peek_list_02)

    sum1, up1, down1 = upAndDown(peek_list_01, valley_list_01)
    sum2, up2, down2 = upAndDown(peek_list_02, valley_list_02)

    return ptt, vally_ptt, rr1, rr2, sum1, up1, down1, sum2, up2, down2

# 读入数据
def input_table(path):
    root = file_path + path
    table = pd.read_table(root, sep=',')
    table.columns=['red1', 'ir1', 'red2', 'ir2']
    table = table[2000:]
    return table

# 对数据做预处理，归一化
def regular(table):
    # root = file_path + path
    # table = pd.read_table(root, header=None, sep=",")
    # # 第一路传感器 是 手腕 / 第二路传感器是 手指
    # table.columns = ['red1', 'ir1', 'red2', 'ir2']
    # table = table[2000:]
    #  1. 均值滤波
    table.red1 = table.red1.rolling(window=30).mean().rolling(window=20).mean()
    table.ir1 = table.ir1.rolling(window=30).mean().rolling(window=20).mean()
    table.red2 = table.red2.rolling(window=30).mean().rolling(window=20).mean()
    table.ir2 = table.ir2.rolling(window=30).mean().rolling(window=20).mean()
    table = table[60:]

    # 2. 将波形反转
    red1_max = max(table.red1)
    ir1_max = max(table.ir1)
    red2_max = max(table.red2)
    ir2_max = max(table.ir2)

    table.red1 = table.red1.map(lambda x: round(red1_max - x, 2))
    table.ir1 = table.ir1.map(lambda x: round(ir1_max - x, 2))
    table.red2 = table.red2.map(lambda x: round(red2_max - x, 2))
    table.ir2 = table.ir2.map(lambda x: round(ir2_max - x, 2))

    table.index = [_ for _ in range(0, len(table))]

    # 3. 去除基线漂移
    if len(table) % 2 == 0:
        table.red1 = wavelet(table.red1)
        table.ir1 = wavelet(table.ir1)
        table.red2 = wavelet(table.red2)
        table.ir2 = wavelet(table.ir2)
    else:
        table.red1 = wavelet(table.red1)[1:]
        table.ir1 = wavelet(table.ir1)[1:]
        table.red2 = wavelet(table.red2)[1:]
        table.ir2 = wavelet(table.ir2)[1:]
    red1_diff = abs(-min(table.red1))
    ir1_diff = abs(-min(table.red1))
    red2_diff = abs(-min(table.red1))
    ir2_diff = abs(-min(table.red1))
    table.red1 = table.red1.map(lambda x: round(x + red1_diff, 2))
    table.ir1 = table.ir1.map(lambda x: round(x + ir1_diff, 2))
    table.red2 = table.red2.map(lambda x: round(red2_diff + x, 2))
    table.ir2 = table.ir2.map(lambda x: round(ir2_diff + x, 2))

    # 4. 去除异常值
    table = remove_outer(table)
    # 保存到文件中
    # table.to_csv(file_path + "/res/"+path, sep=',',index=False, header=None)
    return table

# 去除异常值
def remove_outer(data):
    for i in range(3,len(data)-3):
        mean_red1 = data.loc[i-2,'red1'] + data.loc[i-1,'red1'] +data.loc[i+2,'red1'] +data.loc[i+1,'red1']
        mean_red2 = data.loc[i-2,'red2'] + data.loc[i-1,'red2'] +data.loc[i+2,'red2'] +data.loc[i+1,'red2'] 
        # print(data.loc[i,'red2'], mean_red2/4)
        if data.loc[i,'red2'] > 1.01 * (mean_red2/4):
            print(data[i])
            data.loc[i,'red2'] = mean_red2/4
    return data

# 输出数据
def output(file_name):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', db='plusewave_info',
                           charset='utf8')
    # 处理步骤
    # 1. 先将数据做预处理，滤波+归一化
    file = regular(file_name)

    cursor = conn.cursor()

    # 计算特征值
    data = file.loc[:, ('ir1', 'ir2')]
    ptt, vally_ptt, rr1, rr2, sum1, up1, down1, sum2, up2, down2 = find_indicators(data)
    t = file_name.split('.')[0]
    print('ppt:', ptt)
    # t = parseData(t[0])
    sql = "insert into indicators (time, ptt, vally_ptt, rr1, rr2, sum1, up1, down1, sum2, up2, down2) values ('%s',%f,%f,%f,%f,%f,%f,%f,%f,%f,%f)" % (
    str(t), ptt, vally_ptt, rr1, rr2, sum1, up1, down1, sum2, up2, down2)
    print(sql)
    cursor.execute(sql)
    conn.commit()
    # 通过xgb 计算血压
    model = xgb.Booster(model_file="C:/Users/10507/Desktop/PluseWave_Plot/XGB.model")
    input = pd.DataFrame(columns=['ptt', 'vally_ptt', 'rr1', 'rr2', 'sum1', 'up1', 'down1', 'sum2', 'up2', 'down2'])
    input.loc[0] = [ptt, vally_ptt, rr1, rr2, sum1, up1, down1, sum2, up2, down2]
    dtest = xgb.DMatrix(input)
    out = model.predict(dtest)
    sql = "insert into predict (time, high, file) values ('%s',%f,'%s')" % (str(t), out, file_name)
    cursor.execute(sql)
    conn.commit()

    cursor.close()
    conn.close()

# 绘制峰值波形点
def plot_peek(data, peek):
    plt.plot(data)
    peek_value = [data[_] for _ in peek]
    plt.scatter(peek, peek_value, c='r')
    plt.show()


if __name__ == '__main__':
    # file_name = sys.argv[1]
    file_name = '09-01/14_50_02.txt'
    table = input_table(file_name)
    table = regular(table)
    # 1 手指  2 手掌
    # plt.plot(table.red2)
    # plt.show()

    print(find_indicators(table))