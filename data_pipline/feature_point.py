from plot import *

"""
通过峰值点索引来计算特征点
3路峰值点索引 --- 转为 单波形的特征点集合

【峰值索引】
【重播波索引】 ----> 起始点/终止点/波峰点/重播波点
【波谷索引】

"""


def extract_usage_point(peak_index, mid_peak_index, vally_peak_index, k=1):
    """
    提取可用的特征点
    """
    from load_file import SensorData
    sensor = SensorData()
    d = list(sensor.load_by_number(k, 'regular').ir1)

    ret = []
    for i in range(len(vally_peak_index) - 1):
        start = vally_peak_index.at[i, 'ir1']
        end = vally_peak_index.at[i + 1, 'ir1']
        _range = [start, end]
        peak = find_match_point(peak_index, _range)
        mid = find_match_point(mid_peak_index, _range)
        if peak == -1 and mid == -1:
            ret.append([-1, -1, -1, -1])
        elif vaild_middle(peak, mid, end, d) == -1:
            ret.append([start, peak, -1, end])
        else:
            ret.append([start, peak, mid, end])
    return ret


def vaild_middle(peak, middle, end, d):
    """
    验证重播波点是否正确
    """
    if middle == -1:
        return -1
    if d[peak] < d[middle]:
        return -1
    if peak > middle:
        return -1
    diff = (middle - peak) / (end - middle)
    if diff < 0.25 or diff > 3:
        return -1

    return 1


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


def extract_feature_point(k):
    """
    提取特征点并保存
    """
    from load_file import SensorData
    sensor = SensorData()
    d = sensor.load_by_number(k, default='regular')
    pks, mid_pks, vl_pks = sensor.load_all_index(k)
    # Plot.plot_points(d.ir1, pks, mid_pks, vl_pks)
    points = extract_usage_point(pks, mid_pks, vl_pks, k)
    Plot.plot_feature_point(d.ir1, points)
    sensor.save_all_indicators(k, points)


if __name__ == '__main__':
    from load_file import SensorData

    sensor = SensorData()
    number = 49

    extract_feature_point(number)
