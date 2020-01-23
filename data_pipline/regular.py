from pre_process import *
from load_file import SensorData

if __name__ == '__main__':

    sensor = SensorData()
    df = sensor.load_by_number(1)
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

