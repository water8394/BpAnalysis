import random

from calculate.algorithm import *
import matplotlib.pyplot as plt
import os
import pymysql
"""
计算ppt 通过两路数据的峰值点来计算ptt

"""
def diffByDouble(peek1, peek2,threshold):
    peek1 = [(_, 1) for _ in peek1]
    peek2 = [(_, 2) for _ in peek2]
    peek = peek1 + peek2
    peek.sort()
    count = 0
    sum = 0
    cur_1 = -1
    cur_2 = -1
    ret = []
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
    return round(sum/count, 6)

"""
计算一组波形的R间期

"""
def rr_part(peek):
    diff = 0
    count = 0
    for i in range(len(peek)-1):
        diff += peek[i+1] - peek[i]
        count +=1
    if count == 0: count = 1
    return round(diff/count, 6)

"""
计算一组波形的特征
"""
def upAndDown(peek,vally):
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
    sum  =0
    countsum = 0
    for i in range(len(total)-1):
        if (total[i][1] == 1):
            cur1 = i
        else:
            if cur2 != -1 and 0 < total[i][0] - total[cur2][0] < 350:
                sum += total[i][0] - total[cur2][0]
                countsum += 1
            cur2 = i

        if cur1!= -1 and cur2!= -1 and 0 < total[cur1][0] - total[cur2][0] < 150:
            uptime += total[cur1][0] - total[cur2][0]
            countup += 1
        if cur1!= -1 and cur2!= -1 and 0 < total[cur2][0] - total[cur1][0] < 150:
            downtime += total[cur2][0] - total[cur1][0]
            countdown += 1
    if countsum == 0: countsum =1
    if countup == 0: countup=1
    if countdown == 0: countdown =1
    return round(sum/countsum,6), round(uptime/countup,6), round(downtime/countdown,6)


"""
寻找所有特征值
"""
def find_indicators(data):
    peek_list_01 = find_peek(data.ir1)
    peek_list_02 = find_peek(data.ir2)
    valley_list_01 = find_peek(abs(1 - data.ir1),amplitude=0.7)
    valley_list_02 = find_peek(1 - data.ir2)
    # plt.plot(data.ir1)
    # plt.plot(data.ir2)
    # plt.scatter(valley_list_01, data.ir1[valley_list_01],c='r')
    # plt.scatter(peek_list_02, data.ir2[peek_list_02])

    ptt = diffByDouble(peek_list_01, peek_list_02,50)
    vally_ptt = diffByDouble(valley_list_01, valley_list_02, 50)
    rr1 = rr_part(peek_list_01)
    rr2 = rr_part(peek_list_02)

    sum1, up1, down1 = upAndDown(peek_list_01, valley_list_01)
    sum2, up2, down2 = upAndDown(peek_list_02, valley_list_02)
    # print(ptt, vally_ptt, rr1, rr2)
    # print("1:",sum1, up1, down1)
    # print("2:",sum2, up2, down2)
    # plt.show()
    return ptt, vally_ptt, rr1, rr2, sum1, up1, down1, sum2, up2, down2

def parseData(date):
    dates = date.split('_')
    if dates[0][0] == '0':
        dates[0] = dates[0][1:]
    if dates[1][0] == '0':
        dates[1] = dates[1][1:]
    d = '_'.join(dates)
    return "'"+d+"'"

if __name__ == '__main__':
    paths = os.listdir("../data_regular/")
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', db='plusewave_info', charset='utf8')
    cursor = conn.cursor()
    for path in paths:
        root = "../data_regular/" + path
        file = pd.read_excel(root)
        data = file.loc[:, ('ir1', 'ir2')]
        ptt, vally_ptt, rr1, rr2, sum1, up1, down1, sum2, up2, down2 = find_indicators(data)
        t = path.split('.')[:-1]
        t = parseData(t[0])
        # print(t, ptt, vally_ptt, rr1, rr2, sum1, up1, down1, sum2, up2, down2)
        sql = "insert into indicators values (%s,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f)" %(str(t), ptt, vally_ptt, rr1, rr2, sum1, up1, down1, sum2, up2, down2)
        print(sql)
        cursor.execute(sql)
        conn.commit()

    cursor.close()
    conn.close()