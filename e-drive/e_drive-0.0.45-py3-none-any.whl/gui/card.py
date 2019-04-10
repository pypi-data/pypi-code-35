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

        self.labelFrontRgbRaw.text = (
            "{0:3}, ".format(rawCard.rgbRaw[0][0]) + 
            "{0:3}, ".format(rawCard.rgbRaw[0][1]) + 
            "{0:3}".format(rawCard.rgbRaw[0][2]) )

        self.labelFrontRgb.text = (
            "{0:3}, ".format(rawCard.rgb[0][0]) + 
            "{0:3}, ".format(rawCard.rgb[0][1]) + 
            "{0:3}".format(rawCard.rgb[0][2]) )

        self.labelFrontHsv.text = (
            "{0:3}, ".format(rawCard.hsv[0][0]) + 
            "{0:3}, ".format(rawCard.hsv[0][1]) + 
            "{0:3}".format(rawCard.hsv[0][2]) )

        self.labelFrontColor.text = ( rawCard.color[0].name )

        self.labelRearRgbRaw.text = (
            "{0:3}, ".format(rawCard.rgbRaw[1][0]) + 
            "{0:3}, ".format(rawCard.rgbRaw[1][1]) + 
            "{0:3}".format(rawCard.rgbRaw[1][2]) )

        self.labelRearRgb.text = (
            "{0:3}, ".format(rawCard.rgb[1][0]) + 
            "{0:3}, ".format(rawCard.rgb[1][1]) + 
            "{0:3}".format(rawCard.rgb[1][2]) )

        self.labelRearHsv.text = (
            "{0:3}, ".format(rawCard.hsv[1][0]) + 
            "{0:3}, ".format(rawCard.hsv[1][1]) + 
            "{0:3}".format(rawCard.hsv[1][2]) )

        self.labelRearColor.text = ( rawCard.color[1].name )

        self.widgetCardFront.canvas.clear()
        self.widgetCardRear.canvas.clear()

        with self.widgetCardFront.canvas:
            Color( float(rawCard.rgb[0][0]) / 255.0, float(rawCard.rgb[0][1]) / 255.0, float(rawCard.rgb[0][2]) / 255.0 )
            Rectangle(pos=(0, 120 + self.widgetCardRear.height), size=(self.widgetCardFront.width, self.widgetCardFront.height))

        with self.widgetCardRear.canvas:
            Color( float(rawCard.rgb[1][0]) / 255.0, float(rawCard.rgb[1][1]) / 255.0, float(rawCard.rgb[1][2]) / 255.0 )
            Rectangle(pos=(0, 120), size=(self.widgetCardRear.width, self.widgetCardRear.height))


    def build(self):

        self.widgetCardFront = Widget()
        self.widgetCardRear = Widget()

        labelRgbRaw = Label(text='RGB RAW')
        labelRgb = Label(text='RGB')
        labelHsv = Label(text='HSV')
        labelColor = Label(text='Color')

        self.labelFrontRgbRaw = Label(text='0')
        self.labelFrontRgb = Label(text='0')
        self.labelFrontHsv = Label(text='0')
        self.labelFrontColor = Label(text='0')
        
        self.labelRearRgbRaw = Label(text='0')
        self.labelRearRgb = Label(text='0')
        self.labelRearHsv = Label(text='0')
        self.labelRearColor = Label(text='0')

        l3Left = BoxLayout(orientation='vertical')
        l3Left.add_widget(labelRgbRaw)
        l3Left.add_widget(labelRgb)
        l3Left.add_widget(labelHsv)
        l3Left.add_widget(labelColor)

        l3Middle = BoxLayout(orientation='vertical')
        l3Middle.add_widget(self.labelFrontRgbRaw)
        l3Middle.add_widget(self.labelFrontRgb)
        l3Middle.add_widget(self.labelFrontHsv)
        l3Middle.add_widget(self.labelFrontColor)

        l3Right = BoxLayout(orientation='vertical')
        l3Right.add_widget(self.labelRearRgbRaw)
        l3Right.add_widget(self.labelRearRgb)
        l3Right.add_widget(self.labelRearHsv)
        l3Right.add_widget(self.labelRearColor)

        buttonQuit = Button(text='Quit', on_press=partial(self.closeApplication))
        
        l2Bottom = BoxLayout(size_hint=(1, None), height=120)
        l2Bottom.add_widget(l3Left)
        l2Bottom.add_widget(l3Middle)
        l2Bottom.add_widget(l3Right)
        l2Bottom.add_widget(buttonQuit)

        l1Base = BoxLayout(orientation='vertical')
        l1Base.add_widget(self.widgetCardFront)
        l1Base.add_widget(self.widgetCardRear)
        l1Base.add_widget(l2Bottom)

        self.open()

        return l1Base


    def closeApplication(self):
        if (self.drone != None):
            self.drone.close()
        
        sys.exit(1)





if __name__ == '__main__':

    colorama.init()

    testApp = CardReader()

    testApp.run()

