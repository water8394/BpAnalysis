import datetime
import os
from algorithm import *


if __name__ == '__main__':
    df = pd.read_excel("/document/Project/连续血压测量装置/数据记录.xls")
    cols = df.columns
    df.columns = ['object', 'date', 'high01', 'low01', 'high02', 'low02', 'ptt', 'vally_ptt', 'up_sensor01',
                  'up_sensor02', 'rr_sensor01', 'rr_sensor02']
    root_path = "/document/Project/BPAnalysis/afterFilter/"
    needs = ['01-08/', '01-10/', '01-11/']
    for need in needs:
        file_list = os.listdir(root_path + need)
        # print(file_list)

        for file in file_list:
            # time_is is the test date of file
            time_is = file.split('.')[0].split('_')[1:]
            time_is = [int(_) for _ in time_is]
            year = 2019 if time_is[0] == 1 else 2018
            time_is = datetime.datetime(year=year, month=time_is[0], day=time_is[1], hour=time_is[2], minute=time_is[3])

            path = root_path + need + file  # read the object test data

            df.loc[df['date'] == time_is, ['ptt', 'vally_ptt', 'up_sensor01', 'up_sensor02', 'rr_sensor01',
                                           'rr_sensor02']] = indicators(path)
    print(df)
    df.columns = cols
    df.to_excel("/document/Project/连续血压测量装置/数据记录.xls")
