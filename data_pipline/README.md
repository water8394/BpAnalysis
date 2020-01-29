## data_pipline 包含了数据采集后的全部处理流程

#### step 1: trim
修剪数据，把波动较大的部分去除掉

#### step 2： regular
预处理数据，包含去除DC分量/滤波/放缩

#### step 3： extract
将各个类型的峰值点提取出来

#### step 4：feature_point
提取峰值点数据，包含波峰峰值点，重播波峰值点，波谷点

#### step 5: metric
根据提取到的特征点计算指标

## 📁 文件存储说明
data: 原始数据，不允许做修改

regular: 处理过后的数据

peak_index: 主波峰值点索引文件，包含两路ir数据

mid_peak_index: 只包含单路ir1的重播波峰值点

vally_peak_index: 只包含单路ir1的波谷点

feature_point: 如果一个周期内的波形包含4个特征点，则记录该4个特征点的索引并保存

metric: 通过特征点计算得到的指标文件，共有9个特征值