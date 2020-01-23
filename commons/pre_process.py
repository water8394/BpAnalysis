import matplotlib.pyplot as plt
import pandas as pd

from wavelet import wavelet_filter

"""
2019-9-5
对数据做预处理,过程包括:
    1. 去除DC分量
    2. 均值+小波滤波
    3. 去除基线漂移
    4. 归一化波形
"""


def remove_dc(table):
    # 1. 去除 DC 分量
    min_ir1 = min(table.ir1)
    min_ir2 = min(table.ir2)
    min_red1 = min(table.red1)
    min_red2 = min(table.red2)
    ir1 = [_ - min_ir1 for _ in table.ir1]
    ir2 = [_ - min_ir2 for _ in table.ir2]
    red1 = [_ - min_red1 for _ in table.red1]
    red2 = [_ - min_red2 for _ in table.red2]
    table.ir1 = ir1
    table.ir2 = ir2
    table.red1 = red1
    table.red2 = red2
    return table


def filter(table):
    # 2. 均值 + 小波滤波

    # 均值
    table.ir1 = table.ir1.rolling(window=30).mean()
    table.ir2 = table.ir2.rolling(window=30).mean()
    table.red1 = table.red1.rolling(window=30).mean().rolling(window=30).mean()
    table.red2 = table.red2.rolling(window=30).mean().rolling(window=30).mean()
    table = table[120:]
    ################################################
    # 反转波形
    ir1_max = max(table.ir1)
    print(ir1_max)
    ir2_max = max(table.ir2)
    red1_max = max(table.red1)
    red2_max = max(table.red2)
    ir1 = [ir1_max - _ for _ in table.ir1]
    ir2 = [ir2_max - _ for _ in table.ir2]
    red1 = [red1_max - _ for _ in table.red1]
    red2 = [red2_max - _ for _ in table.red2]
    ################################################
    # 小波滤波
    ir1 = wavelet_filter(ir1)
    ir2 = wavelet_filter(ir2)
    red1 = wavelet_filter(red1)
    red2 = wavelet_filter(red2)

    min_table_length = min(min(min(len(ir1), len(ir2)),len(red1)),len(red2))
    ir1 = ir1[0:min_table_length]
    ir2 = ir2[0:min_table_length]
    red1 = red1[0:min_table_length]
    red2 = red2[0:min_table_length]

    table.ir1 = ir1
    table.ir2 = ir2
    table.red1 = red1
    table.red2 = red2
    return table


if __name__ == '__main__':
    df = pd.read_table('../new_sensor/raw/14_50_02.txt', sep=',', header=None)
    df.columns = ['red1', 'ir1', 'red2', 'ir2']
    df = df[50:len(df) // 2 - 1]
    df.reset_index(drop=True, inplace=True)
    ###################################################################
    # 原始数据
    plt.figure()
    fig1 = plt.subplot(211)
    plt.plot(df.ir1, c='b')
    plt.xlabel('Time (s)', fontsize=18)
    plt.ylabel('Amplitude', fontsize=18)
    x_ticks = [x for x in range(len(df.ir1)) if x % 400 == 0]
    fig1.set_xticks(x_ticks)
    fig1.set_xticklabels([x // 400 for x in x_ticks], fontsize=15)
    plt.title('Raw PPG signal', fontsize=20)

    ###################################################################

    # 处理数据
    df = remove_dc(df)
    df = filter(df)
    ###################################################################
    # 结果数据
    fig2 = plt.subplot(212)
    plt.plot(df.red2, c='r')
    # plt.plot(df.red2, c='r')
    plt.xlabel('Time (s)', fontsize=18)
    plt.ylabel('Amplitude', fontsize=18)
    x_ticks = [x for x in range(len(df.ir2)) if x % 400 == 0]
    fig2.set_xticks(x_ticks)
    fig2.set_xticklabels([x // 400 for x in x_ticks], fontsize=15)
    plt.title('Pre-process PPG signal', fontsize=20)
    plt.subplots_adjust(wspace=0, hspace=0.5)
    plt.show()
    ###################################################################
