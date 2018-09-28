# _*_ encoding:utf-8 _*_
# __author__ = "dr0op"

"""采用xiaocms的验证码采集并识别"""

import glob
import os
import time
import cv2

from imutils import paths

from get_catpcha import get_image
from thresh_image import thresh_image_cv
from extract_image import extractImg
from category_image import ocr_for_Category


CAPTCHA_IMAGE_FOLDER = "catpcha_images"
THRED_IMAGE_FOLDER = "thred_images"
NOISED_IMAGE_FOLDER ="noised_image"
ERODED_IMAGE_FOLDER = "eroded_images"
OUTPUT_FOLDER = "output_images"
EXTRACTED_FOLDER = "extracted_images"
CATEGORY_FORDER = "category_images"


# 采集图片
if len(os.listdir(CAPTCHA_IMAGE_FOLDER)) < 10:
    for i in range(200):
        get_image("http://demo.xiaocms.cn/index.php?c=api&a=checkcode&width=85&height=26&0.8979280327437793")


# 对图片进行二值化，保存在  thred_images   目录下
captcha_image_files = glob.glob(os.path.join(os.getcwd(), CAPTCHA_IMAGE_FOLDER, "*"))
if len(os.listdir(THRED_IMAGE_FOLDER)) < 10:
    for image_file in captcha_image_files:
        path = os.path.join(os.getcwd(), THRED_IMAGE_FOLDER, str(int(time.time() * 1000000000)) + ".jpg")
        cv2.imwrite(path,thresh_image_cv(image_file))



# 由于此验证码无明显干扰，不需要进行降噪和去除干扰线，直接进行切割
thred_image_files = glob.glob(os.path.join(os.getcwd(), THRED_IMAGE_FOLDER, "*"))
if len(os.listdir(EXTRACTED_FOLDER)) < 10:
    for thred_image in thred_image_files:
        path = os.path.join(os.getcwd(), EXTRACTED_FOLDER, str(int(time.time() * 1000000000)) + ".jpg")
        extractImg(thred_image)


# 对分割后的图片进行预分类
extracted_image_files = glob.glob(os.path.join(os.getcwd(), EXTRACTED_FOLDER, "*"))
if len(os.listdir(CATEGORY_FORDER)) < 10:
    for extracted_file in extracted_image_files:
        #path = os.path.join(os.getcwd(), CATEGORY_FORDER, str(int(time.time() * 1000000000)) + ".jpg")
        ocr_for_Category(extracted_file)


