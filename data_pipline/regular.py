from load_file import SensorData
from pre_process import *
from plot import Plot

if __name__ == '__main__':

    sensor = SensorData()
    numbers = sensor.get_record_number()

    for k in numbers:

        df = sensor.load_by_number(k)
        ###################################################################
        # 原始数据
        plt.figure(figsize=(10, 8))
        fig1 = plt.subplot(211)
        plt.plot(df.ir1, c='b')
        Plot.figture_update(fig1, 'Time (s)','Amplitude','Raw PPG signal', df.ir1)
        ###################################################################
        # 处理数据
        df = remove_dc(df)
        df = filter(df)
        ###################################################################
        # 结果数据
        fig2 = plt.subplot(212)
        plt.plot(df.ir1, c='r')
        Plot.figture_update(fig2, 'Time (s)','Amplitude','Pre-process PPG signal', df.ir1)
        plt.subplots_adjust(wspace=0, hspace=0.5)
        # plt.show()
        ###################################################################
        # 存储文件
        #sensor.resave_file(k, df, 'regular')
        ###################################################################
