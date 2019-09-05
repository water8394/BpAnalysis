import matplotlib.pyplot as plt
import pandas as pd

def read_table(path):
    table = pd.read_excel(path)
    return table


if __name__ == '__main__':

    file = '12_26_14_48.xlsx'
    raw_data_path = '../data_raw/' + file
    regular_data_path = '../data_regular/' + file
    raw_table = read_table(raw_data_path)
    regular_table = read_table(regular_data_path)
    # plt.plot(raw_table.ir_1)
    plt.plot(regular_table.ir2)
    plt.show()