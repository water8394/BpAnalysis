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

    @staticmethod
    def _combine_path(k):
        return '../scene/data/' + str(k) + '.txt'

    def get_record_number(self):
        return self.record['number']

    def load_by_number(self, k):

        path = SensorData._combine_path(k)
        return self.load(path)

    def resave_file(self, k, data):
        path = SensorData._combine_path(k)
        with open(path, 'w+') as f:
            f.seek(0)
            for i in range(data.shape[0]):
                line = data.loc[i]
                line = ','.join(str(_) for _ in line) + '\n'
                f.writelines(line)
            f.truncate()


if __name__ == '__main__':
    data = SensorData.load(path='../scene/data/2.txt')
    # print(data)
    sensor = SensorData()
    record = sensor.record
    # print(record[record['number'] > 20])
    #print(record)
    # print(sensor.get_record_number())

    #sensor.resave_file(100, data)