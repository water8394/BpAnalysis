import xgboost as xgb
from calculate.load import load_all,dump_value

if __name__ == '__main__':

    key = '70'
    bp = 'high'
    model = xgb.Booster(model_file='../model/ga_xgboost_'+key+'_'+bp)

    x, h, l = load_all(key)
    y = model.predict(x)
    y = [int(_) for _ in list(y)]
    h = [int(_) for _ in list(h)]

    dump_value(list(y),list(h),'ga_xgboost_'+key+'_'+bp)