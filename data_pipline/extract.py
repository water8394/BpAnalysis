from load_file import SensorData
from plot import Plot


def find_peek(data):
    """
    寻找单路数据的峰值
    """
    amplitude = 0.5
    peek_list = []
    max_value = data.max()
    threshold = amplitude * max_value
    for i in range(2, len(data) - 2):
        if data[i] > data[i + 1] and data[i] > data[i - 1] and data[i] > threshold:
            if len(peek_list) > 1:
                diff = i - peek_list[-1]
            else:
                diff = 101
            if diff < 100:
                old = data[peek_list[-1]]
                new = data[i]
                if old > new:
                    continue
                else:
                    peek_list.pop()
                    peek_list.append(i)
            else:
                peek_list.append(i)

    return peek_list


def save_peeks(data, k):
    """
    保存数据的峰值点索引
    """
    path = SensorData._combine_path(k, default='peek_index')
    with open(path, 'w+') as f:
        f.seek(0)
        for d in data:
            if type(d) is int:
                f.writelines(str(d) + '\n')
            else:
                f.writelines(','.join([str(_) for _ in d]) + '\n')
        f.truncate()


if __name__ == '__main__':
    sensor = SensorData()
    ids = sensor.get_record_number()
    for k in ids:

        d = sensor.load_by_number(k, 'regular')
        Plot.show(d.ir1, d.ir2)
        # col = d.ir1
        # x = find_peek(col)
        # Plot.plot_feature_point(col, x)
        # save_peeks(x, k)
