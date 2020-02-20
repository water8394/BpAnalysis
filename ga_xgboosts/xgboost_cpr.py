import matplotlib.pyplot as plt


def load_file(path):
    data = []
    min = 1000
    with open(path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            s = line[:5]
            d = float(s)
            if (d < min):
                min = d
            data.append(min)
    return data

def save_file(path, data):
    with open(path, 'w') as f:
        for line in data:
            f.writelines(str(line) + '\r\n')

def load(key, bp):
    base = 'scene/'
    save_base = 'res/'
    path = base + key + '_' + bp + '_'
    mae_path = path + 'mae.csv'
    sd_path = path + 'sd.csv'
    rmse_path = path + 'rmse.csv'
    mae = load_file(mae_path)
    sd = load_file(sd_path)
    rmse = load_file(rmse_path)
    save_file(save_base+key + '_' + bp + '_'+ 'mae.csv', mae)
    save_file(save_base+key + '_' + bp + '_'+ 'sd.csv', sd)
    save_file(save_base+key + '_' + bp + '_'+ 'rmse.csv', rmse)

    return mae, sd, rmse


def plot(mae, sd, rmse):
    plt.plot(mae, label='MAE', color='dodgerblue')
    plt.plot(sd, label='SD', color='darkorange')
    plt.plot(rmse, label='RMSE', color='limegreen')

    plt.legend()
    plt.show()


if __name__ == '__main__':
    keys = ['70', '24']
    bps = ['high', 'low']
    for key in keys:
        for bp in bps:
                print("key:"+key+",bp:"+bp)
                mae, sd, rmse = load(key, bp)
                plot(mae, sd, rmse)
