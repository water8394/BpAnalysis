import pywt


def wavelet_filter(wave):
    """
    小波变化 去除基线
    """
    print('data length: ' + str(len(wave)))
    if len(wave) %2 > 0:
        wave = wave[:-1]
    sym = pywt.Wavelet('sym6')  # 小波基
    coeffs = pywt.wavedec(wave, sym)
    coeffs[-1] *= 0  # 去除基线漂移
    coeffs[0] *= 0  # 去除基线漂移
    meta = pywt.waverec(coeffs, sym)
    return meta


def wavelet_filter_with_base(wave, base):
    """
    小波变化 去除基线, 自定义小波基
    """

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


def remove_baseline(wave):
    """
    去除基线漂移
    """
    sym = pywt.Wavelet('db4')  # 小波基
    coeffs = pywt.wavedec(wave, sym)
    coeffs[0] *= 0
    meta = pywt.waverec(coeffs, sym)
    return meta

# print(pywt.wavelist())
