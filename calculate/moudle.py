import pandas as pd
from utils import *

import xgboost as xgb
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

df = pd.read_excel('data/temporary_data.xlsx')

train_X, test_X, train_Y, test_Y = train_test_split(
    df[['ptt', 'vally_ptt', 'up_sensor01', 'up_sensor02', 'rr_sensor01', 'rr_sensor02']], df['high'])

predictor = xgb.XGBRegressor()

predictor.fit(train_X, train_Y)
y = predictor.predict(test_X)
print('predict Y: ', list(y))
print('real Y: ', list(test_Y))
loss = mean_absolute_error(y, test_Y)
print(loss)
measure_difference(test_Y, y, loss)
