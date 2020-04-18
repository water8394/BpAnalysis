from extract import extract_all_peaks
from feature_point import extract_feature_point
from metric import extract_metric
from model import cal_bp
from regular import pre_process

"""
数据预处理 && 提取特征值 主类
"""


def main(k):
    print('样本编号: ' + str(k))
    """
     预处理数据
    """
    pre_process(k)
    ####################
    """
     寻找所有的峰值特征点并保存成文件
    """
    extract_all_peaks(k)
    ####################
    """
     计算每一组波形的4个定位特征点
    """
    extract_feature_point(k)
    ######################
    """
     通过峰值点计算所有的特征值
    """
    extract_metric(k)
    ######################
    """
     使用模型预测结果
    """
    cal_bp(k, 'high')


if __name__ == '__main__':
    number = 76
    main(number)
