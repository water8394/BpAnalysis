from load_file import SensorData
from plot import *

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

    """
    处理70组数据
    """
    # df = pd.read_table('../scene/record/test_log.txt', sep='\t')
    # df.columns = ['idx', 'name', 'date', 'h1', 'l1', 'h2', 'l2']
    # high, low = [], []
    # for i in range(df.shape[0]):
    #     high.append((int(df.loc[i, 'h1']) + int(df.loc[i, 'h2'])) / 2)
    #     low.append((int(df.loc[i, 'l1']) + int(df.loc[i, 'l2'])) / 2)
    #
    # run = pd.read_excel('../scene/record/run.xlsx', header=None)
    # high = list(run[0])
    # low = list(run[1])
    # middle = int(len(high)/2)
    # print(high)
    # print(low)
    # Plot.plot_single_metric(low[middle:], color='gg')
    # plt.show()



