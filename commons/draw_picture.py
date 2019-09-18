import matplotlib.pyplot as plt
import pandas as pd
import pymysql



if __name__ == '__main__':
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
    for r in results:
        raw = (r[3] + r[4]) //2
        a.append(raw)
        b.append(raw - r[1])
        print(raw, r[1])
    plt.title('Bland-Altman plot of SBP', fontsize=16)
    plt.plot((90,150),(5,5), c='r')
    plt.plot((90,150),(-5,-5), c='r')
    plt.plot((90,150),(0,0), c='r')
    plt.plot((90,150),(10,10), c='r')
    plt.plot((90,150),(-10,-10), c='r')
    plt.scatter(a,b)
    plt.xlabel('BP Measurement (mmHg)', fontsize=16)
    plt.ylabel('BP Differences (mmHg)', fontsize=16)
    plt.show()