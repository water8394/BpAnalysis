import pandas as pd

def get_record():
    df = pd.read_excel('记录表.xlsx')
    df.columns = ['file_id','name','scene','high','low']
    return df


if __name__ == '__main__':
    get_record()