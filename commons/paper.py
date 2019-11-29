import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wavelet import *

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 计算信噪比
def wav_snr(ref_wav, in_wav):# 如果ref wav稍长，则用0填充in_wav

    k = len(ref_wav) - len(in_wav)
    if (k < 0):
        ref_wav = np.pad(ref_wav, (0, abs(k)), 'constant')
    elif (k > 0):
        in_wav = np.pad(in_wav, (0, abs(k)), 'constant')

    # 计算 SNR
    norm_diff = np.square(np.linalg.norm(in_wav - ref_wav))
    if (norm_diff == 0):
        print("错误：参考wav与输入wav相同")
        return -1

    ref_norm = np.square(np.linalg.norm(ref_wav))
    snr = 10 * np.log10(ref_norm / norm_diff)
    return snr

# 添加噪声
def wgn(x, snr):
    snr = 10**(snr/10.0)
    xpower = np.sum(x**2)/len(x)
    npower = xpower / snr
    return np.random.randn(len(x)) * np.sqrt(npower)

#########################################################################
# 输入数据
# table = pd.read_excel("../old/data_regular/01_08_17_59.xlsx")
# ir = table.loc[3000:5900,'ir2']
# x = np.array(ir)
# t = np.arange(0, len(x))
# n = wgn(x, 6)
# xn = x+n # 增加了6dBz信噪比噪声的信号

# length = len(x)

#########################################################################
#验证小波去噪效果的数据示意图
# plt.subplot(221)
# plt.plot(t[:length],x[:length])
# plt.title('a. 原始PPG信号')
# plt.xlabel('采样点')
# plt.ylabel('PPG 值')
#
# plt.subplot(222)
# plt.plot(t[:length],xn[:length])
# plt.title('b. 增加高斯噪声信号后的PPG信号')
# plt.xlabel('采样点')
# plt.ylabel('PPG 值')
#
# plt.subplot(223)
# plt.hist(n, bins=100, normed=True)
# plt.title('c. 高斯噪声分布')
# plt.xlabel('随机值')
# plt.ylabel('概率')
#
# plt.subplot(224)
# plt.psd(n)
# plt.title('d. 功率谱密度')
# plt.xlabel('频率')
# plt.ylabel('能量谱密度 （db/Hz）')

#plt.tight_layout()

#plt.savefig('show the result.png',dpi=600)


#########################################################################################
# 验证小波基
# plt.subplot(411)
# plt.plot(x)
# plt.title('a. 原始信号')
#
# plt.subplot(412)
# after = wavelet_filter_with_base(xn,'db4')
# plt.plot(after)
# val = 'SNR(db4): %.2f' % wav_snr(x, after)
# plt.title('b. db4小波基   ' + val)

# plt.subplot(413)
# after = wavelet_filter_with_base(xn,'sym3')
# plt.plot(after)
# val = 'SNR(sym3): %.2f' % wav_snr(x, after)
# plt.title('c. sym3小波基   ' + val)

# plt.subplot(614)
# after = wavelet_filter_with_base(xn,'haar')
# plt.plot(after)
# val = 'SNR(haar): %.2f' % wav_snr(x, after)
# plt.title('d. haar小波基   ' + val)

# plt.subplot(414)
# after = wavelet_filter_with_base(xn,'bior3.1')
# plt.plot(after)
# val = 'SNR(bior3.1): %.2f' % wav_snr(x, after)
# plt.title('d. bior3.1小波基   ' + val)

# plt.subplot(616)
# after = wavelet_filter_with_base(xn,'coif1')
# plt.plot(after)
# val = 'SNR(coif1): %.2f' % wav_snr(x, after)
# plt.title('f. coif1小波基   ' + val)

# plt.tight_layout()
# plt.savefig('base wavelet',dpi=600)
# plt.show()

#########################################################################################
# 计算小波基函数对应的值

# wavelist = ['bior2.2', 'bior2.4', 'bior2.6', 'bior2.8', 'bior3.3', 'bior3.5', 'db2', 'db3', 'db4', 'db5', 'db6', 'db7','sym2', 'sym3', 'sym4', 'sym5', 'sym6', 'sym7']
# for b in wavelist:
#     base = b
#     after = wavelet_filter_with_base(xn, base)
#     val = '%.2f' % wav_snr(x, after)
#     print(base + ' : ' + val)

#########################################################################################
#  去除基线漂移

# table = pd.read_excel("../old/data_raw/12_26_20_30.xlsx")
#
#
# ir = table['ir_1'].rolling(window=30).mean().rolling(window=30).mean()
# ir = ir[2000:]
# ir = ir.reset_index(drop=True)
# x1 = ir
# t1 = np.arange(0, len(x1))
#
# x2 = remove_baseline(x1)
# t2 = np.arange(0, len(x2))
#
# plt.subplot(211)
# plt.plot(t1,x1,c='r')
# plt.title('a. PPG信号')
# plt.xlabel('采样点')
# plt.ylabel('幅值')
# plt.subplot(212)
# plt.plot(t2,x2)
# plt.title('b. 去除基线漂移后的PPG信号')
# plt.xlabel('采样点')
# plt.ylabel('幅值')
#
#
# plt.tight_layout()
# plt.savefig('remove baseline',dpi=600)
# plt.show()

#########################################################################################
#  异常波形片段

table = pd.read_excel("../old/data_raw/12_25_21_37.xlsx")

ir = table['ir_1'].rolling(window=30).mean().rolling(window=30).mean()

plt.plot(ir)
plt.show()











