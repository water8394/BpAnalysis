import matplotlib.pyplot as plt
import pandas as pd
import os
"""
绘制原始数据

"""
def plot(filename):
    file = pd.read_excel(filename, header=None)

    file.columns = ['ir_1', 'ir_2', 't']
    plt.plot(file['ir_1'])
    plt.show()





if __name__ == '__main__':
    root = "../data_after/12_16_13_50.xlsx"
    plot(root)
