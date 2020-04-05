import json

from load_file import SensorData

"""
根据计算出来的 特征点进一步得到指标

"""


def cal_ptt(pks_index, s_index):
    ret = []
    for _val in s_index:
        for _k in pks_index:
            if abs(_val - _k) < 100:
                ret.append(_val - _k)

    up, down = 0, 0
    for _val in ret:
        if _val > 0:
            up += 1
        else:
            down += 1
    if up >= down:
        return [_ for _ in ret if _ > 0]
    return [_ for _ in ret if _ < 0]


def dump_metrics_to_json(metrics, file):
    data = {
        'bf': metrics[0],
        'bs': metrics[1],
        'sd': metrics[2],
        'df': metrics[3],
        'sf': metrics[4],
        'rr': metrics[5],
        'asd': metrics[6],
        'asf': metrics[7],
        'ptt': metrics[8],
    }
    json.dump(data, file)


def extract_metric(k):
    sensor = SensorData()
    d = sensor.load_by_number(k, default='regular')
    pks = sensor.load_peek_index(k).ir2

    ir1 = d.ir1
    f = sensor.load_feature_points(k)
    bf, bs, sd, df, sf, rr, asd, asf = [], [], [], [], [], [], [], []
    metric_list = [bf, bs, sd, df, sf, rr, asd, asf]
    s = []
    for i in range(f.shape[0]):
        l = list(f.loc[i])
        if l[1] == -1 and l[2] == -1:
            pass
        elif l[2] == -1:
            bf.append(l[3] - l[0])
            bs.append(l[1] - l[0])
            sd.append(0)
            df.append(0)
            sf.append(l[3] - l[1])
            asd.append(0)
            asf.append(ir1[l[1]] - ir1[l[3]])
        else:
            bf.append(l[3] - l[0])
            bs.append(l[1] - l[0])
            sd.append(l[2] - l[1])
            df.append(l[3] - l[2])
            sf.append(l[3] - l[1])
            asd.append(ir1[l[1]] - ir1[l[2]])
            asf.append(ir1[l[1]] - ir1[l[3]])

        s.append(l[1])

    # 计算 rr
    for i in range(f.shape[0] - 1):
        l1 = list(f.loc[i])
        l2 = list(f.loc[i + 1])
        if l1[3] == l2[0]:
            rr.append(l2[1] - l1[1])

    # 计算ptt
    ptt = cal_ptt(pks, s)
    metric_list.append(ptt)

    # 保存 metric
    with open('../scene/metric/' + str(k) + '.json', 'w') as file:
        dump_metrics_to_json(metric_list, file)

    metric = []
    for group in metric_list:
        if len(group) != 0:
            metric.append(abs(sum(group) / len(group)))
        else:
            metric.append(0)
    print(metric)


if __name__ == '__main__':
    sensor = SensorData()
    ids = sensor.get_record_number()
    for k in ids:
        # k = 3
        print('current metric: ' + str(k))
        d = sensor.load_by_number(k, default='regular')
        pks = sensor.load_peek_index(k).ir2

        ir1 = d.ir1
        f = sensor.load_feature_points(k)
        bf, bs, sd, df, sf, rr, asd, asf = [], [], [], [], [], [], [], []
        metric_list = [bf, bs, sd, df, sf, rr, asd, asf]
        s = []
        for i in range(f.shape[0]):
            l = list(f.loc[i])
            bf.append(l[3] - l[0])
            bs.append(l[1] - l[0])
            sd.append(l[2] - l[1])
            df.append(l[3] - l[2])
            sf.append(l[3] - l[1])
            asd.append(ir1[l[1]] - ir1[l[2]])
            asf.append(ir1[l[1]] - ir1[l[3]])

            s.append(l[1])

        for i in range(f.shape[0] - 1):
            l1 = list(f.loc[i])
            l2 = list(f.loc[i + 1])
            if l1[3] == l2[0]:
                rr.append(l2[1] - l1[1])

        ptt = cal_ptt(pks, s)
        metric_list.append(ptt)

        with open('../scene/metric/' + str(k) + '.json', 'w') as file:
            dump_metrics_to_json(metric_list, file)

        metric = []
        for group in metric_list:
            if len(group) != 0:
                metric.append(abs(sum(group) / len(group)))
            else:
                metric.append(0)
        print(metric)
