from data_pipline import *
from load_file_old import SensorData
from plot import *


def extract_usage_point(peak_index, mid_peak_index, vally_peak_index):
    """
    提取可用的特征点
    """
    ret = []
    for i in range(len(vally_peak_index)-1):
        start = vally_peak_index.at[i, 'ir1']
        end = vally_peak_index.at[i+1, 'ir1']
        _range = [start, end]
        peak = find_match_point(peak_index, _range)
        mid = find_match_point(mid_peak_index, _range)
        if peak != -1 and mid != -1:
            ret.append([start, peak, mid, end])
    return ret


def find_match_point(data, _range):
    """
    提取区间内是否包含特征点
    """
    ret = []
    for i in range(len(data)):
        _val = data.at[i, 'ir1']
        if _range[0] < _val < _range[1]:
            ret.append(_val)
    if len(ret) == 1:
        return ret[0]
    return -1


if __name__ == '__main__':
    sensor = SensorData()
    ids = sensor.get_record_number()
    for k in ids:
        print('current stage: ' + str(k))
        d = sensor.load_by_number(k, default='regular')
        pks, mid_pks, vl_pks = sensor.load_all_index(k)
        #Plot.plot_points(d.ir1, pks, mid_pks, vl_pks)
        points = extract_usage_point(pks, mid_pks, vl_pks)
        #Plot.plot_feature_point(d.ir1, points)
        sensor.save_all_indicators(k, points)
