import matplotlib.pyplot as plt
import pandas as pd

raw = "../data_raw/1_6_16_26.xlsx"
filter = "../data_after/1_6_16_26.xlsx"
regular = "../data_regular/1_6_16_26.xlsx"

raw_data = pd.read_excel(raw)["ir_1"]
filter_data = pd.read_excel(filter,header=None)[0]
regular_data = pd.read_excel(regular)

plt.plot(regular_data["ir1"])
plt.plot(regular_data["ir2"])

# fig = plt.figure()
# plt.title("原始波形/巴特沃茨滤波器/归一化波形")
# plt.subplot(3,1,1)
# plt.plot(raw_data)
# plt.subplot(3,1,2)
# plt.plot(filter_data)
# plt.subplot(3,1,3)
# plt.plot(regular_data)
plt.show()