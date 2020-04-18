# -*- coding: utf-8 -*-
import geatpy as ea
import xgboost as xgb

from calculate import *
from calculate.load import load
from calculate.mathIndicator import get_mae,get_sd,get_rmse


class MyProblem(ea.Problem):  # 继承Problem父类
    def __init__(self):
        name = 'MyProblem'  # 初始化name（函数名称，可以随意设置）
        M = 1  # 初始化M（目标维数）
        maxormins = [1]  # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
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
        learning_rate_list = Vars[:, [0]]
        min_child_weight_list = Vars[:, [1]]
        max_depth_list = Vars[:, [2]]
        gamma_list = Vars[:, [3]]
        subsample_list = Vars[:, [4]]
        colsample_bytree_list = Vars[:, [5]]
        reg_lambda_list = Vars[:, [6]]

        l = len(learning_rate_list)
        res = []
        for i in range(l):
            learning_rate_x = learning_rate_list[i][0] / 10
            min_child_weight_x = min_child_weight_list[i][0] / 10
            max_depth_x = int(max_depth_list[i][0] * 2)
            gamma_x = gamma_list[i][0] / 10
            subsample_x = subsample_list[i][0] / 10
            colsample_bytree_x = colsample_bytree_list[i][0] / 10
            reg_lambda_x = reg_lambda_list[i][0] / 10
            # 构建模型
            predictor = xgb.XGBRegressor(
                learning_rate=learning_rate_x,
                min_child_weight=min_child_weight_x,
                max_depth=max_depth_x,
                gamma=gamma_x,
                subsample=subsample_x,
                colsample_bytree=colsample_bytree_x,
                reg_lambda=reg_lambda_x,
            )

            # 训练模型
            predictor.fit(train_X, train_Y)
            predictor.save_model('../model/patient_high')
            # 预测结果
            y = predictor.predict(test_X)
            # 计算损失值
            loss = get_rmse(y, test_Y)

            res.append([loss])

        pop.ObjV = np.array(res)  # 赋值给pop种群对象的ObjV属性


if __name__ == '__main__':
    """================================实例化问题对象==========================="""
    problem = MyProblem()  # 生成问题对象
    # 加载数据
    key = 'patient'
    bp = 'low'
    train_X, test_X, train_Y, test_Y = load(key, bp, ratio=0.7)

    """==================================种群设置==============================="""
    Encoding = 'RI'  # 编码方式
    NIND = 100  # 种群规模
    Field = ea.crtfld(Encoding, problem.varTypes, problem.ranges, problem.borders)  # 创建区域描述器
    population = ea.Population(Encoding, Field, NIND)  # 实例化种群对象（此时种群还没被初始化，仅仅是完成种群对象的实例化）
    """================================算法参数设置============================="""
    myAlgorithm = ea.soea_DE_rand_1_L_templet(problem, population)  # 实例化一个算法模板对象
    myAlgorithm.MAXGEN = 50  # 最大进化代数
    myAlgorithm.mutOper.F = 0.5  # 差分进化中的参数F
    myAlgorithm.recOper.XOVR = 0.7  # 重组概率
    """===========================调用算法模板进行种群进化======================="""
    [population, obj_trace, var_trace] = myAlgorithm.run()  # 执行算法模板
    population.save()  # 把最后一代种群的信息保存到文件中
    # 输出结果
    best_gen = np.argmin(problem.maxormins * obj_trace[:, 1])  # 记录最优种群个体是在哪一代
    best_ObjV = obj_trace[best_gen, 1]
    print('最优的目标函数值为：%s' % (best_ObjV))
    print('最优的决策变量值为：')
    for i in range(var_trace.shape[1]):
        print(var_trace[best_gen, i])
    print('有效进化代数：%s' % (obj_trace.shape[0]))
    print('最优的一代是第 %s 代' % (best_gen + 1))
    print('评价次数：%s' % (myAlgorithm.evalsNum))
    print('时间已过 %s 秒' % (myAlgorithm.passTime))
