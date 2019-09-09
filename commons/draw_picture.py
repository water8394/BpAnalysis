import matplotlib.pyplot as plt
import pandas as pd

def read_table(path):
    table = pd.read_table(path, sep=',',header=None)
    table.columns = ['red1','ir1','red2','ir2']
    return table


if __name__ == '__main__':

    file = '14_50_02.txt'
    raw_data_path = '../new_sensor/raw/' + file
    # regular_data_path = '../data_regular/' + file

    raw_table = read_table(raw_data_path)
    # regular_table = read_table(regular_data_path)

    plt.plot(raw_table.ir1)
    # plt.plot(regular_table.ir2)
    plt.show()