import matplotlib.pyplot as plt

from load_file import SensorData


class Plot:

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
    def plot_feature_point(df, x):
        plt.plot(df, c='b')
        y = [df[_] for _ in x]
        plt.scatter(x, y, c='r', marker='*')
        plt.show()


if __name__ == '__main__':
    list = [1, 3, 2, 5, 6, 8, 3, 1]
    # Plot.show(data=list)

    sensor = SensorData()
    d = sensor.load_by_number(1)
    Plot.show_wave(d, s='ir1')
