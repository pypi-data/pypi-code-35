import numpy as np
import cv2

__normalize = lambda x: max(0, min(5, int(x / 256 * 6)))
def __color(rgb, s=None):
    r, g, b = map(__normalize, rgb)
    code = r * 6 * 6 + b * 6 + g + 16
    if s is not None: return "\033[38;5;{}m{}\033[m".format(code, s)
    return "\033[48;5;{}m  \033[m".format(code)

def bytes_to_img(data):
    nparr = np.frombuffer(data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def img_to_str(img, w, h):
    rate = np.min(np.array([h, w]) / img.shape[:2])
    h, w = np.round(np.array(img.shape[:2]) * rate).astype(int)
    img = cv2.resize(img, (w, h))
    s = ''
    for i in range(img.shape[0]):
        s += ''.join(map(__color, img[i])) + '\n'
    return s

