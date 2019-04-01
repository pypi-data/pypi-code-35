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


class CardReaderAndList(App):

    def open(self):

        self.count      = 0

        #self.drone = Drone(True, True, True, True, True)
        self.drone = Drone()
        if self.drone.open() == False:
            print(Fore.RED + "* Error : Unable to open serial port." + Style.RESET_ALL)
            sys.exit(1)
        
        # 이벤트 핸들링 함수 등록
        self.drone.setEventHandler(DataType.RawCard, self.eventRawCard)
        self.drone.setEventHandler(DataType.RawCardList, self.eventRawCardList)

        # call my_callback every 0.5 seconds
        Clock.schedule_interval(self.my_callback, 0.2)


    # dt means delta-time
    def my_callback(self, dt):

        self.count = self.count + 1

        if (self.count & 0x01) == 0:
            self.drone.sendRequest(DeviceType.Drone, DataType.RawCard)
        else:
            self.drone.sendRequest(DeviceType.Drone, DataType.RawCardList)

        #self.drone.sendRequest(DeviceType.Drone, DataType.RawCardList)


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
            Rectangle(pos=(self.widgetCardFront.x, self.widgetCardFront.y), size=(self.widgetCardFront.width, self.widgetCardFront.height))

        with self.widgetCardRear.canvas:
            Color( float(rawCard.rgb[1][0]) / 255.0, float(rawCard.rgb[1][1]) / 255.0, float(rawCard.rgb[1][2]) / 255.0 )
            Rectangle(pos=(self.widgetCardRear.x, self.widgetCardRear.y), size=(self.widgetCardRear.width, self.widgetCardRear.height))


    def eventRawCardList(self, rawCardList):

        for i in range(0, 40):
            
            if      i == rawCardList.index and i == rawCardList.size:
                self.labelNumber[i].text = "[color=ffff33][b]" + "{0}".format(i) + "[/b][/color]"
            elif    i == rawCardList.index:
                self.labelNumber[i].text = "[color=ff3333][b]" + "{0}".format(i) + "[/b][/color]"
            elif    i == rawCardList.size:
                self.labelNumber[i].text = "[color=33ff33][b]" + "{0}".format(i) + "[/b][/color]"
            else:
                self.labelNumber[i].text = "[color=555555]" + "{0}".format(i) + "[/color]"

            self.widgetCardListTop[i].canvas.clear()
            self.widgetCardListBottom[i].canvas.clear()

            cardTop = (rawCardList.card[i][0] >> 4) & 0x0F
            cardBottom = (rawCardList.card[i][0]) & 0x0F
            colorTop = Color(0, 0, 0)
            colorBottom = Color(0, 0, 0)


            if   cardTop == 0x01:
                colorTop = Color(1, 0, 0)
            elif cardTop == 0x02:
                colorTop = Color(0, 1, 0)
            elif cardTop == 0x03:
                colorTop = Color(0, 0, 1)
            elif cardTop == 0x04:
                colorTop = Color(0, 1, 1)
            elif cardTop == 0x05:
                colorTop = Color(1, 0, 1)
            elif cardTop == 0x06:
                colorTop = Color(1, 1, 0)
            elif cardTop == 0x07:
                colorTop = Color(0, 0, 0)
            elif cardTop == 0x08:
                colorTop = Color(1, 1, 1)

            if   cardBottom == 0x01:
                colorBottom = Color(1, 0, 0)
            elif cardBottom == 0x02:
                colorBottom = Color(0, 1, 0)
            elif cardBottom == 0x03:
                colorBottom = Color(0, 0, 1)
            elif cardBottom == 0x04:
                colorBottom = Color(0, 1, 1)
            elif cardBottom == 0x05:
                colorBottom = Color(1, 0, 1)
            elif cardBottom == 0x06:
                colorBottom = Color(1, 1, 0)
            elif cardBottom == 0x07:
                colorBottom = Color(0, 0, 0)
            elif cardBottom == 0x08:
                colorBottom = Color(1, 1, 1)

            with self.widgetCardListTop[i].canvas:
                Color(colorTop.r, colorTop.g, colorTop.b)
                Rectangle(pos=(self.widgetCardListTop[i].x, self.widgetCardListTop[i].y), size=(self.widgetCardListTop[i].width, self.widgetCardListTop[i].height))

            with self.widgetCardListBottom[i].canvas:
                Color(colorBottom.r, colorBottom.g, colorBottom.b)
                Rectangle(pos=(self.widgetCardListTop[i].x, self.widgetCardListBottom[i].y), size=(self.widgetCardListTop[i].width, self.widgetCardListTop[i].height))


    def build(self):

        self.labelNumber = []
        self.widgetCardListTop = []
        self.widgetCardListBottom = []
        
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
        
        l2Top = BoxLayout(size_hint=(1, None), height=60)
        l3TopCardListArray = []
        for i in range(0, 40):
            self.labelNumber.append(Label(text='{0}'.format(i+1), markup=True))
            self.widgetCardListTop.append(Widget())
            self.widgetCardListBottom.append(Widget())
            l3TopCardListArray.append(BoxLayout(orientation='vertical'))
            l3TopCardListArray[i].add_widget(self.labelNumber[i])
            l3TopCardListArray[i].add_widget(self.widgetCardListTop[i])
            l3TopCardListArray[i].add_widget(self.widgetCardListBottom[i])
            l2Top.add_widget(l3TopCardListArray[i])

        l2Bottom = BoxLayout(size_hint=(1, None), height=120)
        l2Bottom.add_widget(l3Left)
        l2Bottom.add_widget(l3Middle)
        l2Bottom.add_widget(l3Right)
        l2Bottom.add_widget(buttonQuit)

        l1Base = BoxLayout(orientation='vertical')
        l1Base.add_widget(l2Top)
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

    testApp = CardReaderAndList()

    testApp.run()

