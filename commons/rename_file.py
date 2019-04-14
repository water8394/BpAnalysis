
import os


"""
批量重命名文件 将开头的姓名代号去掉
para： 数据文件夹路径
"""
def rename(path):
    files = os.listdir(path)
    new_files = []
    for file in files:
        before = file
        file = file.split("_")[1:]
        file = "_".join(file)
        os.rename(path+before, path+file)



if __name__ == '__main__':
    rename("data_after_bak/")