from load_file import SensorData
from plot import Plot
from pre_process import *


def find_peek(data):
    """
    寻找单路数据的峰值
    """
    amplitude = 0.7
    peek_list = []
    max_value = data.max()
    threshold = amplitude * max_value
    for i in range(2, len(data) - 2):
        if data[i] > data[i + 1] and data[i] > data[i - 1] and data[i] > threshold:
            if len(peek_list) > 1:
                diff = i - peek_list[-1]
            else:
                diff = 101
            if diff < 100:
                old = data[peek_list[-1]]
                new = data[i]
                if old > new:
                    continue
                else:
                    peek_list.pop()
                    peek_list.append(i)
            else:
                peek_list.append(i)

    return peek_list


def find_mid_peek(data, peek_index):
    """
    寻找所有重播波点
    """
    ret = []
    for i in range(len(peek_index)-2):
        part = data[peek_index[i]+10: peek_index[i+1]-10]
        ret.append(find_sigle_peak(part))
    return ret


def find_sigle_peak(data):
    """
    在一个区间段内寻找重播波点
    """
    ret = -1
    _max = -1
    idx = data.index[20:-5]
    for i in idx:
        if data[i] > _max and data[i] > data[i-3] and data[i] > data[i+3]:
            _max = data[i]
            ret = i
    return ret



def find_peek_by_other(data, peek_index):
    """
    通过一路数据的 peek 来寻来另外一路的peek
    """
    idx = []
    for i in range(peek_index.shape[0]):
        val = int(peek_index.at[i, 'ir1'])
        idx.append([val - 50, val + 50])
    ret = []
    for rng in idx:
        part = data[rng[0]: rng[1]]
        ret.append(max_index(part))
    return ret


def max_index(data):
    """
    DataFrame 区间内最大值的索引
    """
    _max = -10000
    ret = -1
    idx = data.index
    for i in idx:
        if data[i] > _max:
            ret = i
            _max = data[i]
    return ret


def save_peeks(data, k, default='peak_index'):
    """
    保存数据的峰值点索引
    """
    path = SensorData._combine_path(k, default=default)
    with open(path, 'w+') as f:
        f.seek(0)
        for d in data:
            if type(d) is int:
                f.writelines(str(d) + '\n')
            else:
                f.writelines(','.join([str(_) for _ in d]) + '\n')
        f.truncate()


if __name__ == '__main__':
    sensor = SensorData()
    ids = sensor.get_record_number()
    """
    找双路 PPG 峰值点
    """
    # for k in ids:
    #     # k = 1
    #     print('peek ---> ' + str(k))
    #     d = sensor.load_by_number(k, 'regular')
    #     pki = sensor.load_peek_index(k)
    #     col = d.ir2
    #     peeks = find_peek_by_other(col, pki)
    #
    #     #Plot.plot_all_peek(d.ir1, d.ir2, pki, peeks)
    #     val = zip(pki['ir1'].values.tolist(), peeks)
    #     save_peeks(val, k)

    """
    找重播波峰值点
    """
    # for k in ids:
    #     d = sensor.load_by_number(k, 'regular')
    #     pks = sensor.load_peek_index(k)
    #     mid_pks = find_mid_peek(d.ir1, pks['ir1'].values.tolist())
    #     Plot.plot_sigle_peek(d.ir1, mid_pks)
        #save_peeks(mid_pks, k, default='mid_peak_index')

    """
    找 波谷点
    """
    # for k in ids:
    #     d = sensor.load_by_number(k, 'regular')
    #     d = reverse(d)
    #     pks = find_peek(d.ir1)
    #     save_peeks(pks, k, default='vally_peak_index')
