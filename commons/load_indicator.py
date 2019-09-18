import pymysql
import pandas as pd
import numpy as np

def load():
    df = pd.DataFrame(columns=['t','ptt', 'vally_ptt', 'rr1', 'rr2', 'sum1', 'up1', 'down1', 'sum2', 'up2', 'down2','high_pluse_1','high_pluse_2','low_pluse_1','low_pluse_2'])
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', db='plusewave_info', charset='utf8')
    cursor = conn.cursor()
    sql = """SELECT a.*,b.high_pluse_1,b.high_pluse_2,b.low_pluse_1,b.low_pluse_2
            FROM
            indicators a
            LEFT JOIN test_log b ON a.time = b.time """
    cursor.execute(sql)
    results = cursor.fetchall()
    for result in results:
        # print(result)
        df.loc[df.shape[0],:] = result
    cursor.close()
    conn.close()
    df['ptt'] = [float(_) for _ in df['ptt']]
    df['vally_ptt'] = [float(_) for _ in df['vally_ptt']]
    df['rr1'] = [float(_) for _ in df['rr1']]
    df['rr2'] = [float(_) for _ in df['rr2']]
    df['sum1'] = [float(_) for _ in df['sum1']]
    df['up1'] = [float(_) for _ in df['up1']]
    df['down1'] = [float(_) for _ in df['down1']]
    df['sum2'] = [float(_) for _ in df['sum2']]
    df['up2'] = [float(_) for _ in df['up2']]
    df['down2'] = [float(_) for _ in df['down2']]
    high = df['high_pluse_1'] + df['high_pluse_2']
    df['high_pluse'] = [float(_)/2 for _ in high]
    low = df['low_pluse_1'] + df['low_pluse_2']
    df['low_pluse'] = [float(_)/2 for _ in low]
    return df

# 将预测结果写入sql
def write_to_table(t, predictValue):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', db='plusewave_info',
                           charset='utf8')
    cursor = conn.cursor()
    value = predictValue.astype(np.str_)
    sql = "update predict set low=" + value + " where time= '%s'" % t
    print(sql)
    cursor.execute(sql)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    load()