from datetime import datetime, timedelta

import AppKit
import Foundation
import PyObjCTools.AppHelper


class App(Foundation.NSObject):
    duration = paused_at = started_at = status_item = None
    callbacks = {}

    @classmethod
    def callback_(cls, sender):
        if not isinstance(sender, (AppKit.NSMenuItem, Foundation.NSTimer)):
            raise NotImplementedError(sender)
        try:
            cls.callbacks[sender](sender)
        except:
            import traceback
            traceback.print_exc()

    @classmethod
    def restart_timer(cls, _):
        cls.started_at = datetime.now()

    @classmethod
    def timer_callback(cls, _):
        if not cls.duration:
            cls.duration = timedelta(minutes=20)
        if not cls.started_at:
            cls.restart_timer(_)
        dt = (cls.paused_at or datetime.now()) - cls.started_at
        title = '= ' if cls.paused_at else ''
        if dt > cls.duration:
            dt -= cls.duration
            if 'OVER' not in cls.status_item.title():
                title = 'OVER '
            title += '-'
        else:
            dt = cls.duration - dt
        title += '{:02}:{:02}'.format(*divmod(dt.seconds, 60))
        cls.status_item.setTitle_(title)

    @classmethod
    def pause_timer(cls, sender):
        if cls.paused_at:
            cls.started_at = datetime.now() - (cls.paused_at - cls.started_at)
            cls.paused_at = None
            sender.setTitle_('Pause')
        else:
            cls.paused_at = datetime.now()
            sender.setTitle_('Continue')

    @classmethod
    def menu_item(cls, title, callback, action='callback:', key=''):
        mi = AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(title, action, key)
        mi.setTarget_(cls)
        cls.callbacks[mi] = callback
        return mi

    @classmethod
    def run(cls):
        app = cls.alloc().init()

        application = AppKit.NSApplication.sharedApplication()
        application.setActivationPolicy_(AppKit.NSApplicationActivationPolicyAccessory)
        application.setDelegate_(app)

        timer = Foundation.NSTimer.alloc().initWithFireDate_interval_target_selector_userInfo_repeats_(
            Foundation.NSDate.date(), 0.5, cls, 'callback:', None, True)
        cls.callbacks[timer] = cls.timer_callback
        Foundation.NSRunLoop.currentRunLoop().addTimer_forMode_(timer, Foundation.NSDefaultRunLoopMode)

        menu = AppKit.NSMenu.alloc().init()
        menu.addItem_(cls.menu_item('Restart', callback=cls.restart_timer))
        menu.addItem_(AppKit.NSMenuItem.separatorItem())
        menu.addItem_(cls.menu_item('Pause', callback=cls.pause_timer))
        menu.addItem_(AppKit.NSMenuItem.separatorItem())
        menu.addItem_(cls.menu_item('Quit', callback=lambda _: application.terminate_(application)))

        cls.status_item = AppKit.NSStatusBar.systemStatusBar().statusItemWithLength_(-1)
        cls.status_item.setMenu_(menu)

        PyObjCTools.AppHelper.installMachInterrupt()
        PyObjCTools.AppHelper.runEventLoop()
