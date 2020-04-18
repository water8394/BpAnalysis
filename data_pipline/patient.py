from load_file import *
import matplotlib.pyplot as plt


def plot_distribute(values, is_high=1):
    _range = []
    if is_high:
        _range = [100, 110, 120, 130, 140]
    else:
        _range = [60, 70, 80, 90]

    ret = [0] * len(_range)
    for v in values:
        k = v - v % 10
        for i, value in enumerate(_range):
            if k == value:
                ret[i] += 1
    print(ret)
    width = 0.45
    fig, ax = plt.subplots()
    x = range(len(_range))
    ax.bar(x + width / 2, ret, width=width)
    ax.set_xticklabels(_range)
    ax.set_xticks(x)
    plt.show()


def load_metric():
    df = SensorData().load_patient_record()
    number = list(df['number'])
    sensor = SensorData()
    return sensor.load_all_metric(number)


if __name__ == '__main__':
    from load_file import SensorData

    df = SensorData().load_patient_record()

    high = list(df['high'])

    all, df, m, h, l = load_metric()
    print(all)
