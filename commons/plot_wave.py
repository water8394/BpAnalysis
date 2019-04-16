import matplotlib.pyplot as plt
import pandas as pd
import os

from calculate.algorithm import find_peek, find_max, find_mean, regular, baseline

"""
绘制原始数据 

"""
def plot(filename):
    file = pd.read_excel(filename)
    file = file.loc[:,('ir1','ir2')]
    print(file)
    # file.columns = ['ir_1', 'ir_2']
    ir = baseline(file.ir1)
    plt.plot(ir)
    plt.show()





if __name__ == '__main__':
    root = "../data_regular/1_6_16_57.xlsx"
    plot(root)
