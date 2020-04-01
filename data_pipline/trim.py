from load_file import SensorData
from plot import Plot

""""
    修剪数据片段，删除不准确的部分
"""

def remove_part(data, r):
    start = r[0]
    end = r[1] if r[1] != -1 else len(data)-1
    data_drop = data.drop(index=range(start, end))
    data_drop.index = range(0, data_drop.shape[0])
    return data_drop


if __name__ == '__main__':
    sensor = SensorData()

    k = 27
    re_save = 0  # 0: origin  / 1: trim
    d = sensor.load_by_number(k, default='data')

    print(d.ir1)
    if not re_save:
        Plot.show(d.ir1, d.ir2)
    else:
        d2 = remove_part(d, [0, 100])
        #Plot.show(d2.ir1, d2.ir2)
        sensor.resave_file(k, d2, default='data')
