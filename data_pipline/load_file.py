from data_pipline import *


class SensorData:

    def __init__(self):
        self.data = pd.DataFrame

        self.record = pd.DataFrame
        self._load_record()

    def _load(self, path, form='txt'):
        self.data = self.load(path, form)

    @staticmethod
    def load(path, form='txt'):

        data = pd.DataFrame

        if form == 'txt':
            data = pd.read_table(path, header=None, sep=',')
        elif form == 'excel':
            data = pd.read_excel(path, header=None)

        data.columns = ['ir1', 'red1', 'ir2', 'red2']

        return data

    def _load_record(self):
        self.record = pd.read_excel('../scene/记录表.xlsx')
