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
from load import load


""""
训练不同机器学习模型
ga-xgboost

lr / svm / bp 等等各种不同的算法

训练并保存模型
"""


# key = '24'
# bp = 'high'
keys = ['patient']
bps = ['high']
for key in keys:
    for bp in bps:
        train_X, test_X, train_Y, test_Y = load(key, bp=bp, ratio=0.2)
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
        #liner_predictor = linear_model.LinearRegression()

        # 支持向量机 liner 线性  poly 多项式  rbf 径向基
        #svr_predictor = SVR(kernel='poly', C=100, gamma=0.1, epsilon=.1)

        base = '../model/'
        print(key)
        print(bp)
        #train_X = train_X.fillna(0, inplace=True)
        print(list(train_X))
        print(list(train_Y))
        xgboost_predictor.fit(train_X, train_Y)
        xgboost_predictor.save_model(base+key+'_'+bp)

        #print(train_X)
        #print(train_X)
        #liner_predictor.fit(train_X, train_Y)
        #print('liner finish')
        #svr_predictor.fit(train_X, train_Y)
        #print('svr finish')

        print('-------------')

        import pickle
        #pickle.dump(liner_predictor, open(base+'liner_'+key+'_'+bp, 'wb'))
        #pickle.dump(svr_predictor, open(base+'svr_'+key+'_'+bp, 'wb'))


