from plot import *
from load_file import SensorData
from scipy import stats


if __name__ == '__main__':
    sensor = SensorData()

    k = 3
    """
    指标分析
    """
    # metrics = sensor.load_json_metric(k)
    # metircs_name = ['bf', 'bs', 'sd', 'df', 'sf', 'rr', 'asd', 'asf', 'ptt']
    # Plot.plot_metrics(metrics, metircs_name)

    """
    筛选合理的特征片段
    """
    # d = sensor.load_by_number(k, default='regular')
    # part = sensor.load_feature_points(k)
    # Plot.plot_all_and_part_data(d.ir1, part)