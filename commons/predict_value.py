import pymysql
import pandas as pd
import xgboost as xgb
from sklearn.externals import joblib #jbolib模块

if __name__ == '__main__':

    choose = "high"
    if choose == "high":
        target = "svr_high"
        model_name = "svr_sbp.pkl"
    else:
        target = "svr_low"
        model_name = "svr_dbp.pkl"

    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', db='plusewave_info',
                           charset='utf8')
    cursor = conn.cursor()
    sql = """SELECT * from indicators where
            time in (
            select time from test_log)"""
    cursor.execute(sql)
    results = cursor.fetchall()
    # model = xgb.Booster(model_file="../XGB.model")
    model = joblib.load('../model/' + model_name)

    input = pd.DataFrame(columns=['ptt', 'vally_ptt', 'rr1', 'rr2', 'sum1', 'up1', 'down1', 'sum2', 'up2', 'down2'])
    for r in results:
        input.loc[0] = r[1:]
        # dtest = xgb.DMatrix(input)
        out = model.predict(input)

        sql = "update predict set %s = %f where time = '%s'" % (target, out[0],str(r[0]))
        print(sql)
        # cursor.execute(sql)
        print("*****************************")

    conn.commit()

    cursor.close()