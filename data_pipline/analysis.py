from plot import *
from load_file import SensorData
from scipy import stats


if __name__ == '__main__':
    sensor = SensorData()

    k = 15

    metrics = sensor.load_json_metric(k)

    metircs_name = ['bf', 'bs', 'sd', 'df', 'sf', 'rr', 'asd', 'asf', 'ptt']
    #Plot.plot_metrics(metrics, metircs_name)
