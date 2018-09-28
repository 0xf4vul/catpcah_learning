# _*_ encoding:utf-8 _*_
# __author__ = "dr0op"
"""
对图片进行二值化  两个DEMO 分别为opencv库和PIL库方式
"""


import cv2
from PIL import Image

def thresh_image_cv(image_file):
    """
    对图片二值化（非黑即白）的openv方式
    :param image_file:
    :return:
    """
    # 加载图片并进行灰度化
    image = cv2.imread(image_file)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 扩展边框,  ---可选
    # gray = cv2.copyMakeBorder(gray, 8, 8, 8, 8, cv2.BORDER_REPLICATE)

    # 图片二值化，将其转化为非黑即白
    thresh = cv2.threshold(gray.copy(), 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return thresh



def thresh_image_pil(image_file):
    """
    对图片进行二值化（非黑即白）的PIL方式
    :param img:
    :param out:
    :return:
    """
    image = Image.open(image_file)
    # 灰度图
    lim = image.convert('L')
    # 灰度阈值设为165，低于这个值的点全部填白色
    threshold = 165
    table = []
    for j in range(256):
        if j < threshold:
            table.append(0)
        else:
            table.append(1)
    bim = lim.point(table, '1')
    return bim