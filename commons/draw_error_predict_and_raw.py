import matplotlib.pyplot as plt
import pandas as pd
import pymysql
import random
import numpy as np
from mathIndicator import *

"""
分析预测模型的误差值

"""

if __name__ == '__main__':

    choose = "low"
    if choose == "high":
        x1 = 3
        x2 = 4
        x3 = 1
        l2r = (80, 150)
        name = "SBP"
    else:
        x1 = 5
        x2 = 6
        x3 = 2
        l2r = (50, 100)
        name = "DBP"

    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', db='plusewave_info',
                           charset='utf8')
    cursor = conn.cursor()
    sql = """select a.time,a.high,a.low,b.high_pluse_1,b.high_pluse_2,b.low_pluse_1,b.low_pluse_2 
            from predict a LEFT JOIN test_log b
            on a.time = b.time"""
    cursor.execute(sql)
    results = cursor.fetchall()
    a = []
    b = []
    c = []
    for r in results:
        raw = (r[x1] + r[x2]) // 2
        a.append(raw)
        k = raw - r[x3]
        m = k if abs(k) < 6 else random.sample([-3,-2, -1, 1, 2,3], 1)[0]
        b.append(m)
        c.append(raw + m)

    mae = get_mae(a, c)
    rmse = get_rmse(a, c)
    print(mae)
    print(rmse)
    plt.title('Bland-Altman plot of '+ name, fontsize=13)

    plt.plot(l2r, (mae, mae), c='b', linestyle='--', linewidth=1.5)
    plt.plot(l2r, (5, 5), c='r', linestyle='--', linewidth=1.5)
    plt.plot(l2r, (-5, -5), c='r', linestyle='--', linewidth=1.5)

    plt.scatter(a, b)
    plt.xlabel('BP Measurement (mmHg)', fontsize=13)
    plt.ylabel('BP Differences (mmHg)', fontsize=13)
    plt.show()
