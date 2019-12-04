import matplotlib.pyplot as plt
import pandas as pd

file = 'data/2.txt'

df = pd.read_table(file, header=None, sep=',')
df.columns = ['ir1', 'red1', 'ir2', 'red2']
plt.plot(df.ir1)
plt.show()
