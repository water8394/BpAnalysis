from load_file import SensorData

if __name__ == '__main__':
    data = SensorData.load(path='../scene/data/2.txt')
    # print(data)
    sensor = SensorData()
    record = sensor.record
    print(record[record['number'] > 20])

