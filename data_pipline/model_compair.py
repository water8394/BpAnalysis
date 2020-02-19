import pandas as pd
from plot import Plot

if __name__ == '__main__':

    path = '../scene/diff.txt'
    df = pd.read_table(path, header=None, sep=' ')
    df.columns = ['model', 'key', 'bp', 'mad', 'sd', 'rmsd']
    keys = [70, 24]
    bps = ['high', 'low']

    for key in keys:
        for bp in bps:
            tb = df[(df['key'] == key) & (df['bp'] == bp)]
            print('key:'+str(key)+', bp:'+bp)
            Plot.bar_plot(tb)


