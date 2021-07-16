# weixin_Image.bat 破解
# JPG 16进制 FF D8 FF
# PNG 16进制 89 50 4e 47
# GIF 16进制 47 49 46 38
# 微信.bat 16进制 a1 86----->jpg  ab 8c----jpg     dd 04 --->png
# 自动计算异或 值
import os

into_path = r'C:/image'  # 微信image文件路径
out_path = r"C:/image/jpg"


def main(into_path, out_path):

    dat_list = Dat_files(into_path)  # 把路径文件夹下的dat文件以列表呈现
    lens = len(dat_list)
    if lens == 0:
        print('没有dat文件')
        exit()

    num = 0
    for dat_file in dat_list:  # 逐步读取文件
        num += 1
        temp_path = into_path + '/' + dat_file  # 拼接路径：微信图片路径+图片名
        dat_file_name = dat_file[:-4]  # 截取字符串 去掉.dat
        imageDecode(temp_path, dat_file_name, out_path)  # 转码函数
        value = int((num / lens) * 100)             # 显示进度
        print('正在处理--->{}%'.format(value))


def Dat_files(file_dir):
    """
    :param file_dir: 寻找文件夹下的dat文件
    :return: 返回文件夹下dat文件的列表
    """
    dat = []
    for files in os.listdir(file_dir):
        if os.path.splitext(files)[1] == '.dat':
            dat.append(files)
    return dat


def imageDecode(temp_path, dat_file_name, out_path):
    dat_read = open(temp_path, "rb")  # 读取.bat 文件
    xo, j = Format(temp_path)  # 判断图片格式 并计算返回异或值 函数

    if j == 1:
        mat = '.png'
    elif j == 2:
        mat = '.gif'
    else:
        mat = '.jpg'

    out = out_path + '/' + dat_file_name + mat  # 图片输出路径
    png_write = open(out, "wb")  # 图片写入
    dat_read.seek(0)  # 重置文件指针位置

    for now in dat_read:  # 循环字节
        for nowByte in now:
            newByte = nowByte ^ xo  # 转码计算
            png_write.write(bytes([newByte]))  # 转码后重新写入

    dat_read.close()
    png_write.close()


def Format(f):
    """
    计算异或值
    各图片头部信息
    png：89 50 4e 47
    gif： 47 49 46 38
    jpeg：ff d8 ff
    """
    dat_r = open(f, "rb")

    try:
        a = [(0x89, 0x50, 0x4e), (0x47, 0x49, 0x46), (0xff, 0xd8, 0xff)]
        for now in dat_r:
            j = 0
            for xor in a:
                j = j + 1  # 记录是第几个格式 1：png 2：gif 3：jpeg
                i = 0
                res = []
                now2 = now[:3]      # 取前三组判断
                for nowByte in now2:
                    res.append(nowByte ^ xor[i])
                    i += 1
                if res[0] == res[1] == res[2]:
                    return res[0], j
    except:
        pass
    finally:
        dat_r.close()


# 运行
# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    main(into_path, out_path)
