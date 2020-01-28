from load_file import SensorData
from plot import Plot


def find_peek(data):
    """
    寻找单路数据的峰值
    """
    # find one serials peeks
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


if __name__ == '__main__':

    sensor = SensorData()
    d = sensor.load_by_number(8, 'regular')

    ir = d.ir1
    x = find_peek(ir)
    Plot.plot_feature_point(ir, x)
