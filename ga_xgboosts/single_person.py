import pandas as pd
import numpy as np

def mae(a, b):
    ret = 0
    cnt = 0
    for x,y in zip(a,b):
        ret += abs(x-y)
        cnt += 1
    return ret/cnt

df = pd.read_excel('../scene/高压记录.xlsx')

a = df[(df['name'] == 'C') & (df['is_eat'] == 0)]

rh = np.asarray(a['high'])
rl = np.asarray(a['low'])
ph = np.asarray(a['h'])
pl = np.asarray(a['l'])
print(np.mean(rh))
print(np.mean(rl))
print(np.mean(ph))
print(np.mean(pl))

print(mae(rh, ph))
print(mae(rl, pl))
