import math
import numpy as np
import pandas as pd

"""
寻找一个列表或者dataframe的最大值
"""
def find_max(data):
    m = -1
    for n in data:
        if math.isnan(n):
            pass
        else:
            m = n if n-m>0 else m
    return m

"""
计算一个列表或者dataframe的均值
"""
def find_mean(data):
    m = 0;
    for n in data:
        if not math.isnan(n):
            m += n
    return m/len(data)



"""
寻找一个列表或者dataframe的最小值
"""
def find_min(data):
    m = 1
    for n in data:
        if math.isnan(n):
            pass
        else:
            m = m if n - m > 0 else n
    return m

"""
归一化一个片段
"""
def regular(part, data, vally, diff):
    reg_part = data[part[0]:part[1]]
    real_diff = find_max(reg_part) - find_min(reg_part)
    ind = diff / real_diff
    reg_part = [_*ind for _ in reg_part]

    f = vally - find_min(reg_part)
    reg_part = [_ + f for _ in reg_part]

    return reg_part


"""
归一化一组数据

"""

def baseline(data):
    data = data.rolling(window=15).mean()
    mean = data.mean()
    mean_value = [mean for _ in data]


    # 寻找峰值
    peek_idx = find_peek(data)
    peeks = [data[idx] for idx in peek_idx]

    # 寻找谷值
    valley_value = [mean+(mean-_) for _ in data]
    vally_idx = find_peek(valley_value)
    vallys = [data[idx] for idx in vally_idx]


    # 寻找峰值基线,谷值基线
    peek_baseline = find_mean(peeks)
    peek_baseline = [peek_baseline for _ in data]
    vally_baseline = find_mean(vallys)
    vally_baseline = [vally_baseline for _ in data]

    # 构建片段 列表
    vally_part = []
    for i in range(len(vally_idx)-1):
        vally_part.append((vally_idx[i], vally_idx[i+1]))
    new_ir = []
    for i in range(len(vally_part)):
        new_ir += regular(vally_part[i],data,vally_baseline[0], peek_baseline[0]-vally_baseline[0])

    return new_ir

"""
寻找单路数据的峰值
"""
def find_peek(data):
    # find one serials peeks
    amplitude = 0.6
    peek_list = []
    max_value = find_max(data)
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
通过两路的峰值 peek 计算ptt
"""
def cal_ptt(data, peek_1, peek_2, thr=0.05):

    time_1 = list(data.time[peek_1])
    time_2 = list(data.time[peek_2])
    length_1 = len(time_1)
    length_2 = len(time_2)
    ptt = 0
    sum = 0
    threshold = thr
    curr_1, curr_2 = 0, 0
    while curr_1 < length_1 and curr_2 < length_2:
        # print(curr_1, curr_2)
        diff = time_2[curr_2] - time_1[curr_1]
        if 0 < diff < threshold:
            ptt += diff
            sum += 1
            curr_1 += 1
            curr_2 += 1
            continue

        elif diff > threshold:
            curr_1 = curr_1 + 1 if curr_1 < length_1 - 1 else curr_1
            diff = time_2[curr_2] - time_1[curr_1]
            if 0 < diff < threshold:
                ptt += diff
                sum += 1
                curr_1 += 1
                curr_2 += 1
                continue
            else:
                curr_2 += 1

        elif diff < 0:
            curr_2 = curr_2 + 1 if curr_2 < length_2 - 1 else curr_2
            diff = time_2[curr_2] - time_1[curr_1]
            if 0 < diff < threshold:
                ptt += diff
                sum += 1
                curr_1 += 1
                curr_2 += 1
                continue
            else:
                curr_1 += 1

        elif diff == 0:
            curr_1 += 1
            curr_2 += 1
    if sum == 0:
        try:
            return cal_ptt(data, peek_1, peek_2, threshold * 2)
        except RecursionError:
            return 0
    return round(ptt / sum, 4)

"""
计算单路数据的R 间期
"""
def cal_rr(data, peek):
    rr = 0
    sum = 0
    for i in range(1, len(peek)):
        rr += data.time[peek[i]] - data.time[peek[i - 1]]
        sum += 1

    return round(rr / sum, 4)


"""
计算所有参数
"""
def indicators(path):
    data = pd.read_excel(path, headers=None)
    data.columns = ['sensor01', 'sensor02', 'time']

    # get the peek list from two sensor
    peek_list_01 = find_peek(data.sensor01)
    peek_list_02 = find_peek(data.sensor02)
    valley_list_01 = find_peek(1 - data.sensor01)
    valley_list_02 = find_peek(1 - data.sensor02)

    # cal the PPT between sensor01 and sensor02
    ptt = cal_ptt(data, peek_list_01, peek_list_02)
    # plt.plot(data.sensor01)
    # plt.plot(data.sensor02)
    # plt.scatter(valley_list_01, data.sensor01[valley_list_01])
    # plt.scatter(valley_list_02, data.sensor02[valley_list_02])
    # plt.show()
    vally_ptt = cal_ptt(data, valley_list_01, valley_list_02)
    rr_ptt01 = cal_rr(data, peek_list_01)
    rr_ptt02 = cal_rr(data, peek_list_02)
    up_sensor01 = cal_ptt(data, peek_list_01, valley_list_01, thr=0.6)
    up_sensor02 = cal_ptt(data, peek_list_02, valley_list_02, thr=0.6)
    print('[INFO]  ptt: ', ptt, ' vally_ptt: ', vally_ptt, ' up_sensor01: ', up_sensor01, ' up_sensor02: ', up_sensor02,
          ' rr_ptt01: ', rr_ptt01, ' rr_ptt02: ', rr_ptt02)
    return [ptt, vally_ptt, up_sensor01, up_sensor02, rr_ptt01, rr_ptt02]
