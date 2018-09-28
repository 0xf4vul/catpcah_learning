# _*_ encoding:utf-8 _*_
# __author__ = "dr0op"
"""
对二值化后的图片进行降噪
"""
import cv2
from PIL import Image

#推荐使用
def clearNoise(image_file):
    """
    传入一个二值化的图片并利用PIL库进行降噪，除去验证码背景的黑点
    :param image_file 二值化图片路径:
    :return:
    """
    im = Image.open(image_file)
    data = im.getdata()
    w, h = im.size
    black_point = 0

    for x in range(1, w - 1):
        for y in range(1, h - 1):
            mid_pixel = data[w * y + x]  # 中央像素点像素值
            if mid_pixel < 50:  # 找出上下左右四个方向像素点像素值
                top_pixel = data[w * (y - 1) + x]
                left_pixel = data[w * y + (x - 1)]
                down_pixel = data[w * (y + 1) + x]
                right_pixel = data[w * y + (x + 1)]

                # 判断上下左右的黑色像素点总个数
                if top_pixel < 10:
                    black_point += 1
                if left_pixel < 10:
                    black_point += 1
                if down_pixel < 10:
                    black_point += 1
                if right_pixel < 10:
                    black_point += 1
                if black_point < 1:
                    im.putpixel((x, y), 255)
                #print(black_point)
                black_point = 0
    for x in range(1, w - 1):
        for y in range(1, h - 1):
            if x < 2 or y < 2:
                im.putpixel((x - 1, y - 1), 255)
            if x > w - 3 or y > h - 3:
                im.putpixel((x + 1, y + 1), 255)

    return im



# 暂不推荐使用，保留选择
def clearNoiseCV(image_file):
    """
    依托opencv中的'中值滤波'方式对图片进行降噪，经测试对图片的影响较大，暂不推荐使用，或后期修改后可使用，保留选择
    :param image_file:
    :return:
    """
    img = cv2.imread(image_file)
    #中值滤波，第二个参数回影响中值滤波的效果，暂时测试只能取奇数
    img_medianblur = cv2.medianBlur(img, 3)
    return img_medianblur
    """注： 在opencv中将 背景黑点称为'椒盐噪声' ，由于验证码的黑点像素大小不一，而椒盐噪声的像素点大小一般
    比较统一，验证码的'噪声'严格意义上不能称为'椒盐噪声' 而理解为 '去除干扰' """
