import xgboost as xgb

from calculate.load import load_all, dump_value

if __name__ == '__main__':
    key = '70'
    bp = 'low'
    m = 'norm_svr_'
    base = '../model/' + m
    #model = xgb.Booster(model_file=base + key + '_' + bp)
    import pickle
    model = pickle.load(open(base + key + '_' + bp,'rb'))

    test, x, h, l = load_all(key)
    #test.fillna(0, inplace=True)
    y = model.predict(test)
    y = [int(_) for _ in list(y)]
    h = [int(_) for _ in list(h)]
    l = [int(_) for _ in list(l)]
    print(y)

    name = m + key + '_' + bp
    dump_value(list(y), list(l), name)
