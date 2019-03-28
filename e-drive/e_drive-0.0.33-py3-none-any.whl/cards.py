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


class CardsReaderGUI(App):

    def open(self):

        self.drone = Drone(True, True, True, True, True)
        #self.drone = Drone()
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

        '''
        self.labelFront.text = (
            "{0:5}".format(rawCard.rgbRaw[0][0]) +
            "{0:5}".format(rawCard.rgbRaw[0][1]) +
            "{0:5}".format(rawCard.rgbRaw[0][2]) +
            "{0:5}".format(rawCard.rgbRaw[1][0]) +
            "{0:5}".format(rawCard.rgbRaw[1][1]) +
            "{0:5}".format(rawCard.rgbRaw[1][2]) +
            "{0:4}".format(rawCard.rgb[0][0]) +
            "{0:4}".format(rawCard.rgb[0][1]) +
            "{0:4}".format(rawCard.rgb[0][2]) +
            "{0:4}".format(rawCard.rgb[1][0]) +
            "{0:4}".format(rawCard.rgb[1][1]) +
            "{0:4}".format(rawCard.rgb[1][2]) +
            "{0:4}".format(rawCard.hsv[0][0]) +
            "{0:4}".format(rawCard.hsv[0][1]) +
            "{0:4}".format(rawCard.hsv[0][2]) +
            "{0:4}".format(rawCard.hsv[1][0]) +
            "{0:4}".format(rawCard.hsv[1][1]) +
            "{0:4} ".format(rawCard.hsv[1][2]) +
            "{0:14}".format(rawCard.color[0].name) +
            "{0:14}".format(rawCard.color[1].name))
        '''
        self.labelFront.text = (
            "{0:0.2}, ".format(float(rawCard.rgb[0][0]) / 255.0) + 
            "{0:0.2}, ".format(float(rawCard.rgb[0][1]) / 255.0) + 
            "{0:0.2}\n".format(float(rawCard.rgb[0][2]) / 255.0) +
            "{0:0.2}, ".format(float(rawCard.hsv[0][0]) / 255.0) + 
            "{0:0.2}, ".format(float(rawCard.hsv[0][1]) / 255.0) + 
            "{0:0.2}\n".format(float(rawCard.hsv[0][2]) / 255.0) +
            rawCard.color[0].name)

        self.labelRear.text = (
            "{0:0.2}, ".format(float(rawCard.rgb[1][0]) / 255.0) + 
            "{0:0.2}, ".format(float(rawCard.rgb[1][1]) / 255.0) + 
            "{0:0.2}\n".format(float(rawCard.rgb[1][2]) / 255.0) +
            "{0:0.2}, ".format(float(rawCard.hsv[1][0]) / 255.0) + 
            "{0:0.2}, ".format(float(rawCard.hsv[1][1]) / 255.0) + 
            "{0:0.2}\n".format(float(rawCard.hsv[1][2]) / 255.0) + 
            rawCard.color[1].name)

        self.widgetFront.canvas.clear()
        self.widgetRear.canvas.clear()

        with self.widgetFront.canvas:
            Color( float(rawCard.rgb[0][0]) / 255.0, float(rawCard.rgb[0][1]) / 255.0, float(rawCard.rgb[0][2]) / 255.0 )
            Rectangle(pos=(0, 120 + self.widgetRear.height), size=(self.widgetFront.width, self.widgetFront.height))

        with self.widgetRear.canvas:
            Color( float(rawCard.rgb[1][0]) / 255.0, float(rawCard.rgb[1][1]) / 255.0, float(rawCard.rgb[1][2]) / 255.0 )
            Rectangle(pos=(0, 120), size=(self.widgetRear.width, self.widgetRear.height))


    def build(self):
        self.widgetFront = Widget()
        self.widgetRear = Widget()
        self.labelFront = Label(text='0')
        self.labelRear = Label(text='0')

        self.btn_quit = Button(text='Quit', on_press=partial(self.closeApplication))

        self.layoutBottom = BoxLayout(size_hint=(1, None), height=120)
        self.layoutBottom.add_widget(self.labelFront)
        self.layoutBottom.add_widget(self.labelRear)
        self.layoutBottom.add_widget(self.btn_quit)

        self.root = BoxLayout(orientation='vertical')
        self.root.add_widget(self.widgetFront)
        self.root.add_widget(self.widgetRear)
        self.root.add_widget(self.layoutBottom)

        self.open()

        return self.root

    def closeApplication(self):
        if (self.drone != None):
            self.drone.close()
        
        sys.exit(1)


if __name__ == '__main__':

    colorama.init()

    cardsReaderGUI = CardsReaderGUI()

    cardsReaderGUI.run()

