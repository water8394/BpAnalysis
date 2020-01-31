from plot import *
from load_file import SensorData

if __name__ == '__main__':
    sensor = SensorData()

    k = 1

    metrics = sensor.load_json_metric(k)

    plt.scatter(range(len(metrics['bf'])), metrics['bf'])
    plt.show()