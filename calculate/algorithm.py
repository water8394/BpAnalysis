from calculate import *

"""
寻找单路数据的峰值
"""
def find_peek(data):
    # find one serials peeks
    amplitude = 0.6
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
