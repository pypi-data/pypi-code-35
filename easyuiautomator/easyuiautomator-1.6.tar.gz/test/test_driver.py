# coding=utf-8

from easyuiautomator.driver.driver import Driver
import unittest
from easyuiautomator.driver.common.keyevent import KeyCode
from easyuiautomator.driver.common.touch_action import TouchAction
from easyuiautomator.driver.common.multi_action import MultiAction
import time
app = Driver.connect_device()

class TestDriver(unittest.TestCase):
    
    def test_003_get_page_source(self):
        print app.get_device_size()
        print app.get_page_source()
        print app.get_current_activity()
        print app.getOrientation()

    def test_004_press_keycode(self):
        print app.longpress_keycode(KeyCode.KEYCODE_MENU)
        print app.back()

    def test_touch_action(self):
        el = app.find_element_by_id("com.asus.gallery:id/gl_root_view")
        action = TouchAction(app)
        action.press(el).wait(1) \
            .moveTo(x=563, y=895).wait(1) \
            .moveTo(x=563, y=1211).wait(1) \
            .moveTo(x=563, y=1508).wait(1) \
            .release().perform()

    def test_006_multi_action(self):
        action1 = TouchAction(app)
        action1.press(x=243, y=500).wait(100) \
            .moveTo(x=563, y=895).wait(100) \
            .moveTo(x=563, y=1211).wait(100) \
            .moveTo(x=563, y=1508).wait(100) \
            .release()

        action2 = TouchAction(app)
        action2.press(x=500, y=600).wait(1) \
            .moveTo(x=563, y=895).wait(100) \
            .moveTo(x=563, y=1211).wait(100) \
            .moveTo(x=563, y=1508).wait(100) \
            .release()
        mm = MultiAction(app)
        mm.add(action1, action2).perform()

    def test_007_common(self):
        app.wake()  # 唤醒屏幕
        app.compressed_layout_hierarchy()  # 开启uiautomator压缩模式
        app.open_notification()  # 打开通知栏
        print app.get_device_size()
        app.get_screenshot_as_file(r"d:\123.png")

    def test_008_adb_action(self):
        print app.is_app_installed('com.example.uibestpractice')
        print app.start_activity('com.example.uibestpractice', '.MainActivity')
        print app.get_current_activity()
        print app.background(2)
        print app.lock()
        app.wake()
        print app.install_app('C:/Users/fengbo/Downloads/csdn.apk')
        print app.launch_app('net.csdn.csdnplus', '.activity.SwitchLoginActivity')
        print app.close_app('net.csdn.csdnplus')
        print app.reset('net.csdn.csdnplus')
        print app.remove_app('net.csdn.csdnplus')
        print app.push_file('D:/current.txt', 'storage/sdcard0/screen.txt')
        print app.pull_file('storage/sdcard0/360Download/new2.txt', 'D:/')
        print app.hide_keyboard()

    def test_010_zoom_pinch(self):
        ele = app.find_element_by_id("com.asus.gallery:id/gallery_root")
        app.zoom(ele)
        time.sleep(2)
        app.pinch(ele)

    def test_011_tap(self):
        app.tap([(152, 1307), (118, 1307), (520, 1307)])
        
    def test_012_setText(self):
        ele = app.find_element_by_id('com.yep.test.tools:id/edit_phone')
        ele.clear()

    def test_013_get_current_activity(self):
        print app.get_current_activity

    def test_014_scrollTo(self):
        el = app.find_element_by_class_name("android.widget.ListView")
        app.scrollTo(el, "106906621653", 'vertical')

    def test_015_wake_up(self):
        app.wake()
        app.close_app('')
    
    def test_016_find_imag_position(self):
        print app.find_img_position('res/dump_1.png', 'res/dump_2.png')


