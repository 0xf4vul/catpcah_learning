# _*_ encoding:utf-8 _*_
# __author__ = "dr0op"
"""
对切割后的图片进行预识别和分类
"""


from PIL import Image
import pytesseract
import os
import glob
import cv2
import time


EXTRACTED_FOLDER = "extracted_images"
CATEGORY_FOLDER = "category_images"



def ocr_for_Category(extracted_file):
    """
    对分割后的图片进行预识别和分类，预识别的准确率大致在%50～%60之间，预分类之后需要进行人工纠错
    :return:
    """
    # 验证码中一般不会出现`1`和`I`，因为易混淆
    catpcha_words = "ABCDEFGHJKLMNOPQRSTUVWXYZ234567890"
    """
    需要处理pytesseract不能识别或识别为空的情况，使用try...except包裹
    """
    try:
        img = Image.open(extracted_file)
        # pytesseract对分割后的图片进行识别，转化为字符
        code = pytesseract.image_to_string(img, config="-psm 10")
        print("code:", code)
        if code in catpcha_words:
            path = os.path.join(os.getcwd(), CATEGORY_FOLDER, code)
            if not os.path.exists(path):
                os.mkdir(path)
            file = os.path.join(path, "{}.jpg".format(str(int(time.time() * 1000000000))))
            img.save(file)
    except:
        pass

