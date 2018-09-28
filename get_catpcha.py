# _*_ encoding:utf-8 _*_
# __author__ = "dr0op"

"""
验证码采集
"""


import os
import requests
import time


CAPTCHA_IMAGE_FOLDER = "catpcha_images"


def get_image(image_src,):
    """
    :param image_src 验证码URL:
    :return:
    """
    img= requests.get(image_src,stream=True)
    path = os.path.join(os.getcwd(),CAPTCHA_IMAGE_FOLDER)
    img_name = os.path.join(path, str(int(time.time()*1000000000))+".jpg")
    print(img_name)
    with open(img_name,"wb") as f:
        f.write(img.content)
        f.close()


if __name__ == '__main__':
    for i in range(80):
        get_image("http://demo.xiaocms.cn/index.php?c=api&a=checkcode&width=85&height=26&0.8979280327437793")