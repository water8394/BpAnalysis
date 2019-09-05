import matplotlib.pyplot as plt
import pandas as pd
import os


"""
绘制原始数据 

"""
def plot(filename):
    file = pd.read_excel(filename)
    file = file.loc[:,('ir1','ir2')]
    print(file)
    # file.columns = ['ir_1', 'ir_2']
    # ir = baseline(file.ir1)
    # plt.plot(ir)
    plt.show()

def plot_txt(filename):
    file = pd.read_table(filename, sep=',',header=None)
    file.columns = ['red1','ir1', 'red2', 'ir2']
    plt.plot(file.red2)
    plt.show()




if __name__ == '__main__':
    root = "../data-bak/20_53_21.txt"
    plot_txt(root)
