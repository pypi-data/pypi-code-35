from distutils.core import setup

#从python的发布工具导入setup函数



setup(

    name = 'ColorFont',

    version = '1.0.5',

    #关联模块

    py_modules = ['ColorFont'],

    author = 'galaxy',

    author_email = 'galaxy_2018@126.com',

    url = 'https://github.com/galaxy080123/ColorFont/tree/1.0.0',

    description = '''
控制台打印彩色字体
    
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

)