import pymysql
import pandas as pd
import xgboost as xgb


if __name__ == '__main__':
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', db='plusewave_info',
                           charset='utf8')
    cursor = conn.cursor()
    sql = """SELECT * from indicators where
            time in (
            select time from test_log)"""
    cursor.execute(sql)
    results = cursor.fetchall()
    model = xgb.Booster(model_file="C:/Users/10507/Desktop/PluseWave_Plot/XGB.model")
    input = pd.DataFrame(columns=['ptt', 'vally_ptt', 'rr1', 'rr2', 'sum1', 'up1', 'down1', 'sum2', 'up2', 'down2'])
    for r in results:
        input.loc[0] = r[1:]
        dtest = xgb.DMatrix(input)
        out = model.predict(dtest)
        print(r[0])
        print(out)
        sql = "insert into predict (time, high, file) values ('%s',%f,'%s')" % (str(r[0]), out, "tmp")
        cursor.execute(sql)
        print("*****************************")

    conn.commit()

    cursor.close()