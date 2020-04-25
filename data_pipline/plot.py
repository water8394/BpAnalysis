import matplotlib.pyplot as plt
from scipy import stats

from data_pipline import *
from load_file_dup import SensorData

"""
为了绘制波形
方便实时观察

已经对一些中间过程展示
"""


class Plot:

    @staticmethod
    def get_colors():
        return ['deeppink','dodgerblue','darkorange','limegreen']

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
        # 更新图的坐标
        plt.xlabel(x_str, fontsize=12)
        plt.ylabel(y_str, fontsize=12)
        x_ticks = [x for x in range(len(index_data)) if x % 400 == 0]
        figture.set_xticks(x_ticks)
        figture.set_xticklabels([x // 400 for x in x_ticks], fontsize=10)
        plt.title(title, fontsize=13)

    @staticmethod
    def plot_sigle_peak(df, x):
        #  绘制单路波形峰值
        Plot.init_plot()
        Plot._plot_single_data_peak(df, x)
        plt.show()

    @staticmethod
    def plot_all_peak(df1, df2, x1, x2):
        # 绘制所有峰值点

        Plot.init_plot()
        Plot._plot_single_data_peak(df1, x1)
        Plot._plot_single_data_peak(df2, x2, c='g', m='r^')
        plt.show()

    @staticmethod
    def _plot_single_data_peak(df, x, c='b', m='r*', label='None'):

        #  df 就是 ir的数据， x 就是峰值点数据
        y = []
        if type(x) is pd.DataFrame:
            x = x['ir1'].values.tolist()
            x = [_ for _ in x if _ != -1]
            y = [df[_] for _ in x]
        elif type(x) is list:
            x = [_ for _ in x if _ != -1]
            y = [df[_] for _ in x]
        plt.scatter(x, y, c=m[0], marker=m[1], s=140, label=label)

    @staticmethod
    def plot_points(data, peak_index, mid_peak_index, vally_peak_index):
        # plot 所有的特征点
        Plot.init_plot()
        Plot._plot_single_data_peak(data, peak_index, m='r*')
        Plot._plot_single_data_peak(data, mid_peak_index, m='g^')
        Plot._plot_single_data_peak(data, vally_peak_index, m='mP')
        plt.show()

    @staticmethod
    def plot_feature_point(data, point_list):
        # 绘制波形特征点
        Plot.init_plot()
        plt.plot(data)
        x1, x2, x3, x4 = [], [], [], []
        for points in point_list:
            x1.append(points[0])
            x2.append(points[1])
            x3.append(points[2])
            x4.append(points[3])
        Plot._plot_single_data_peak(data, x1, m='r*', label='vally')
        Plot._plot_single_data_peak(data, x2, m='g^', label='peak')
        Plot._plot_single_data_peak(data, x3, m='mP', label='middle')
        Plot._plot_single_data_peak(data, x4, m='r*', label='vally')
        plt.legend()
        plt.show()

    @staticmethod
    def plot_single_metric(metric, step=10, color='bm'):
        # 绘制一个指标 柱状图
        skew = 'Skew: ' + str(round(float(stats.skew(metric)), 2))
        _mean = np.mean(metric)
        _median = np.median(metric)
        _max = max(metric)
        _min = min(metric)
        _range = _max - _min
        step_val = _range / step
        _val = [0] * (step + 1)
        for i in metric:
            n = int((i - _min) / step_val)
            _val[n] += 1
        x = [str(int(_min + _ * step_val)) for _ in range(11)]
        _mean_x, _median_x = 0, 0
        _mean_y, _median_y = 0, 0
        for i, _x in enumerate(x):
            if int(_x) < _mean < int(_x) + step_val:
                _mean_x = i
                _mean_y = _val[i]
            if int(_x) < _median < int(_x) + step_val:
                _median_x = i
                _median_y = _val[i]

        plt.bar(range(11), _val, tick_label=x, fc=color[0])
        if _mean_x == _median_x:
            width = 0.45
            # plt.bar(_mean_x - width / 2, _mean_y, width=width, fc='m', label='mean')
            plt.bar(_mean_x, _mean_y, fc=color[1], label='mean')
            # plt.bar(_median_x + width / 2, _median_y, width=width, fc='g', label='median')
        else:
            plt.bar(_mean_x, _mean_y, fc=color[1], label='mean')
            # plt.bar(_median_x, _median_y, fc='g', label='median')
            pass

        # plt.text(1, max(_val) - 1, s=skew, fontsize=10, ha="center", va="center",
        # bbox=dict(boxstyle="square", ec=(1., 0.5, 0.5), fc=(1., 0.8, 0.8), ))
        plt.legend()

    @staticmethod
    def plot_metrics(metrics, names, row=3, col=3):
        if len(metrics) != row * col:
            print('subplot number error')

        plt.figure(figsize=(18, 10), dpi=100)

        for i in range(len(names)):
            plt.subplot(row, col, i + 1)
            plt.title('Paramter: ' + names[i], fontsize=10)
            Plot.plot_single_metric(metrics[names[i]])
        plt.subplots_adjust(wspace=0.4, hspace=0.4)
        plt.show()

    @staticmethod
    def plot_all_and_part_data(data, part):
        plt.plot(data, c='b')
        x1, x2, x3, x4 = [], [], [], []
        for i in range(part.shape[0]):
            plt.plot(data[part.loc[i, 'f1']: part.loc[i, 'f4']], c='y', linewidth=3, alpha=0.8)
            x1.append(part.loc[i, 'f1'])
            x2.append(part.loc[i, 'f2'])
            x3.append(part.loc[i, 'f3'])
            x4.append(part.loc[i, 'f4'])
        Plot._plot_single_data_peak(data, x1, m='r*')
        Plot._plot_single_data_peak(data, x2, m='r^')
        Plot._plot_single_data_peak(data, x3, m='rP')
        Plot._plot_single_data_peak(data, x4, m='r*')

        plt.show()

    @staticmethod
    def plot_diff(pred_h, real_h, pred_l, real_l):
        plt.figure(figsize=(15, 6))
        plt.plot(pred_h, color='deeppink', marker='*', markersize=7, label='Predict Systolic')
        plt.plot(real_h, color='dodgerblue', marker='o', markersize=7, label='Real Systolic')
        plt.plot(pred_l, color='darkorange', marker='*', markersize=7, label='Predict Diastolic')
        plt.plot(real_l, color='limegreen', marker='o', markersize=7, label='Real Diastolic')
        plt.legend()
        plt.show()

    @staticmethod
    def bland_altman_plot(data1, data2):
        # 绘制 ba图
        data1 = np.asarray(data1)
        data2 = np.asarray(data2)
        mean = np.mean([data1, data2], axis=0)
        diff = data1 - data2  # Difference between data1 and data2
        md = np.mean(diff)  # Mean of the difference
        sd = np.std(diff, axis=0)  # Standard deviation of the difference

        print('md:' + str(md))
        print('sd:' + str(sd))
        plt.scatter(mean, diff, alpha=0.8, color='deeppink')
        plt.axhline(md, color='dodgerblue', linestyle='--', alpha=0.7)
        plt.axhline(md + 1.96 * sd, color='tomato', linestyle='--', alpha=0.7)
        plt.axhline(md - 1.96 * sd, color='tomato', linestyle='--', alpha=0.7)

        plt.show()

    @staticmethod
    def ba_plot(data1, data2, data3, data4):
        Plot.bland_altman_plot(data1, data2)
        Plot.bland_altman_plot(data3, data4)
        plt.show()

    @staticmethod
    def bar_plot(td):
        colors = Plot.get_colors()
        names = ['liner', 'svr', 'bp', 'ga_xgboost']
        x = np.arange(3)
        width = 0.12
        fig, ax = plt.subplots()

        for i, name in enumerate(names):
            value_set = list(td[td['model'] == name].iloc[0])[-3:]
            value_set = [abs(_) for _ in value_set]
            ax.bar(x + 2 * width - i * width, value_set, width * 0.8, label=name.upper())

        labels = ['MAE', 'SD', 'RSME']
        ax.set_xticklabels(labels)
        ax.set_xticks(x)
        plt.legend()
        plt.show()





if __name__ == '__main__':
    list = [1, 3, 2, 5, 6, 8, 3, 1]
    # Plot.show(data=list)

    sensor = SensorData()
    d = sensor.load_by_number(1)
    # Plot.show_wave(d, s='ir1')

    ph = [4, 6, 7]
    rh = [5, 4, 5]
    pl = [14, 16, 17]
    rl = [15, 14, 16]
    Plot.plot_diff(ph, rh, pl, rl)
