# coding=utf-8

"""
Created on 2015年11月6日

@author: thomas.ning
"""

import json,tempfile,zipfile,re,time
import os,base64,sys
try:
    from PIL import Image, ImageChops
except:
    pass 
from easyuiautomator.common.exceptions import NoSuchElementException
from easyuiautomator.common.log import Logger
from easyuiautomator.common.find_img import find_img_position
from easyuiautomator.common.blackCheck import blackBorderCheck  
 
LOGGER = Logger.getLogger()


def format_json(json_struct):
    return json.dumps(json_struct, indent=4)


def dump_json(json_struct, ensure_ascii=True):
    return json.dumps(json_struct, ensure_ascii=ensure_ascii)


def load_json(s):
    return json.loads(s)


def handle_find_element_exception(e):
    if ("No element found" in e["value"] or
                "Unable to locate" in e["value"]):
        raise NoSuchElementException("Unable to locate element:")
    else:
        raise e


def return_value_if_exists(resp):
    if resp and "value" in resp:
        return resp["value"]


def get_root_parent(elem):
    parent = elem.parent
    while True:
        try:
            parent.parent
            parent = parent.parent
        except AttributeError:
            return parent


def unzip_to_temp_dir(zip_file_name):
    """Unzip zipfile to a temporary directory.

    The directory of the unzipped files is returned if success,
    otherwise None is returned. """
    if not zip_file_name or not os.path.exists(zip_file_name):
        return None

    zf = zipfile.ZipFile(zip_file_name)

    if zf.testzip() is not None:
        return None

    # Unzip the files into a temporary directory
    LOGGER.info("Extracting zipped file: %s" % zip_file_name)
    tempdir = tempfile.mkdtemp()

    try:
        # Create directories that don't exist
        for zip_name in zf.namelist():
            # We have no knowledge on the os where the zipped file was
            # created, so we restrict to zip files with paths without
            # charactor "\" and "/".
            name = (zip_name.replace("\\", os.path.sep).
                    replace("/", os.path.sep))
            dest = os.path.join(tempdir, name)
            if (name.endswith(os.path.sep) and not os.path.exists(dest)):
                os.mkdir(dest)
                LOGGER.debug("Directory %s created." % dest)

        # Copy files
        for zip_name in zf.namelist():
            # We have no knowledge on the os where the zipped file was
            # created, so we restrict to zip files with paths without
            # charactor "\" and "/".
            name = (zip_name.replace("\\", os.path.sep).
                    replace("/", os.path.sep))
            dest = os.path.join(tempdir, name)
            if not (name.endswith(os.path.sep)):
                LOGGER.debug("Copying file %s......" % dest)
                outfile = open(dest, 'wb')
                outfile.write(zf.read(zip_name))
                outfile.close()
                LOGGER.debug("File %s copied." % dest)

        LOGGER.info("Unzipped file can be found at %s" % tempdir)
        return tempdir

    except IOError as err:
        LOGGER.error("Error in extracting webdriver.xpi: %s" % err)
        return None


def formatReturnStr(status, value):
    return {'status': status, 'value': value}

def formatExceptionStr(device, msg):
    return dump_json({'device': device, 'message': msg}, False)

def is_base64(strword):
    try:
        if len(strword) < 200:
            if os.path.exists(strword):
                return False
        else:
            base64.b64decode(strword)
            return True
    except:
        pass
    return False

def waitForCondition(method, returnValue, timeout=5, intervalMs=0.5, args=None):
    '''等待条件超时函数，根据函数返回值条件，确认是否跳出
    ：    :Args:
        methon: 函数名
        args: 必须是元组参数传递形式，如（'tt',dd)
        returnValue:对比值
    '''
    end_time = time.time() + timeout
    while True:
        try:
            if args is None:
                tmp = method()
            else:
                tmp = method(*args)
            if tmp == returnValue:
                return True
        except:
            print sys.exc_info()
        if time.time() - end_time>0:
            return None
        time.sleep(intervalMs)    

class ImageUtil:
    '''
    image deal class
    '''
    @staticmethod
    def find_image_positon(query, origin, algorithm='sift', radio=0.75):
        temp = origin
        if is_base64(origin):
            temp=tempfile.mktemp()
            with open(temp,"wb") as f:
                f.write(origin)
        if not os.path.exists(query):
            raise IOError,('No such file or directory:%s'%query)
        position = find_img_position(query, temp, algorithm, radio)
        if os.path.exists(temp):os.remove(temp)
        return position

    @staticmethod
    def compare_stream(strStream, target_file):
        '''
        file stream compare
        :Args:
         - strStream: strStrem by driver.get_screenshot_as_png.
         - target_file: need compared target file.
        '''
        temp=tempfile.mktemp()
        with open(temp,"wb") as f:
            f.write(strStream)
        simily = ImageUtil.compare(target_file, temp)
        if os.path.exists(temp):os.remove(temp)
        return simily
    
    @staticmethod
    def compare(f1, f2):
        """
        Calculate the similarity  between f1 and f2
        return similarity  0-100
        """
        img1 = Image.open(f1)
        img2 = Image.open(f2,'r')
        # if image size is not equal, return 1
        if img1.size[0] != img2.size[0] or img1.size[1] != img2.size[1]:
            return 0
        size = (256, 256)
        img1 = img1.resize(size).convert('RGB')
        img2 = img2.resize(size).convert('RGB')
        # # get the difference between the two images
        h = ImageChops.difference(img1, img2)
        size = float(img1.size[0] * img1.size[1])
        diff = 0
        for p in list(h.getdata()):
            if p != (0, 0, 0):
                diff += 1
        return round((1 - (diff / size)) * 100, 2)

    @staticmethod
    def crop(startx, starty, endx, endy, scrfile, destfile):
        """
        cut img by the given coordinates and picture, then make target file
        """
        box = (startx, starty, endx, endy)
        img = Image.open(scrfile)
        cut_img = img.crop(box)
        if cut_img:
            cut_img.save(destfile)
            return True
        else:
            return False
        
    @staticmethod
    def rmBlackBorder(
                srcpath,  # input image
                tarpath,
                thres,  # threshold for cropping: sum([r,g,b] - [0,0,0](black))
                diff,  # max tolerable difference between black borders on two side
                shrink,  # number of pixels to shrink after the blackBorders removed
                directionMore  # 哪个方向上多出不对称的内容，0：正常，1：上，2：下,3：左，4：右
                ):
        blackBorderCheck(srcpath,tarpath,thres,diff,shrink,directionMore)
        

######################
class Verify:
    """
    Class verify is specially used for element attribute validation.
    Including Text、Image、Content_Desc and etc.
    """
    @staticmethod
    def verifyText(srcText, desText):
        """
        Verify element's Text of attribute whether is equal to the text you set.
        :Args: text
        :Return: True or False
        """
        if srcText == desText:
            return True
        return False

    @staticmethod
    def verifyNotText(srcText, desText):
        """
        This is the opposite of verifyText.
        :Args: text
        :Return: True or False
        """
        return not Verify.verifyText(srcText, desText)

    @staticmethod
    def verifyImage(srcImage, dstImage, similarity=100):
        """
        Verify element's Image whether is equal to the image you set.
        :Args: image
        :Return: similarity  0-100
        """
        return ImageUtil.compare(srcImage,dstImage) >= similarity

    @staticmethod
    def verifyTextRe(searchText, checkText):
        """
        Verify element's Text of attribute whether is about equal to the text you set.
        :Args: text
        :Return: True or False
        """
        if re.search(checkText,searchText):
            return True
        return False

    @staticmethod
    def verifyNotTextRe(searchText, checkText):
        """
        This is the opposite of verifyTextRe
        :Args: text
        :Return: True or False
        """
        return not Verify.verifyTextRe(searchText, checkText)
if __name__ == '__main__':

    path = r"C:\Program Files\AutoRecorder\workspace\test_tool\tools\test.png"
    path2 = r"C:\Program Files\AutoRecorder\workspace\test_tool\tools\test2.png"
    print ImageUtil.rmBlackBorder(path, path2, 50,1000,0,0)