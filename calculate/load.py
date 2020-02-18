import xgboost as xgb
from sklearn.model_selection import train_test_split

from data_pipline import *
from load_file import SensorData


def create_table(name):
    if name == '70':
        indicator = pd.read_table('../scene/record/indicators.txt', header=None)
        record = pd.read_table('../scene/record/test_log.txt', header=None)
        indicator.columns = ['name', 'ptt', 'vally_ptt', 'rr1', 'rr2', 'sum1', 'up1', 'down1', 'sum2', 'up2', 'down2']
        record.columns = ['idx', 'stu', 'name', 'h1', 'l1', 'h2', 'l2']
        h, l = [], []
        for i in range(record.shape[0]):
            h.append(int((int(record.loc[i, 'h1']) + int(record.loc[i, 'h2'])) / 2))
            l.append(int((int(record.loc[i, 'l1']) + int(record.loc[i, 'l2'])) / 2))
        record['h1'] = h
        record['l1'] = l
        df = pd.merge(indicator, record, on='name')
        df = df[['name', 'ptt', 'vally_ptt', 'rr1', 'rr2', 'sum1', 'up1', 'down1', 'sum2', 'up2', 'down2', 'h1', 'l1']]
        df = df.rename(columns={"h1": "high", "l1": "low"})
        return df
    else:
        sensor = SensorData()
        ids = sensor.get_record_number()
        record = sensor.record
        metric_name = ['bf', 'bs', 'sd', 'df', 'sf', 'rr', 'asd', 'asf', 'ptt']
        columns = ['bf', 'bs', 'sd', 'df', 'sf', 'rr', 'asd', 'asf', 'ptt', 'high', 'low']
        df = pd.DataFrame(columns=columns)
        for k in ids:
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
        return df


def load(name='70', bp='high', ratio=0.5):
    df = create_table(name)
    if name == '70':
        train_X, test_X, train_Y, test_Y = train_test_split(
            df[['ptt', 'vally_ptt', 'rr1', 'rr2', 'sum1', 'up1', 'down1', 'sum2', 'up2', 'down2']], df[bp],
            test_size=ratio)
        return train_X, test_X, train_Y, test_Y
    else:
        train_X, test_X, train_Y, test_Y = train_test_split(
            df[['bf', 'bs', 'sd', 'df', 'sf', 'rr', 'asd', 'asf', 'ptt']], df[bp], test_size=ratio)
        return train_X, test_X, train_Y, test_Y


def load_all(name='70'):
    df = create_table(name)
    high, low = df.loc[:, 'high'], df.loc[:, 'low']
    if name == '70':
        df = df.drop(['name', 'high', 'low'], axis=1)
    else:
        df = df.drop(['high', 'low'], axis=1)
    return xgb.DMatrix(df), list(high), list(low)


def dump_value(a, b, name):
    l = len(a)
    with open('../scene/result/' + name + '.txt', 'w') as f:
        for i in range(l):
            inp = str(a[i]) + ',' + str(b[i]) + '\n'
            f.writelines(inp)


if __name__ == '__main__':
    load('run')
