import sys
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.graphics import Color, Rectangle
from random import random as r
from kivy.clock import Clock
from functools import partial
from e_drive.drone import Drone
from e_drive.system import DeviceType
from e_drive.protocol import DataType
import colorama
from colorama import Fore, Back, Style


class CardReader(App):

    def open(self):

        #self.drone = Drone(True, True, True, True, True)
        self.drone = Drone()
        if self.drone.open() == False:
            print(Fore.RED + "* Error : Unable to open serial port." + Style.RESET_ALL)
            sys.exit(1)
        
        # 이벤트 핸들링 함수 등록
        self.drone.setEventHandler(DataType.RawCard, self.eventRawCard)

        # call my_callback every 0.5 seconds
        Clock.schedule_interval(self.my_callback, 0.2)


    # dt means delta-time
    def my_callback(self, dt):

        self.drone.sendRequest(DeviceType.Drone, DataType.RawCard)


    def eventRawCard(self, rawCard):

        self.l3MiddleLabelFrontRgb.text = (
            "{0:0.2}, ".format(float(rawCard.rgb[0][0]) / 255.0) + 
            "{0:0.2}, ".format(float(rawCard.rgb[0][1]) / 255.0) + 
            "{0:0.2}".format(float(rawCard.rgb[0][2]) / 255.0) )

        self.l3MiddleLabelFrontHsv.text = (
            "{0:0.2}, ".format(float(rawCard.hsv[0][0]) / 255.0) + 
            "{0:0.2}, ".format(float(rawCard.hsv[0][1]) / 255.0) + 
            "{0:0.2}".format(float(rawCard.hsv[0][2]) / 255.0) )

        self.l3MiddleLabelFrontColor.text = ( rawCard.color[0].name )

        self.l3RightLabelFrontRgb.text = (
            "{0:0.2}, ".format(float(rawCard.rgb[1][0]) / 255.0) + 
            "{0:0.2}, ".format(float(rawCard.rgb[1][1]) / 255.0) + 
            "{0:0.2}".format(float(rawCard.rgb[1][2]) / 255.0) )

        self.l3RightLabelFrontHsv.text = (
            "{0:0.2}, ".format(float(rawCard.hsv[1][0]) / 255.0) + 
            "{0:0.2}, ".format(float(rawCard.hsv[1][1]) / 255.0) + 
            "{0:0.2}".format(float(rawCard.hsv[1][2]) / 255.0) )

        self.l3RightLabelFrontColor.text = ( rawCard.color[1].name )

        self.l2WidgetFront.canvas.clear()
        self.l2WidgetRear.canvas.clear()

        with self.l2WidgetFront.canvas:
            Color( float(rawCard.rgb[0][0]) / 255.0, float(rawCard.rgb[0][1]) / 255.0, float(rawCard.rgb[0][2]) / 255.0 )
            Rectangle(pos=(0, 120 + self.widgetRear.height), size=(self.widgetFront.width, self.widgetFront.height))

        with self.l2WidgetRear.canvas:
            Color( float(rawCard.rgb[1][0]) / 255.0, float(rawCard.rgb[1][1]) / 255.0, float(rawCard.rgb[1][2]) / 255.0 )
            Rectangle(pos=(0, 120), size=(self.widgetRear.width, self.widgetRear.height))


    def build(self):

        self.l2WidgetFront = Widget()
        self.l2WidgetRear = Widget()

        self.l3LeftLabelFrontRgb = Label(text='RGB')
        self.l3LeftLabelFrontHsv = Label(text='HSV')
        self.l3LeftLabelFrontColor = Label(text='Color')
        
        self.l3MiddleLabelFrontRgb = Label(text='0')
        self.l3MiddleLabelFrontHsv = Label(text='0')
        self.l3MiddleLabelFrontColor = Label(text='0')
        
        self.l3RightLabelFrontRgb = Label(text='0')
        self.l3RightLabelFrontHsv = Label(text='0')
        self.l3RightLabelFrontColor = Label(text='0')

        l3Left = BoxLayout(orientation='vertical')
        l3Left.add_widget(self.l3LeftLabelFrontRgb)
        l3Left.add_widget(self.l3LeftLabelFrontHsv)
        l3Left.add_widget(self.l3LeftLabelFrontColor)

        l3Middle = BoxLayout(orientation='vertical')
        l3Middle.add_widget(self.l3MiddleLabelFrontRgb)
        l3Middle.add_widget(self.l3MiddleLabelFrontHsv)
        l3Middle.add_widget(self.l3MiddleLabelFrontColor)

        l3Right = BoxLayout(orientation='vertical')
        l3Right.add_widget(self.l3RightLabelFrontRgb)
        l3Right.add_widget(self.l3RightLabelFrontHsv)
        l3Right.add_widget(self.l3RightLabelFrontColor)

        l2ButtonQuit = Button(text='Quit', on_press=partial(self.closeApplication))
        
        l2Bottom = BoxLayout(size_hint=(1, None), height=120)
        l2Bottom.add_widget(l3Left)
        l2Bottom.add_widget(l3Middle)
        l2Bottom.add_widget(l3Right)
        l2Bottom.add_widget(l2ButtonQuit)

        l1Base = BoxLayout(orientation='vertical')
        l1Base.add_widget(self.l2WidgetFront)
        l1Base.add_widget(self.l2WidgetRear)
        l1Base.add_widget(l2Bottom)

        self.open()

        return l1Base


    def closeApplication(self):
        if (self.drone != None):
            self.drone.close()
        
        sys.exit(1)

