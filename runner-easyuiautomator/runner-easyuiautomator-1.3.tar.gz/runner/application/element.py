#coding=utf-8
'''
Created on 2016年5月25日

@author: Hal
'''
from runner.common.log import Logger
from easyuiautomator.driver.common.by import By
from easyuiautomator.driver.element import Element

class TestElement(Element):
    
    def __init__(self, parent, _id):
        super(TestElement, self).__init__(parent, _id)
        self.logger = Logger.getLogger()
    
    def find_element(self, by=By.ID, value=None, thinkTime=None, timeOut=None, ignoreExp=False):
        self.logger.info("find child element by %s value %s"%(by,value))
        return Element.find_element(self, by, value, thinkTime, timeOut, ignoreExp=ignoreExp)
        
    def find_elements(self, by=By.ID, value=None, thinkTime=None, timeOut=None, ignoreExp=False):
        self.logger.info("find child elements by %s"%value)
        return Element.find_elements(self, by, value, thinkTime, timeOut, ignoreExp=ignoreExp)
    
    def find_element_by_id(self, id_, thinkTime=None, timeOut=None, ignoreExp=False):
        return self.find_element(By.ID, id_, thinkTime, timeOut, ignoreExp)
    
    def find_elements_by_id(self, id_, thinkTime=None, timeOut=None, ignoreExp=False):
        return self.find_elements(By.ID, id_, thinkTime, timeOut, ignoreExp)
    
    def find_element_by_name(self, name, thinkTime=None, timeOut=None, ignoreExp=False):
        return self.find_element(By.NAME, name, thinkTime, timeOut, ignoreExp)
    
    def find_elements_by_name(self, name, thinkTime=None, timeOut=None, ignoreExp=False):
        return self.find_elements(By.NAME, name, thinkTime, timeOut, ignoreExp)
    
    def find_element_by_class_name(self, name, thinkTime=None, timeOut=None, ignoreExp=False):
        return self.find_element(By.CLASS_NAME, name, thinkTime, timeOut, ignoreExp)
    
    def find_elements_by_class_name(self, name, thinkTime=None, timeOut=None, ignoreExp=False):
        return self.find_elements(By.CLASS_NAME, name, thinkTime, timeOut, ignoreExp)
    
    def find_element_by_accessibility_id(self, id_, thinkTime=None, timeOut=None, ignoreExp=False):
        return self.find_element(By.ACCESSIBILITY_ID, id_, thinkTime, timeOut, ignoreExp)
    
    def find_elements_by_accessibility_id(self, id_, thinkTime=None, timeOut=None, ignoreExp=False):
        return self.find_elements(By.ACCESSIBILITY_ID, id_, thinkTime, timeOut, ignoreExp)
    
    def find_element_by_xpath(self, xpath, thinkTime=None, timeOut=None, ignoreExp=False):
        return self.find_element(By.XPATH, xpath, thinkTime, timeOut, ignoreExp)
    
    def find_elements_by_xpath(self, xpath, thinkTime=None, timeOut=None, ignoreExp=False):
        return self.find_elements(By.XPATH, xpath, thinkTime, timeOut, ignoreExp)
    
    def find_element_by_uiautomator(self, uia_string, thinkTime=None, timeOut=None, ignoreExp=False):
        return self.find_element(By.ANDROID_UIAUTOMATOR, uia_string, thinkTime, timeOut, ignoreExp)
    
    def find_elements_by_uiautomator(self, uia_string, thinkTime=None, timeOut=None, ignoreExp=False):
        return self.find_elements(By.ANDROID_UIAUTOMATOR, uia_string, thinkTime, timeOut, ignoreExp)

    def click(self):
        self.logger.info("click")
        Element.click(self) 
        return self
       
    def longClick(self,duration=None):
        self.logger.info("long click")
        Element.longClick(self, duration) 
        return self  
         
    def setText(self, value,replace=True):
        self.logger.info("set text as %s"%value)
        return Element.setText(self, value,replace) 
    
    def getParent(self):
        self.logger.info("get parent")
        return Element.getParent(self)
     
    def getText(self):
        self.logger.info("get text")
        return Element.getText(self)
     
    def getResourceId(self):
        self.logger.info("get resourceID")
        return Element.getResourceId(self)
     
    def getClassName(self):
        self.logger.info("get class name")
        return Element.getClassName(self)
     
    def getContent_Desc(self):
        self.logger.info("get content_desc")
        return Element.getContent_Desc(self)
     
    def isChecked(self):
        self.logger.info("is checked")
        return Element.isChecked(self)
     
    def isCheckable(self):
        self.logger.info("is checkable")
        return Element.isCheckable(self)
     
    def isClickable(self):
        self.logger.info("is clickable")
        return Element.isClickable(self)
     
    def isEnabled(self):
        self.logger.info("is enabled")
        return Element.isEnabled(self)
     
    def isFocuable(self):
        self.logger.info("is focuable")
        return Element.isFocuable(self)
     
    def isFocused(self):
        self.logger.info("is focused")
        return Element.isFocused(self)
     
    def isScrollable(self):
        self.logger.info("is scrollable")
        return Element.isScrollable(self)
     
    def isSelected(self):
        self.logger.info("is selected")
        return Element.isSelected(self)
     
    def isLongClickable(self):
        self.logger.info("is longclickable")
        return Element.isLongClickable(self)
     
    def isDisplayed(self):
        self.logger.info("is displayed")
        return Element.isDisplayed(self)
     
    def getSize(self):
        self.logger.info("get size")
        return Element.getSize(self)
     
    def getLocation(self):
        self.logger.info("get location")
        return Element.getLocation(self)
     
    def clear(self):
        self.logger.info("clear")
        Element.clear(self)
         
    def get_screenshot_as_file(self, filename):
        self.logger.info("get screenshot save to %s"%str(filename))
        return Element.get_screenshot_as_file(self, filename)
     
    def dragToEle(self, element, duration=None):
        self.logger.info("drag to ele")
        return Element.dragToEle(self, element, duration=duration)
     
    def dragToPos(self, x, y, duration=None):
        self.logger.info("drag to (%d, %d)"%(x,y))   
        return Element.dragToPos(self, x, y, duration=duration)
     
    def scroll(self, destination_el):
        self.logger.info("scroll ele")
        return Element.scroll(self, destination_el)
     
    def scrollTo(self, text, direction='vertical'):
        self.logger.info("scroll to %s"%text)
        return Element.scrollTo(self, text, direction=direction)
     
    def scrollBottom(self, duration=None):
        self.logger.info("scroll to bottom")
        return Element.scrollBottom(self, duration=duration)
     
    def scrollTop(self, duration=None):
        self.logger.info("scroll to top")
        return Element.scrollTop(self, duration=duration)
     
    def swipeDown(self, duration=None):
        self.logger.info("swipe down")
        return Element.swipeDown(self, duration=duration)
     
    def swipeLeft(self, duration=None):
        self.logger.info("swipe left")
        return Element.swipeLeft(self, duration=duration)
     
    def swipeRight(self, duration=None):
        self.logger.info("swipe right")
        return Element.swipeRight(self, duration=duration)
     
    def swipeUp(self, duration=None):
        self.logger.info("swipe up")
        return Element.swipeUp(self, duration=duration)
     
    def pinch(self, percent=200, steps=50):
        self.logger.info("pinch percent %d"%percent)
        return Element.pinch(self, percent=percent, steps=steps)
     
    def zoom(self, percent=200, steps=50):
        self.logger.info("zoom percent %s"%percent)
        return Element.zoom(self, percent=percent, steps=steps)
    
    def verifyImage(self, Image, similarity=100):
        self.logger.info("verify by image similarity: %d"%similarity)
        return Element.verifyImage(self, Image, similarity=similarity)
    
    def verifyContent_Desc(self, content_desc):
        self.logger.info("verify by content_desc: %s"%content_desc)
        return Element.verifyContent_Desc(self, content_desc)
     
    def verifyNotContent_Desc(self, content_desc):
        self.logger.info("verify not content_desc: %s"%content_desc)
        return Element.verifyNotContent_Desc(self, content_desc)
    
    def verifyContent_DescRe(self, content_desc):
        self.logger.info("verify by content_descre: %s"%content_desc)
        return Element.verifyContent_DescRe(self, content_desc)
      
    def verifyNotContent_DescRe(self, content_desc):
        self.logger.info("verify not content_descre: %s"%content_desc)
        return Element.verifyNotContent_DescRe(self, content_desc)
    
    def verifyText(self, text):
        self.logger.info("verify text: %s"%text)
        return Element.verifyText(self, text)
    
    def verifyNotText(self, text):
        self.logger.info("verify not text: %s"%text)
        return Element.verifyNotText(self, text)
    
    def verifyTextRe(self, text):
        self.logger.info("verify textre: %s"%text)
        return Element.verifyTextRe(self, text)
    
    def verifyNotTextRe(self, text):
        self.logger.info("verify not textre: %s"%text)
        return Element.verifyNotTextRe(self, text)
    
    