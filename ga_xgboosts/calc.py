from data_pipline.plot import Plot
from calculate.load import load_metric
import matplotlib.pyplot as plt
import numpy as np


def rmse(predictions, targets):
    return np.sqrt(((predictions - targets) ** 2).mean())


if __name__ == '__main__':

    keys = ['70', '24']
    models = ['svr', 'liner']
    for key in keys:
        for model in models:
            ph, rh, pl, rl = load_metric(key, model=model)
            #Plot.plot_diff(ph, rh, pl, rl)
            #Plot.bland_altman_plot(ph, rh)
            # plt.show()
            ph = np.asarray(ph)
            rh = np.asarray(rh)
            pl = np.asarray(pl)
            rl = np.asarray(rl)

            diff = ph - rh  # Difference between data1 and data2
            md = np.mean(diff)  # Mean of the difference
            sd = np.std(diff, axis=0)  # Standard deviation of the difference
            rmsd = rmse(ph, rh)
            print(key+'/'+model+'/'+'high--->>>>>'+str(md) + ' ' + str(sd) + ' ' +str(rmsd))

            diff = pl - rl  # Difference between data1 and data2
            md = np.mean(diff)  # Mean of the difference
            sd = np.std(diff, axis=0)  # Standard deviation of the difference
            rmsd = rmse(pl, rl)
            print(key+'/'+model+'/'+'low----->>>>>' + str(md) + ' ' + str(sd) + ' ' + str(rmsd))