from data_pipline.plot import Plot
from calculate.load import load_metric
import matplotlib.pyplot as plt
import numpy as np

"""
计算diff
"""


def remove_max(d1, d2):
    r1, r2 = [], []
    for i in range(len(d1)):
        if abs(d1[i]-d2[i]) < 10:
            r1.append(d1[i])
            r2.append(d2[i])
    return r1, r2

def rmse(predictions, targets):
    return np.sqrt(((predictions - targets) ** 2).mean())


if __name__ == '__main__':
    """
    
    绘制  趋势图 和  BA图
    
    """

    keys = ['']
    models = ['patient']

    ph, rh, pl, rl = load_metric('', 'patient')
    Plot.plot_diff(ph, rh, pl, rl)
    ph, rh = remove_max(ph, rh)
    pl, rl = remove_max(pl, rl)
    Plot.bland_altman_plot(ph, rh)
    Plot.bland_altman_plot(pl, rl)

    # for key in keys:
    #     for model in models:
    #         ph, rh, pl, rl = load_metric(key)
    #         #Plot.plot_diff(ph, rh, pl, rl)
    #         #Plot.bland_altman_plot(ph, rh)
    #         # plt.show()
    #         ph = np.asarray(ph)
    #         rh = np.asarray(rh)
    #         pl = np.asarray(pl)
    #         rl = np.asarray(rl)
    #
    #         diff = ph - rh  # Difference between data1 and data2
    #         md = np.mean(diff)  # Mean of the difference
    #         sd = np.std(diff, axis=0)  # Standard deviation of the difference
    #         rmsd = rmse(ph, rh)
    #         print(key+'/'+model+'/'+'high--->>>>>'+str(md) + ' ' + str(sd) + ' ' +str(rmsd))
    #
    #         diff = pl - rl  # Difference between data1 and data2
    #         md = np.mean(diff)  # Mean of the difference
    #         sd = np.std(diff, axis=0)  # Standard deviation of the difference
    #         rmsd = rmse(pl, rl)
    #         print(key+'/'+model+'/'+'low----->>>>>' + str(md) + ' ' + str(sd) + ' ' + str(rmsd))