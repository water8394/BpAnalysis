from load_file import SensorData
from plot import Plot


def remove_part(data, r):
    data_drop = data.drop(index=range(r[0], r[1]))
    data_drop.index = range(0, data_drop.shape[0])
    return data_drop


if __name__ == '__main__':
    sensor = SensorData()
    numbers = sensor.get_record_number()

    d = sensor.load_by_number(5)
    # Plot.show_wave(d, 'red1')

    d2 = remove_part(d, [0, 100])
    print(d2)
    Plot.show_wave(d2, 'ir1')
