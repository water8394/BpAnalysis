from calculate.mathIndicator import get_mae, get_sd, get_rmse


def load_index(path):
    idx = []
    with open(path, 'r+') as f:
        lines = f.readlines()
        for line in lines:
            idx.append(int(line))
    return idx


def load_value(path):
    high, low = [], []
    with open(path, 'r+') as f:
        lines = f.readlines()
        for line in lines:
            v1, v2 = line.split(',')
            high.append(int(v1))
            low.append(int(v2))
    return high, low


if __name__ == '__main__':

    idx = load_index('../scene/group/70.txt')

    v1, v2 = load_value('../scene/result/ga_xgboost_70_low.txt')

    for k in range(1, 4):
        print('-----------  ' + str(k) + '  ---------------')
        l1, l2 = [], []
        for i in range(len(v1)):
            if idx[i] == k:
                l1.append(v1[i])
                l2.append(v2[i])
        print(get_mae(l1, l2))
        print(get_sd(l1, l2))
        print(get_rmse(l1, l2))
