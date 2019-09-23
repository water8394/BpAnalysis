import matplotlib.pyplot as plt
import pandas as pd


"""
绘制excel中的数据波形


"""

if __name__ == '__main__':

    df = pd.read_excel("../old/data_regular/1_6_16_41.xlsx")
    print(df.ir1)
    fig2 = plt.subplot(111)
    plt.plot(df.ir1, c='b')
    plt.plot(df.ir2, c='r')
    plt.xlabel('Time(s)', fontsize=18)
    plt.ylabel('Amptitude', fontsize=18)
    x_ticks = [x for x in range(len(df.ir2)) if x % 400 == 0]
    fig2.set_xticks(x_ticks)
    fig2.set_xticklabels([x // 400 for x in x_ticks], fontsize=15)
    # plt.title('After Pre-process PluseWave', fontsize=20)
    plt.subplots_adjust(wspace=0, hspace=0.5)
    plt.show()

