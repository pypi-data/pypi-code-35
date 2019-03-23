from crawlerUtils import Post


# 验证码的字符集合
CAPTCHA_SET = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a',
    'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
]


# 根据验证码的字符集合创建验证码训练文件夹
Post.createTestSet(captcha_set=CAPTCHA_SET)

# 请求并获取验证码函数
def getCaptcha():
    """ 获取验证码的函数必须至少返回filepath->验证码路径, 和extension->验证码图片扩展名如jpeg两个参数 """
    captcha_params = {
        "captcha_str": "15718894914",
    }

    captcha_url = "https://h5.ele.me/restapi/eus/v3/captchas"

    captcha_json = Post(captcha_url, jsons=captcha_params).json
    captcha_hash = captcha_json["captcha_hash"]
    b64data = captcha_json['captcha_image']

    filepath, extension = Post.base64decode(b64data)

    return filepath, extension

# 进行验证码训练, 比如训练2次
Post.captchaTrain(getCaptcha, times=2)

# 请求一次验证码
captcha_code = Post.recognizeCaptcha(getCaptcha)
print(f"\n验证码识别结果：{captcha_code}, ", end="")