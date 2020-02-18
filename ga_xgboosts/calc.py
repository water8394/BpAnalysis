from data_pipline.plot import Plot
from calculate.load import load_metric
import matplotlib.pyplot as plt


if __name__ == '__main__':

    ph, rh, pl, rl = load_metric('70')
    #Plot.plot_diff(ph, rh, pl, rl)
    Plot.bland_altman_plot(ph, rh)
    plt.show()
