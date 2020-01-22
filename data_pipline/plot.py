import matplotlib.pyplot as plt

from load_file import SensorData


class Plot:

    @staticmethod
    def show(data):
        plt.plot(data)
        plt.show()

    @staticmethod
    def show_wave(dataframe, s):
        Plot.show(dataframe[s])


if __name__ == '__main__':
    list = [1, 3, 2, 5, 6, 8, 3, 1]
    # Plot.show(data=list)

    sensor = SensorData()
    d = sensor.load_by_number(1)
    Plot.show_wave(d, s='ir1')
