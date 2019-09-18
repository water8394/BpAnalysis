import pymysql
import pandas as pd
import matplotlib.pyplot as plt


if __name__ == '__main__':
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', db='plusewave_info',
                           charset='utf8')
    cursor = conn.cursor()
    sql = """SELECT a.id,a.name, a.high_pluse_1,a.high_pluse_2,b.high, a.low_pluse_1,a.low_pluse_2,b.low from test_log a 
            inner JOIN predict b
            on a.time = b.time
            """
    cursor.execute(sql)
    results = cursor.fetchall()
    raw_high = []
    high = []
    raw_low = []
    low = []
    for r in results:
        raw_high.append((r[2] + r[3]) // 2)
        high.append(r[4])
        raw_low.append((r[5] + r[6]) // 2)
        low.append(r[7])

    plt.plot(raw_high, marker='o', c='b', label='Ref SBP')
    plt.plot(high, marker='*', c='r', label='Predict SBP')
    plt.plot(raw_low, marker='v', c='b', label='Ref DBP')
    plt.plot(low, marker='<', c='g', label='Predict DBP')
    plt.legend(prop = {'size':12})
    plt.xlabel('Cardiac Cycle', fontsize=18)
    plt.ylabel('Estimated SBP(mmHg)', fontsize=18)
    plt.show()