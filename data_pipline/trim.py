from load_file import SensorData
from plot import Plot


def remove(data, r):
    pass


if __name__ == '__main__':

    sensor = SensorData()
    numbers = sensor.get_record_number()

    for number in numbers:
        d = sensor.load_by_number(number)
        Plot.show_wave(d, 'red1')
