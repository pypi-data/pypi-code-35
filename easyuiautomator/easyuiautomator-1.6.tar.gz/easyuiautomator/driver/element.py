# coding=utf-8

'''
Created on 2015年11月5日

@author: thomas.ning
'''
import base64,tempfile,os,sys
from .common.by import By
from easyuiautomator.common.exceptions import InvalidSelectorException
from easyuiautomator.common.exceptions import DeviceNotFound
from easyuiautomator.driver.common.mobilecommand import MobileCommand as Command
from easyuiautomator.common.log import Logger
from easyuiautomator.driver.executor.utils import Verify
from easyuiautomator.driver.common.touch_action import TouchAction
from easyuiautomator.driver.executor.utils import ImageUtil


# 收集异常信息
def collectException(func):
    def wrap(*args, **argkw):
        try:
            return func(*args, **argkw)
        except DeviceNotFound, e:
            raise DeviceNotFound(e)
        except:
            msg = sys.exc_info()[1].message
            Logger.getLogger().warning("%s is failed [%s]" % (func.__name__, msg))  
            if 'ignoreExp' not in  argkw.keys():
                raise
            if not argkw['ignoreExp']:
                raise  
    return wrap

class Element(object):
    '''
    All actions of element.

    - element - a element you get by find_element in driver.
    '''

    def __init__(self, parent, id_):
        self._parent = parent
        self._id = id_
        
    @collectException
    def find_element(self, by=By.ID, value=None, thinkTime=None, timeOut=None, ignoreExp=False):
        '''
        Find element by parent element.

        :Args:
         - by - parent element
         - value - text

        :Usage:
            element.find_element(parent_element)
        '''
        if not By.is_valid(by) or not isinstance(value, str):
            raise InvalidSelectorException("Invalid locator values passed in")
        if thinkTime is not None :
            thinkTime = float(thinkTime)
        if timeOut is not None:
            timeOut = float(timeOut)
        return self._execute(Command.FINE_CHILD_ELEMNT,
                             {'using': by, 
                              'value': value, 
                              'thinkTime':thinkTime, 
                              'timeOut':timeOut})['value']
    @collectException
    def find_elements(self, by=By.ID, value=None, thinkTime=None, timeOut=None, ignoreExp=False):
        '''
        Find elements by parent element.

        :Args:
         - by - parent element
         - value - text

        :Usage:
            element.find_elements(parent_element)
        '''
        if not By.is_valid(by) or not isinstance(value, str):
            raise InvalidSelectorException("Invalid locator values passed in")
        if thinkTime is not None :
            thinkTime = float(thinkTime)
        if timeOut is not None:
            timeOut = float(timeOut)
        return self._execute(Command.FINE_CHILD_ELEMNTS,
                             {'using': by, 
                              'value': value, 
                              'thinkTime':thinkTime, 
                              'timeOut':timeOut})['value']

    def find_element_by_id(self, id_, thinkTime=None, timeOut=None, ignoreExp=False):
        """Finds an element by id.

        :Args:
         - id\_ - The id of the element to be found.

        :Usage:
            element.find_element_by_id('foo')
        """
        return self.find_element(by=By.ID, value=id_, thinkTime=thinkTime, timeOut=timeOut, ignoreExp=ignoreExp)

    def find_elements_by_id(self, id_, thinkTime=None, timeOut=None, ignoreExp=False):
        """
        Finds multiple elements by id.

        :Args:
         - id\_ - The id of the elements to be found.

        :Usage:
            element.find_elements_by_id('foo')
        """
        return self.find_elements(by=By.ID, value=id_, thinkTime=thinkTime, timeOut=timeOut, ignoreExp=ignoreExp)

    def find_element_by_xpath(self, xpath, thinkTime=None, timeOut=None, ignoreExp=False):
        """
        Finds an element by xpath.

        :Args:
         - xpath - The xpath locator of the element to find.

        :Usage:
            element.find_element_by_xpath('//div/td[1]')
        """
        return self.find_element(by=By.XPATH, value=xpath, thinkTime=thinkTime, timeOut=timeOut, ignoreExp=ignoreExp)

    def find_elements_by_xpath(self, xpath, thinkTime=None, timeOut=None, ignoreExp=False):
        """
        Finds multiple elements by xpath.

        :Args:
         - xpath - The xpath locator of the elements to be found.

        :Usage:
            element.find_elements_by_xpath("//div[contains(@class, 'foo')]")
        """
        return self.find_elements(by=By.XPATH, value=xpath, thinkTime=thinkTime, timeOut=timeOut, ignoreExp=ignoreExp)

    def find_element_by_name(self, name, thinkTime=None, timeOut=None, ignoreExp=False):
        """
        Finds an element by name.

        :Args:
         - name: The name of the element to find.

        :Usage:
            element.find_element_by_name('foo')
        """
        return self.find_element(by=By.NAME, value=name, thinkTime=thinkTime, timeOut=timeOut, ignoreExp=ignoreExp)

    def find_elements_by_name(self, name, thinkTime=None, timeOut=None, ignoreExp=False):
        """
        Finds elements by name.

        :Args:
         - name: The name of the elements to find.

        :Usage:
            element.find_elements_by_name('foo')
        """
        return self.find_elements(by=By.NAME, value=name, thinkTime=thinkTime, timeOut=timeOut, ignoreExp=ignoreExp)

    def find_element_by_class_name(self, name, thinkTime=None, timeOut=None, ignoreExp=False):
        """
        Finds an element by class name.

        :Args:
         - name: The class name of the element to find.

        :Usage:
            element.find_element_by_class_name('foo')
        """
        return self.find_element(by=By.CLASS_NAME, value=name, thinkTime=thinkTime, timeOut=timeOut, ignoreExp=ignoreExp)

    def find_elements_by_class_name(self, name, thinkTime=None, timeOut=None, ignoreExp=False):
        """
        Finds elements by class name.

        :Args:
         - name: The class name of the elements to find.

        :Usage:
            element.find_elements_by_class_name('foo')
        """
        return self.find_elements(by=By.CLASS_NAME, value=name, thinkTime=thinkTime, timeOut=timeOut, ignoreExp=ignoreExp)

    def find_element_by_uiautomator(self, uia_string, thinkTime=None, timeOut=None, ignoreExp=False):
        """Finds element by uiautomator in Android.

        :Args:
         - uia_string - The element name in the Android UIAutomator library

        :Usage:
            element.find_element_by_android_uiautomator('.elements()[1].cells()[2]')
        """
        return self.find_element(by=By.ANDROID_UIAUTOMATOR, value=uia_string, thinkTime=thinkTime, timeOut=timeOut, ignoreExp=ignoreExp)

    def find_elements_by_uiautomator(self, uia_string, thinkTime=None, timeOut=None, ignoreExp=False):
        """Finds elements by uiautomator in Android.

        :Args:
         - uia_string - The element name in the Android UIAutomator library

        :Usage:
            element.find_elements_by_android_uiautomator('.elements()[1].cells()[2]')
        """
        return self.find_elements(by=By.ANDROID_UIAUTOMATOR, value=uia_string, thinkTime=thinkTime, timeOut=timeOut, ignoreExp=ignoreExp)

    def find_element_by_accessibility_id(self, id_, thinkTime=None, timeOut=None, ignoreExp=False):
        """Finds an element by accessibility id.

        :Args:
         - id - a string corresponding to a recursive element search using the
         Id/Name that the native Accessibility options utilize

        :Usage:
            element.find_element_by_accessibility_id()
        """
        return self.find_element(by=By.ACCESSIBILITY_ID, value=id_, thinkTime=thinkTime, timeOut=timeOut, ignoreExp=ignoreExp)

    def find_elements_by_accessibility_id(self, id_, thinkTime=None, timeOut=None, ignoreExp=False):
        """Finds elements by accessibility id.

        :Args:
         - id - a string corresponding to a recursive element search using the
         Id/Name that the native Accessibility options utilize

        :Usage:
            element.find_elements_by_accessibility_id()
        """
        return self.find_elements(by=By.ACCESSIBILITY_ID, value=id_, thinkTime=thinkTime, timeOut=timeOut, ignoreExp=ignoreExp)
    
    def _execute(self, command, params=None):

        if params is None:
            params = {}
        params['id'] = self._id
        return self._parent._execute(command, params)

    def click(self):
        """Clicks the element.

        :Usage:
            element.click()
        """
        self._execute(Command.CLICK)

    def longClick(self, duration=None):
        """long Clicks the element.

        :Usage:
            element.longClick(duration)
        """
        opts = {
                'duration':duration
                }
        self._execute(Command.LONG_CLICK, opts)

    def setText(self, value, replace=True):
        '''
        Set Text in textedit.

        :Args:
          - value - text you will set

        :Usage:
            element.setText()
        '''
        opts = {
            'text': value,
            'replace':replace
        }
        return self._execute(Command.SET_TEXT, opts)

    def getText(self):
        '''
        Get text from element attribute.

        :Usage:
            element.getText()
        '''
        return self._getAttribute("text")

    def getResourceId(self):
        '''
        Get resource id from element attribute.

        :Usage:
            element.getResourceId()
        '''
        return self._getAttribute("resourceId")
    
    def getBounds(self):
        '''
        Get bounds from element attribute.

        :Usage:
            element.getResourceId()
        '''
        return self._getAttribute("bounds")

    def getClassName(self):
        '''
        Get class name from element attribute.

        :Usage:
            element.getClassName()
        '''
        return self._getAttribute("className")

    def getContent_Desc(self):
        '''
        Get content-desc element atribute

        :Usage:
            element.getContent()
        '''
        return self._getAttribute("content_desc")
    
    def getParent(self):
        '''
        Get content-desc element atribute

        :Usage:
            element.getContent()
        '''
        return self._execute(Command.GET_PARENT)['value']

    def isChecked(self):
        '''
        Check whether element is checked.

        :Usage:
            element.isChecked()

        :Return:
            true or false
        '''
        return self._getAttribute("checked")

    def isCheckable(self):
        '''
        Check whether element is checkable.

        :Usage:
            element.isCheckable()
        '''
        return self._getAttribute("checkable")

    def isClickable(self):
        '''
        Check whether element is clickable.

        :Usage:
            element.isClickable()
        '''
        return self._getAttribute("clickable")

    def isEnabled(self):
        '''
        Check whether element is enabled.

        :Usage:
            element.isEnabled()
        '''
        return self._getAttribute("enabled")

    def isFocuable(self):
        '''
        Check whether element is focuable.

        :Usage:
            element.isFocuable()
        '''
        return self._getAttribute("focusable")

    def isFocused(self):
        '''
        Check whether element is focused.

        :Usage:
            element.isFocused()
        '''
        return self._getAttribute("focused")

    def isScrollable(self):
        '''
        Check whether element is scrollable.

        :Usage:
            element.isScrollable()
        '''
        return self._getAttribute("scrollable")

    def isLongClickable(self):
        '''
        Check whether element is longclickable.

        :Usage:
            element.isLongClickable()
        '''
        return self._getAttribute("longClickable")

    def isSelected(self):
        '''
        Check whether element is selected.

        :Usage:
            element.isSelected()
        '''
        return self._getAttribute("selected")

    def isDisplayed(self):
        '''
        Check whether element is displayed.

        :Usage:
            element.isDisplayed()
        '''
        return self._getAttribute("displayed")

    def getSize(self):
        '''
        Get size from element attribute.

        :Usage:
            element.getSize()

        :Return:
            length and width
        '''
        return self._execute(Command.GET_SIZE)['value']

    def getLocation(self):
        '''
        Get location from element attribute.

        :Usage:
            element.getLocation()

        :Return:
            x and y of element
        '''
        return self._execute(Command.GET_LOCATION)['value']

    def _getAttribute(self, attribute):
        opts = {
            "attribute": attribute
        }
        return self._execute(Command.GET_ATTRIUBTE, opts)["value"]

    def clear(self):
        '''
        Clear the text in textedit.

        :Usage:
            element.clear()
        '''
        """Clears the text if it's a text entry element."""
        
        self._execute(Command.CLEAR_ELEMENT)

    def get_screenshot_as_file(self, filename,scale=1.0,quality=50):
        """
        Gets the screenshot of the current window. Returns False if there is
           any IOError, else returns True. Use full paths in your filename.

        :Args:
         - filename: The full path you wish to save your screenshot to.

        :Usage:
            element.get_screenshot_as_file('/Screenshots/foo.png')
        """
        png = self.get_screenshot_as_png(scale,quality)
        try:
            with open(filename, 'wb') as f:
                f.write(png)
        except IOError:
            return False
        finally:
            del png
        return True

    def get_screenshot_as_png(self,scale=1.0,quality=50):
        """
        Gets the screenshot of the current window as a binary data.
        
        :Args:
         - scale: The screen size scale,default:1.0.
         - quality: The screen quality,default:50%  0-100.
        
        :Usage:
            driver.get_screenshot_as_png(0.8,80%)
        """
        return base64.b64decode(self.get_screenshot_as_base64(scale,quality).encode('ascii'))

    def get_screenshot_as_base64(self,scale=1.0,quality=50):
        """
        Gets the screenshot of the current window as a base64 encoded string
           which is useful in embedded images in HTML.
        
        :Args:
         - scale: The screen size scale,default:1.0.
         - quality: The screen quality,default:50%  0-100.
        
        :Usage:
            driver.get_screenshot_as_base64()
        
        """
#         opts = {
#             "scale": scale,
#             "quality": quality
#         }
        return self._overdo_takeshot()
#         return self._execute(Command.SCREENSHOT, opts)['value']
    
    def _overdo_takeshot(self):
        temp = tempfile.mktemp()
        temp_dest = tempfile.mktemp(suffix=".png")
        if self._parent.get_screenshot_as_file(temp):
            startx, starty, endx, endy = self.getBounds().split(" ")
            ImageUtil.crop(float(startx), float(starty), float(endx), float(endy), temp, temp_dest)
            os.remove(temp)
            tmpContent = ""
            with open(temp_dest, 'rb') as f:
                for line in f.readlines():
                    tmpContent += line
            os.remove(temp_dest)
            return base64.b64encode(tmpContent)
              
    #####################################################################################################
    ############################################   NEW PLUS    ##########################################
    #####################################################################################################
    def dragToEle(self, element, duration=None):
        """
        The Element drag to another element's position..

        :Args:
         - element: The full path you wish to save your screenshot to.
         - duration: The time it costs.

        :Usage:
            element.dragToEle(element)
        """
        opts = {
            'destElId': element.id,
            'duration':duration
        }

        return  self._execute(Command.DRAG, opts)['value']

    def dragToPos(self, x, y, duration=None):
        """
        The Element drag to another element's position by x and y..

        :Args:
         - x: Position x
         - y: Position y
         - duration: The time it costs.

        :Usage:
            element.dragToPos(100,200)
        """
        opts = {
            'endX':x,
            'endY':y,
            'duration':duration
        }
        return  self._execute(Command.DRAG, opts)['value']

    def scroll(self, destination_el):
        """Scrolls from one element to another

        :Args:
         - destinationEl - the element to scroll to

        :Usage:
            element.scroll(el2)
        """
        action = TouchAction(self)
        action.press(self).moveTo(destination_el).release().perform()
        return self
    
    @collectException
    def scrollTo(self, text, direction='vertical'):
        """Scrolls from one element to another

        :Args:
         - text - the text to scroll to
         - direction - vertical horizontal

        :Usage:
            element.scrollTo(text)
        """
        opts = {
            'text': text,
            'direction': direction
        }
        self._execute(Command.SCROLL_TO, opts)
        return True

    def swipeLeft(self, duration=None):
        '''
        swipe from the right border of element to he left border of element with duration

        :Usage:
            element.swipeLeft(duration)
        '''
        return self._swipeOrientation("left", duration)

    def swipeRight(self, duration=None):
        '''
        swipe from the left border of element to he right border of element with duration

        :Usage:
            element.swipeRight(duration)
        '''
        return self._swipeOrientation("right", duration)

    def swipeUp(self, duration=None):
        '''
        swipe from the up border of element to he down border of element with duration

        :Usage:
            element.swipeUp(duration)
        '''
        return self._swipeOrientation("up", duration)

    def swipeDown(self, duration=None):
        '''
        swipe from the up border of element to he down border of element with duration

        :Usage:
            element.swipeDown(duration)
        '''
        return self._swipeOrientation("down", duration)

    def _swipeOrientation(self, direction, duration=None):
        '''
        swipe from the some border of element to he some border of element with duration
        base method,no suggest used
        :Args:
        dirction: left,right,up,down
        duation : from second to steps default 20

        :Usage:
            element.swipeDown(duration)
        '''
        opts = {
                'direction': direction,
                'duration' : duration
                }
        return self._execute(Command.SWIPE_ORIENTAION, opts)['value']

    def pinch(self, percent=200, steps=50):
        """Pinch on an element a certain amount

        :Args:
         - percent - (optional) amount to pinch. Defaults to 200%
         - steps - (optional) number of steps in the pinch action

        :Usage:
            element.pinch(element)
        """
        opts = {
            'percent': percent,
            'steps': steps,
        }
        self._execute(Command.PINCH, opts)
        return self

    def zoom(self, percent=200, steps=50):
        """Zooms in on an element a certain amount

        :Args:
         - element - the element to zoom
         - percent - (optional) amount to zoom. Defaults to 200%
         - steps - (optional) number of steps in the zoom action

        :Usage:
            element.zoom(element)
        """
        opts = {
            'percent': percent,
            'steps': steps,
        }
        self._execute(Command.ZOOM, opts)
        return self

    def verifyText(self, text):
        """
        Verify element's Text of attribute whether is equal to the text you set.

        :Args:
         - text:The text you want to verify.

        :Usage:
            ele.verifyText('Settings')
        """
        return Verify.verifyText(self.getText(), text)

    def verifyNotText(self, text):
        """
        This is the opposite of verifyText.

        :Args:
         - text:The text you want to verify.

        :Usage:
            ele.verifyNotText('Settings')
        """
        return Verify.verifyNotText(self.getText(), text)

    def verifyContent_Desc(self, content_desc):
        """
        Verify element's content_desc of attribute whether is equal to the text you set.

        :Args:
         - content_desc:The content_desc you want to verify.

        :Usage:
            ele.verifyContent("text....")
        """
        return Verify.verifyText(self.getText(), content_desc)

    def verifyNotContent_Desc(self, content_desc):
        """
        This is the opposite of verifyContent_desc.

        :Args:
         - content_desc:The content_desc you want to verify.

        :Usage:
            ele.verifyNotContent("text....")
        """
        return Verify.verifyNotText(self.getText(), content_desc)

    def verifyImage(self, Image, similarity=100):
        """
        Verify element's Image whether is equal to the image you set.

        :Args:
         - Image: The content_desc you want to compare.

        :Usage:
            ele.verifyImage("a/a/a.png.")
        """
        temp=tempfile.mktemp()
        if self.get_screenshot_as_file(temp):
            a=Verify.verifyImage(temp, Image, similarity)
            if os.path.exists(temp):os.remove(temp)
            return a
        else:
            return False

    def verifyTextRe(self, text):
        """
        Verify element's Text of attribute whether is about equal to the text you set.

        :Args:
         - text:The text you want to verify.

        :Usage:
            ele.verifyTextRe('Settings') or (u"邮箱")
        """
        return Verify.verifyTextRe(self.getText(), text)

    def verifyNotTextRe(self, text):
        """
        This is the opposite of verifyTextRe.

        :Args:
         - text:The text you want to verify.

        :Usage:
            ele.verifyNotTextRe('Settings') or (u"邮箱")
        """
        return Verify.verifyNotTextRe(self.getText(), text)

    def verifyContent_DescRe(self, content_desc):
        """
        Verify element's content_desc of attribute whether is equal to the text you set.

        :Args:
         - content_desc:The content_desc you want to verify.

        :Usage:
            ele.verifyContent_DescRe("text....") or (u"邮箱")
        """
        return Verify.verifyTextRe(self.getContent_Desc(), content_desc)

    def verifyNotContent_DescRe(self, content_desc):
        """
        This is the opposite of verifyContent_descRe.

        :Args:
         - content_desc:The content_desc you want to verify.

        :Usage:
            ele.verifyNotContent_DescRe("text....") or (u"邮箱")
        """
        return Verify.verifyNotTextRe(self.getContent_Desc(), content_desc)

    def scrollTop(self,duration=None):
        '''滑动到顶部,例如在电话本，文件管理中
        :Usage:
            ele.scrollTop()
        '''
        opts = {
            'direction': 'top',
            'duration' : duration
        }
        self._execute(Command.SCROLL_ORIENTAION, opts)
        return self

    def scrollBottom(self,duration=None):
        '''滑动到底部，例如在电话本，文件管理中
        API适用于ListView 或 ScrollView 等可滑动的元素

        :Usage:
            ele.scrollBottom()
        '''
        opts = {
            'direction': 'bottom',
            'duration' : duration
        }

        self._execute(Command.SCROLL_ORIENTAION, opts)
        return self

########################################################################
    @property
    def parent(self):
        return self._parent

    @property
    def id(self):
        return self._id

    def __eq__(self, element):
        return hasattr(element, 'id') and self._id == element.id

    def __ne__(self, element):
        return not self.__eq__(element)
