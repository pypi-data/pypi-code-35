#coding=utf-8
'''
Created on 2017年3月27日

@author: Administrator
'''
import unittest
from easyuiautomator.driver.driver import Driver
Driver.set_debug()
app = Driver.connect_device()

class TestElement(unittest.TestCase):


    def testAttribute(self):
        ele = app.find_element_by_accessibility_id("联系人")
        print "text: " + ele.getText()
        print "resourceId: " + ele.getResourceId()
        print "classname: " + ele.getClassName()
        print "package: "
        print "context-desc: "
        print "checkable: " + str(ele.isCheckable())
        print "Checked: " + str(ele.isChecked())
        print "clickable: " + str(ele.isClickable())
        print "enabled: " + str(ele.isEnabled())
        print "focuable: " + str(ele.isFocuable())
        print "focused: " + str(ele.isFocused())
        print "scrollable: " + str(ele.isScrollable())
        print "longclickable: " + str(ele.isLongClickable())
        print "seleceted : " + str(ele.isSelected())
        print "diaplayed: " + str(ele.isDisplayed())
        print "location: " + str(ele.getLocation())
        print "size: " + str(ele.getSize())


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()