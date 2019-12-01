# -*- coding: utf-8 -*-
import numpy as np
import geatpy as ea
import xgboost as xgb
"""

"""


class MyProblem(ea.Problem):  # 继承Problem父类
    def __init__(self):
        name = 'MyProblem'  # 初始化name（函数名称，可以随意设置）
        M = 1  # 初始化M（目标维数）
        maxormins = [-1]  # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
        Dim = 7  # 初始化Dim（决策变量维数）
        varTypes = [1] * Dim  # 初始化varTypes（决策变量的类型，元素为0表示对应的变量是连续的；1表示是离散的）
        lb = [0, 0, 0, 0, 0, 0, 0]  # 决策变量下界
        ub = [10, 10, 10, 10, 10, 10, 10]  # 决策变量上界
        lbin = [0, 0, 0, 0, 0, 0, 0]  # 决策变量下边界
        ubin = [1, 1, 1, 1, 1, 1, 1]  # 决策变量上边界
        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)

    def aimFunc(self, pop):  # 目标函数

        Vars = pop.Phen  # 得到决策变量矩阵
        learning_rate_x = Vars[:, [0]]
        min_child_weight_x = Vars[:, [1]]
        max_depth_x = Vars[:, [2]]
        gamma_x = Vars[:, [3]]
        subsample_x = Vars[:, [4]]
        colsample_bytree_x = Vars[:, [5]]
        reg_lambda_x = Vars[:, [6]]

        predictor = xgb.XGBRegressor(
            learning_rate=0.1,
            min_child_weight=1,
            max_depth=8,
            gamma=0,
            subsample=0.8,
            colsample_bytree=0.8,
            reg_lambda=1,
            )


