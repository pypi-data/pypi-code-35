from ..utils import Get


__all__ = ["runLoginAndPrintZens"]


def runLoginAndPrintZens():
    ''' 实现登录动作并打印中英文版python之禅 '''
    url = "https://localprod.pandateacher.com/python-manuscript/hello-spiderman/"
    method_params = [
        ("id", "teacher"),
        ("id", "assistant"),
        ("cl", "sub"),
    ]
    username = "酱酱"
    password = "酱酱"

    driver = Get.loginNoCaptcha(url, method_params, username, password)
    zens = Get.locateElement(driver, "ids")("p")
    english_zen = Get.beautifulSoup(zens[0].text)
    chinese_zen = Get.beautifulSoup(zens[1].text)
    print(f"英文版Python之禅：\n{english_zen.text}\n")
    print(f"\n中文版Python之禅：\n{chinese_zen.text}\n")
