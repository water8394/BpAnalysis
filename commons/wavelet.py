import pywt


"""
小波变化 去除基线
"""
def wavelet_filter(wave):
    sym = pywt.Wavelet('sym6')  # 小波基
    coeffs = pywt.wavedec(wave, sym)
    coeffs[-1] *= 0  # 去除基线漂移
    coeffs[0] *= 0  # 去除基线漂移
    meta = pywt.waverec(coeffs, sym)
    return meta

"""
小波变化 去除基线, 自定义小波基
"""
def wavelet_filter_with_base(wave,base):
    sym = pywt.Wavelet(base)  # 小波基
    coeffs = pywt.wavedec(wave, sym)
    coeffs[-1] *= 0
    coeffs[-2] *= 0
    coeffs[-3] *= 0
    coeffs[-4] *= 0
    coeffs[-5] *= 0
    coeffs[-6] *= 0
    meta = pywt.waverec(coeffs, sym)
    return meta

"""
去除基线漂移
"""
def remove_baseline(wave):
    sym = pywt.Wavelet('db4')  # 小波基
    coeffs = pywt.wavedec(wave, sym)
    coeffs[0] *= 0
    meta = pywt.waverec(coeffs, sym)
    return meta

# print(pywt.wavelist())