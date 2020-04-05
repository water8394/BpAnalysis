import xgboost as xgb

from calculate.load import dump_value
from load_file import SensorData


def cal_bp(k, bp='high'):
    base = '../model/' + 'norm_xgb_'
    model = xgb.Booster(model_file=base + '24_' + bp)

    test, x, h, l = SensorData.load_metric(k)
    y = model.predict(x)
    y = [int(_) for _ in list(y)]
    h = [int(_) for _ in list(h)]
    l = [int(_) for _ in list(l)]
    print(y)

    name = 'bp-value-' + bp + '-' + str(k)
    dump_value(list(y), list(l), name)
