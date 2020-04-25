import xgboost as xgb


""""
使用模型计算指标
"""


from calculate.load import load_all, dump_value

if __name__ == '__main__':

    """
    使用模型 预测结果
    
    """

    # keys = ['24', '70']
    keys = ['patient']
    bps = ['high', 'low']
    for key in keys:
        for bp in bps:
            base = '../model/'
            model = xgb.Booster(model_file=base + key + '_' + bp)
            import pickle
            #model = pickle.load(open(base + key + '_' + bp, 'rb'))

            test, x, h, l = load_all(key)
            test.fillna(0, inplace=True)
            y = model.predict(x)
            y = [int(_) for _ in list(y)]
            h = [int(_) for _ in list(h)]
            l = [int(_) for _ in list(l)]
            print(y)

            name = key + '_' + bp
            if bp == 'high':
                dump_value(list(y), list(h), name)
            else:
                dump_value(list(y), list(l), name)
