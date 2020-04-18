from data_pipline import *
import json
import xgboost as xgb
from sklearn.model_selection import train_test_split
"""
读取数据并转为 Dataframe

方便拿各种数据的

输入为 txt 路径 -> DataFrame(ir1,red1,ir2,red2)
"""

class SensorData:

    def __init__(self):
        self.data = None
        self.record = None

        self._load_record()

    def _load(self, path, form='txt'):
        # 加载文件
        self.data = self.load(path, form)

    def _load_record(self):
        # 加载实验记录
        self.record = pd.read_excel('../scene/记录表.xlsx')

    @staticmethod
    def load(path, form='txt'):
        # 把 txt/excel 转为 dataframe
        data = pd.DataFrame

        if form == 'txt':
            data = pd.read_table(path, header=None, sep=',')
        elif form == 'excel':
            data = pd.read_excel(path, header=None)

        data.columns = ['ir1', 'red1', 'ir2', 'red2']

        return data

    # 有很多中间文件需要直接拿到，比如峰值索引点，峰谷索引点

    @staticmethod
    def load_peek_index(k, default='peak_index'):
        # 拿到峰值索引点
        path = SensorData._combine_path(k, default=default)
        try:
            idx = pd.read_table(path, header=None, sep=',')
        except:
            idx = pd.DataFrame(columns=['ir1', 'ir2'])
        print(idx)
        if idx.shape[1] == 1:
            idx.columns = ['ir1']
        elif idx.shape[1] == 2:
            idx.columns = ['ir1', 'ir2']
        return idx

    @staticmethod
    def _combine_path(k, default='data', form='txt'):
        return '../scene/' + default + '/' + str(k) + '.' + form

    def get_record_number(self):
        # 拿到实验记录编号
        record = self.record[self.record['usage'] != 0]
        return record['number']

    def load_by_number(self, k, default='data'):
        # 通过实验记录编号直接加载数据
        path = SensorData._combine_path(k, default)
        return self.load(path)

    def resave_file(self, k, data, default='regular'):
        # 把数据存储为txt  /  dafault是上层目录的名字
        path = SensorData._combine_path(k, default)
        with open(path, 'w+') as f:
            f.seek(0)
            for i in range(data.shape[0]):
                line = data.loc[i]
                line = ','.join(str(_) for _ in line) + '\n'
                f.writelines(line)
            f.truncate()

    @staticmethod
    def load_all_index(k):
        # 加载索引点  波峰 波谷 重播波峰值点
        pks = SensorData.load_peek_index(k)
        mid_pks = SensorData.load_peek_index(k, default='mid_peak_index')
        vl_pks = SensorData.load_peek_index(k, default='vally_peak_index')
        return pks, mid_pks, vl_pks

    @staticmethod
    def save_all_indicators(k, data, default='feature_point'):
        # 通过文件得到的特征值
        # 目前一共9个特征值 ptt tsf tad 。。。。

        path = SensorData._combine_path(k, default)
        with open(path, 'w+') as f:
            f.seek(0)
            for i in range(len(data)):
                line = data[i]
                line = ','.join(str(_) for _ in line) + '\n'
                f.writelines(line)
            f.truncate()

    @staticmethod
    def load_feature_points(k):
        #通过编号拿到特征点
        # 一个有4个 起始点 结束点 波峰 重播波波峰
        path = SensorData._combine_path(k, default='feature_point')
        data = pd.read_table(path, header=None, sep=',')
        data.columns = ['f1', 'f2', 'f3', 'f4']
        return data

    @staticmethod
    def save_metric(k, metrics):
        # 保存 特征值

        path = SensorData._combine_path(k, default='metric')
        with open(path, 'w+') as f:
            f.seek(0)
            tags = 'bf, bs, sd, df, sf, rr, asd, asf,ptt \n'
            f.writelines(tags)
            line = ','.join([str(_) for _ in metrics])
            f.writelines(line + '\n')
            f.truncate()

    @staticmethod
    def load_json_metric(k):
        # 加载json格式的特征值
        path = SensorData._combine_path(k, default='metric', form='json')
        with open(path, 'r') as f:
            data = json.load(f)
        return data


    @staticmethod
    def load_metric(k):
        sensor=SensorData()
        record = sensor.record
        metric_name = ['bf', 'bs', 'sd', 'df', 'sf', 'rr', 'asd', 'asf', 'ptt']
        columns = ['bf', 'bs', 'sd', 'df', 'sf', 'rr', 'asd', 'asf', 'ptt', 'high', 'low']
        df = pd.DataFrame(columns=columns)
        metric = sensor.load_json_metric(k)
        high, low = int(record[record['number'] == k]['high']), int(record[record['number'] == k]['low'])
        l = []
        for name in metric_name:
            l.append(np.mean(metric[name]))
        l.append(high)
        l.append(low)
        insert_row = dict(zip(columns, l))
        df.loc[df.shape[0]] = insert_row
        df['ptt'] = [abs(_) for _ in list(df['ptt'])]
        high, low = df.loc[:, 'high'], df.loc[:, 'low']
        df = df.drop(['high', 'low'], axis=1)
        df.fillna(0, inplace=True)
        return df, xgb.DMatrix(df), list(high), list(low)

    @staticmethod
    def load_all_metric(numbers):
        sensor=SensorData()
        record = sensor.record
        metric_name = ['bf', 'bs', 'sd', 'df', 'sf', 'rr', 'asd', 'asf', 'ptt']
        columns = ['bf', 'bs', 'sd', 'df', 'sf', 'rr', 'asd', 'asf', 'ptt', 'high', 'low']
        df = pd.DataFrame(columns=columns)
        for k in numbers:
            metric = sensor.load_json_metric(k)
            high, low = int(record[record['number'] == k]['high']), int(record[record['number'] == k]['low'])
            l = []
            for name in metric_name:
                l.append(np.mean(metric[name]))
            l.append(high)
            l.append(low)
            insert_row = dict(zip(columns, l))
            df.loc[df.shape[0]] = insert_row
        df['ptt'] = [abs(_) for _ in list(df['ptt'])]
        high, low = df.loc[:, 'high'], df.loc[:, 'low']
        all = df
        df = df.drop(['high', 'low'], axis=1)
        df.fillna(0, inplace=True)
        return all, df, xgb.DMatrix(df), list(high), list(low)

    @staticmethod
    def load_patient_record():
        path = '../scene/高压记录.xlsx'
        df = pd.read_excel(path)
        return df


if __name__ == '__main__':
    d = SensorData.load(path='../scene/data/2.txt')
    # print(data)
    sensor = SensorData()
    record = sensor.record

    # print(record[record['number'] > 20])
    # print(record)
    # print(sensor.get_record_number())

    # sensor.resave_file(100, data)

    #print(sensor.get_record_number())

    df = sensor.load_patient_record()
    print(df)
