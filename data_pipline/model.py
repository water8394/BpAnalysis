from data_pipline import *
from load_file import SensorData


def load_data():
    sensor = SensorData()
    ids = sensor.get_record_number()
    record = sensor.record
    metric_name = ['bf', 'bs', 'sd', 'df', 'sf', 'rr', 'asd', 'asf', 'ptt']
    columns = ['bf', 'bs', 'sd', 'df', 'sf', 'rr', 'asd', 'asf', 'ptt', 'high', 'low']
    df = pd.DataFrame(columns=columns)
    for k in ids:
        metric = sensor.load_json_metric(k)
        high, low = int(record[record['number']==k]['high']), int(record[record['number']==k]['low'])
        l = []
        for name in metric_name:
            l.append(np.mean(metric[name]))
        l.append(high)
        l.append(low)
        insert_row = dict(zip(columns, l))
        print(insert_row)
        df.loc[df.shape[0]] = insert_row
    return df


if __name__ == '__main__':
    data = load_data()
    print(data)