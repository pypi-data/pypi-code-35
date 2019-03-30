#-*- coding:utf-8 -*-#

#filename: prt_cmd_color.py

import ctypes,sys
 
STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12
 
#字体颜色定义 text colors
FOREGROUND_BLUE = 0x09 # blue.
FOREGROUND_GREEN = 0x0a # green.
FOREGROUND_RED = 0x0c # red.
FOREGROUND_YELLOW = 0x0e # yellow.
 
# 背景颜色定义 background colors
BACKGROUND_YELLOW = 0xe0 # yellow.

'''
0 = 黑色       8 = 灰色
1 = 蓝色       9 = 淡蓝色
2 = 绿色       A = 淡绿色
3 = 浅绿色     B = 淡浅绿色
4 = 红色       C = 淡红色
5 = 紫色       D = 淡紫色
6 = 黄色       E = 淡黄色
7 = 白色       F = 亮白色
格式：
0x12
高位代表背景色，低位代表字体颜色

0x10 | 0x02
0x10代表背景色，0x02代表字体颜色

使用方法：
import ColorFont
ColorFont.Color.printColoredText('hello', 0x02, 0x10, '\n')
'''
 
# get handle
std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

class Color:
    def set_cmd_text_color(color, handle=std_out_handle):
        Bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
        return Bool
 
    #reset white
    def resetColor():
        Color.set_cmd_text_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)
 
    #green
    def printGreen(mess):
        Color.set_cmd_text_color(FOREGROUND_GREEN)
        sys.stdout.write(mess + '\n')
        Color.resetColor()

    #red
    def printRed(mess):
        Color.set_cmd_text_color(FOREGROUND_RED)
        sys.stdout.write(mess + '\n')
        Color.resetColor()
  
    #yellow
    def printYellow(mess):
        Color.set_cmd_text_color(FOREGROUND_YELLOW)
        sys.stdout.write(mess + '\n')
        Color.resetColor()

    #white bkground and black text
    def printYellowRed(mess):
        Color.set_cmd_text_color(BACKGROUND_YELLOW | FOREGROUND_RED)
        sys.stdout.write(mess + '\n')
        Color.resetColor()

    def printColoredText(text,foregroundcolor=(0x0f),backgroundcolor=(0x00),end='\n'):
        Color.set_cmd_text_color(foregroundcolor | backgroundcolor)
        sys.stdout.write(text + end)
        Color.resetColor()


if __name__ == '__main__':
    Color.printGreen('printGreen:Gree Color Text')
    Color.printRed('printRed:Red Color Text')
    Color.printYellow('printYellow:Yellow Color Text')
    Color.printColoredText('hello',0x08,0x90)
    Color.printYellowRed('hi')