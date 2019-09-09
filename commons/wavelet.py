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