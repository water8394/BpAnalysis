from data_pipline import *
import matplotlib.pyplot as plt

from load_file import SensorData


class Plot:

    @staticmethod
    def init_plot():
        plt.figure(figsize=(15, 6))

    @staticmethod
    def show(*data):
        plt.figure(figsize=(14, 6))
        for d in data:
            plt.plot(d)
        plt.show()

    @staticmethod
    def show_wave(dataframe, s):
        Plot.show(dataframe[s])

    @staticmethod
    def figture_update(figture, x_str, y_str, title, index_data):
        plt.xlabel(x_str, fontsize=12)
        plt.ylabel(y_str, fontsize=12)
        x_ticks = [x for x in range(len(index_data)) if x % 400 == 0]
        figture.set_xticks(x_ticks)
        figture.set_xticklabels([x // 400 for x in x_ticks], fontsize=10)
        plt.title(title, fontsize=13)

    @staticmethod
    def plot_sigle_peek(df, x):
        Plot.init_plot()
        Plot._plot_single_data_peek(df, x)
        plt.show()

    @staticmethod
    def plot_all_peek(df1, df2, x1, x2):
        Plot.init_plot()
        Plot._plot_single_data_peek(df1, x1)
        Plot._plot_single_data_peek(df2, x2, c='g', m='r^')
        plt.show()

    @staticmethod
    def _plot_single_data_peek(df, x, c='b', m='r*'):
        plt.plot(df, c=c)
        if type(x) is pd.DataFrame:
            x = x['ir1'].values.tolist()
            y = [df[_] for _ in x]
        elif type(x) is list:
            x = [_ for _ in x if _ != -1]
            y = [df[_] for _ in x]
        plt.scatter(x, y, c=m[0], marker=m[1])


if __name__ == '__main__':
    list = [1, 3, 2, 5, 6, 8, 3, 1]
    # Plot.show(data=list)

    sensor = SensorData()
    d = sensor.load_by_number(1)
    Plot.show_wave(d, s='ir1')
