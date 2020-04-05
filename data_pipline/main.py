from load_file import SensorData
from pre_process import *
from pre_process import _scale
from plot import Plot
from extract import *

"""
数据预处理 && 提取特征值 主类
"""


def main(k):
    sensor = SensorData()

    df = sensor.load_by_number(k, 'data')

    ###################################################################
    # 预处理数据
    df = remove_dc(df)  # 去除dc分量
    df = filter(df)  # 滤波
    df = scale(df)  # 放缩
    df = mean_filter(df)  # 均值滤波
    #df = reverse(df)  # 反转波形
    ###################################################################
    # 显示滤波结果
    plt.figure(figsize=(10, 8))
    fig1 = plt.subplot(111)
    plt.plot(df.ir2, c='r')
    Plot.figture_update(fig1, 'Time (s)', 'Amplitude', 'Pre-process PPG signal', df.ir1)
    plt.subplots_adjust(wspace=0, hspace=0.5)
    plt.show()
    ###################################################################
    # 存储 预处理 文件
    sensor.resave_file(k, df, 'regular')
    ###################################################################
    # 寻找一路峰值点
    d = sensor.load_by_number(k, 'regular')
    pks = find_peek(d.ir1)
    save_peeks(pks, k, default='peak_index')
    # 寻找两路峰值点
    pki = sensor.load_peek_index(k)
    col = d.ir2
    peeks = find_peek_by_other(col, pki)
    val = zip(pki['ir1'].values.tolist(), peeks)
    save_peeks(val, k)
    # 寻找重播波峰值点
    pks = sensor.load_peek_index(k)
    mid_pks = find_mid_peek(d.ir1, pks['ir1'].values.tolist())
    Plot.plot_sigle_peek(d.ir1, mid_pks)
    save_peeks(mid_pks, k, default='mid_peak_index')
    # 寻找波谷点
    d = reverse(d)
    pks = find_peek(d.ir1)
    save_peeks(pks, k, default='vally_peak_index')
    ###################################################################



if __name__ == '__main__':

    number = 27
    main(number)
