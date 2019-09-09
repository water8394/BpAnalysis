import pymysql
import pandas as pd
import matplotlib.pyplot as plt


if __name__ == '__main__':
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', db='plusewave_info',
                           charset='utf8')
    cursor = conn.cursor()
    sql = """SELECT a.id,a.name, a.high_pluse_1,a.high_pluse_2,b.high from test_log a 
            inner JOIN predict b
            on a.time = b.time
            """
    cursor.execute(sql)
    results = cursor.fetchall()
    raw = []
    predict = []
    for r in results:
        raw.append((r[2]+r[3])//2)
        predict.append(r[-1])

    plt.plot(raw,marker='o',c='b', label='Ref SBP')
    plt.plot(predict,marker='*',c='r', label='Predict SBP')
    plt.legend(prop = {'size':12})
    plt.xlabel('Cardiac Cycle', fontsize=18)
    plt.ylabel('Estimated SBP(mmHg)', fontsize=18)
    plt.show()