import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib

sns.set_style('darkgrid')

df = pd.read_excel("/document/Project/连续血压测量装置/数据记录.xls")
df.columns = ['name', 'data', 'high01', 'low01', 'high02', 'low02', 'ptt', 'vally_ptt', 'up_sensor01', 'up_sensor02',
              'rr_sensor01', 'rr_sensor02']

for name, group in df.groupby('name'):
    print(name)
    # print(group)
    # group = group.loc[group['vally_ptt'] < 0.05]
    # print(group.ptt)
    high = (np.array(group['high01']) + np.array(group['high02'])) / 2
    low = (np.array(group['low01']) + np.array(group['low02'])) / 2

    plt.scatter(group['ptt'], high, label=name)
    # plt.scatter(low, group['ptt'])
    # print(high)
plt.legend()
plt.show()
