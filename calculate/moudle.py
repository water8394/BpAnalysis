import pandas as pd

import xgboost as xgb
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC, SVR
from commons.load_indicator import load, write_to_table
from commons.utils import measure_difference
from sklearn import linear_model
from sklearn.svm import LinearSVC
import pickle
from sklearn.externals import joblib

df = load()
df = df.loc[:70, :]
old_df = df.copy()

raw_pulse = "high_pluse"

# print(df)
train_X, test_X, train_Y, test_Y = train_test_split(
    df[['ptt', 'vally_ptt', 'rr1', 'rr2', 'sum1', 'up1', 'down1', 'sum2', 'up2', 'down2']], (df["high_pluse"]+df["low_pluse"])/2)
# XGBoost
xgboost_predictor = xgb.XGBRegressor(
    learning_rate=0.1,
    n_estimators=1000,
    max_depth=8,
    min_child_weight=1,
    # gamma=0,
    subsample=0.8,
    colsample_bytree=0.8,
    nthread=4,
    scale_pos_weight=1,
    seed=27)
# 线性回归
liner_predictor = linear_model.LinearRegression()

# 支持向量机 liner 线性  poly 多项式  rbf 径向基
svr_predictor = SVR(kernel='rbf', C=100, gamma=0.1, epsilon=.1)

predictors = [xgboost_predictor, liner_predictor, svr_predictor]

for predictor in predictors:

    predictor.fit(train_X, train_Y)
    y = predictor.predict(test_X)
    print('predict Y: ', list(y))
    print('real Y: ', list(test_Y))
    loss = mean_absolute_error(y, test_Y)
    print(loss)
    print('--------------------------------------')

    # measure_difference(test_Y, y, loss)
    # yy = list(y)
    # idx = list(test_X.index)
    # for i,index in enumerate(idx):
    #     t = old_df.loc[index, 't']
    #     write_to_table(t, yy[i])
