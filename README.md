## 基于机器学习的验证码识别

### 目录说明

```
├──  .
├──  catpcha_images     				验证码采集存储目录
├──  thred_images						二值化图片存储目录
├──  noised_images						降噪图片存储目录
├──  eroded_images			 			腐蚀和膨胀图片存储目录
├──  extracted_images					分割图片目录
├──  category_images					预识别分类目录
├──  
├──  get_catpcha.py						验证码采集
├──  thresh_image.py					二值化
├──  mov_noise_image.py					降噪
├──  dilate_erod_image.py  				腐蚀和膨胀
├──  extract_image.py					图片切割
├──  category_image.py					预识别和分类
├──  model_labels.dat					训练模型时生成的所需序列化标签
├──  captcha_model.hdf5   				训练后生成的模型
├──  
├──  train_model.py						训练模型
├──  solve_catpcha.py					使用训练的模型识别验证码
├── 
├──  helpers.py 						训练和识别时所需的函数
└──  main.py							统一调用和测试

```

## 环境

**我的环境：**

* OSX 
* Python3.6 
* opencv 
* virtulenv 
* PIL 
* pytesseract 

**安装opencv** 

`brew install opencv` 

将`opencv`与虚拟环境`virtulenv`中的`python3`进行关联链接 

`sudo ln -s /usr/local/Cellar/opencv/3.4.2/lib/python3.7/site-packages/cv2.cpython-37m-darwin.so cv2.so` 

其他requirements 

```
numpy 
imutils 
sklearn 
tensorflow 
keras 
```

```
pip3 install -r requirements.txt
```

## 测试与运行

可参考代码中的注释进行理解。

验证码前置操作：

包含验证码`二值化`、`降噪`、`腐蚀和膨胀`、`预分类`

在`main`中直接调用，依据不同的验证码的情况调节：

如：有的验证码有背景噪声、干扰线，需要进行降噪、腐蚀膨胀操作。

有的验证码干净、只需要二值化、切割即可。

## 示例

使用`xiaocms`的验证码进行测试：

```
http://demo.xiaocms.cn/index.php?c=api&a=checkcode&width=85&height=26&0.8979280327437793
```

操作：

切换到virtulenv环境：

```
source /venv/bin/acticate
```

opencv与virtulenv环境关联

```
sudo ln -s /usr/local/Cellar/opencv/3.4.2/lib/python3.7/site-packages/cv2.cpython-37m-darwin.so cv2.so
```

then

```
python3 main.py
```

等category_image预识别与分类完成，进行人工纠错，然后训练模型

```
python3 train_model.py
```

注：有时当采集数量不足时，随机字符串不足以覆盖所有字符，或预识别不准，不能准确全部分类32个字符串，因此训练模型这一步可能会报错，也就是88行`model.add(Dense(32, activation="softmax"))`中的32修改为category_images目录下的分类目录数量，(报错会提示这个数字)

训练成功后：

```
python3 solve_catpcha.py
```

会随机选择5个验证码进行识别，并显示出来。