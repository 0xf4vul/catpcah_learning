# _*_ encoding:utf-8 _*_
# __author__ = "dr0op"

"""对图片进行切割，分割为单个字符在一个图片中的形式，以便后面的分类和训练"""

import cv2
import os
from PIL import Image
import time
import imutils

EXTRACTED_FOLDER = "extracted_images"

# 分割图片,使用opencv的findContours功能自动智能地对图片进行`块`切割
def extractImg(image_file):
    """
    分割图片,使用opencv的findContours功能自动智能地对图片进行`块`切割
    :param image_file :  一个经过 二值化、降噪、腐蚀与膨胀处理后的图片
    :return:
    """
    # 加载图片并进行灰度化
    img =cv2.imread(image_file)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 给验证码添加边框，后期根据需求进行修改
    gray = cv2.copyMakeBorder(gray, 0, 0, 0, 0, cv2.BORDER_REPLICATE)

    # 继续对图片进行二值化，因为后面的函数需要一个二值化后的图片格式
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # 使用opencv进行块切割,切割后的数据存储在contours中
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 匹配不同的opencv版本
    contours = contours[0] if imutils.is_cv2() else contours[1]

    letter_image_regions = []

    # 从contours中取出切割后的数据
    for contour in contours[:4]:
        # Get the rectangle that contains the contour
        (x, y, w, h) = cv2.boundingRect(contour)
        # Compare the width and height of the contour to detect letters that
        # are conjoined into one chunk
        if w / h > 1.25:
            # This contour is too wide to be a single letter!
            # Split it in half into two letter regions!
            half_width = int(w / 2)
            letter_image_regions.append((x, y, half_width, h))
            letter_image_regions.append((x + half_width, y, half_width, h))
        else:
            # This is a normal letter by itself
            letter_image_regions.append((x, y, w, h))

    # Sort the detected letter images based on the x coordinate to make sure
    # we are processing them from left-to-right so we match the right image
    # with the right letter
    # 对切割后的图片进行排序，从左到右以便处理
    letter_image_regions = sorted(letter_image_regions, key=lambda x: x[0])


    # 将切割的部分保存为单独的图片
    for letter_bounding_box in letter_image_regions:
        # Grab the coordinates of the letter in the image
        x, y, w, h = letter_bounding_box

        # Extract the letter from the original image with a 2-pixel margin around the edge
        letter_image = gray[y - 2:y + h + 2, x - 2:x + w + 2]
        # write the letter image to a file
        p = os.path.join(os.getcwd(),EXTRACTED_FOLDER, "{}.jpg".format(str(int(time.time()*1000000000))))
        if len(letter_image) != 0:
            cv2.imwrite(p, letter_image)



# 切割图片， 垂直切割（等距切割）使用PIL库的方式
def sliceImg(image_file, outDir, count = 4):
    """
    采用垂直切割的方式进行切割，适用于验证码字符的相对位置不改变的情况，效率较高
    :param image_file: 需要切割的 二值化、降噪、去除干扰线 等操作后的图片
    :param outDir: 切割后的图片存储路径
    :param count: 验证码的字符个数，如 验证码有4个字符，则这个值为4
    :return:
    """
    img = Image.open(image_file)
    w, h = img.size
    eachWidth = int(w / count)
    for i in range(count):
        box = (i * eachWidth, 0, (i + 1) * eachWidth, h)
        img.crop(box).save(os.path.join(outDir, "{}.jpg").format(str(int(time.time()*1000000000))))




# 智能切割，适用于验证码倾斜的情况
def smartSliceImg(image, outDir, count=4, p_w=1):
    '''
    当验证码倾斜或者字符间距比较小的时候，等距切割法切割后的图片会`割`到相邻的字符，这个时候在目标位置的前后进行垂直上
    的像素判断，判断某一列的黑色像素最少，就是切割点

    :param img: 需要切割的图片
    :param outDir: 切割后的存储地址
    :param count: 图片中有多少个图片
    :param p_w: 对切割地方多少像素内进行判断
    :return:
    '''
    img = Image.open(image)
    w, h = img.size
    pixdata = img.load()
    eachWidth = int(w / count)
    beforeX = 0
    for i in range(count):

        allBCount = []
        nextXOri = (i + 1) * eachWidth

        for x in range(nextXOri - p_w, nextXOri + p_w):
            if x >= w:
                x = w - 1
            if x < 0:
                x = 0
            b_count = 0
            for y in range(h):
                if pixdata[x, y] == 0:
                    b_count += 1
            allBCount.append({'x_pos': x, 'count': b_count})
        sort = sorted(allBCount, key=lambda e: e.get('count'))

        nextX = sort[0]['x_pos']
        box = (beforeX, 0, nextX, h)
        img.crop(box).save(os.path.join(outDir,"{}.jpg").format(str(i)))
        beforeX = nextX

