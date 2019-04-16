import pandas as pd
import matplotlib.pyplot as plt
from calculate.algorithm import baseline
import os

def filter(filename):
    file = pd.read_excel(filename, header=None)

    file.columns = ['ir_1', 'ir_2', 't']
    ir1 = baseline(file.ir_1)
    ir2 = baseline(file.ir_2)
    dataframe = pd.DataFrame(columns=['ir1','ir2'])
    max_l = max(len(ir1), len(ir2))
    for i in range(max_l):
        i1 = ir1[i] if i < len(ir1) else pd.NaT
        i2 = ir2[i] if i < len(ir2) else pd.NaT
        dataframe.loc[i] = [i1,i2]
    # plt.plot(ir1)
    # plt.plot(ir2)
    # plt.show()
    name = filename.split('/')[-1]
    dataframe.to_excel('../data_regular/'+name)


if __name__ == '__main__':

    for path in os.listdir('../data_after'):
        filter('../data_after/' + path)
        print('finish for ->',path)