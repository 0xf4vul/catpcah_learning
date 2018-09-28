# _*_ encoding:utf-8 _*_
# __author__ = "dr0op"
"""对图片进行腐蚀和膨胀，对去除验证码中的干扰线有较好的效果"""

import cv2


# 腐蚀和膨胀，去除图片横线
def dilate_erod_image(image_file):
    """
    对图片进行腐蚀和膨胀，有效去除干扰线
    :param image_file:
    :return:
    """
    img = cv2.imread(image_file, -1)
    # 腐蚀和膨胀的参数设置，测试当参数为2，3时最佳
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,3))
    # 对图片进行腐蚀和膨胀
    dilated = cv2.dilate(img, kernel)
    eroded = cv2.erode(dilated, kernel)

    return eroded

'''
if __name__ == '__main__':
    file = os.path.join(os.getcwd(),"noised_images/1538028289907087872.jpg")
    dilate_erod_image(file)
'''