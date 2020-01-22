from data_pipline import *


class SensorData:

    def __init__(self):
        self.data = None
        self.record = None

        self._load_record()

    def _load(self, path, form='txt'):
        self.data = self.load(path, form)

    def _load_record(self):
        self.record = pd.read_excel('../scene/记录表.xlsx')

    @staticmethod
    def load(path, form='txt'):

        data = pd.DataFrame

        if form == 'txt':
            data = pd.read_table(path, header=None, sep=',')
        elif form == 'excel':
            data = pd.read_excel(path, header=None)

        data.columns = ['ir1', 'red1', 'ir2', 'red2']

        return data

    def get_record_number(self):
        return self.record['number']

    def load_by_number(self, k):

        path = '../scene/data/' + str(k) + '.txt'
        return self.load(path)


if __name__ == '__main__':
    data = SensorData.load(path='../scene/data/2.txt')
    # print(data)
    sensor = SensorData()
    record = sensor.record
    # print(record[record['number'] > 20])
    print(record)
    # print(sensor.get_record_number())
