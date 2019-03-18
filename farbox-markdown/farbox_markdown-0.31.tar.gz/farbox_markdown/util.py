# coding: utf8
from __future__ import absolute_import
import os, sys, re


line_char = u'\uffff'
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY3:
    string_types = str
else:
    string_types = basestring



_COLOR_NAMES = ['ivory',
 'darkgreen',
 'lightcoral',
 'darkslategray',
 'blanchedalmond',
 'chocolate',
 'palevioletred',
 'black',
 'mediumpurple',
 'magenta',
 'mediumslateblue',
 'beige',
 'lightpink',
 'springgreen',
 'orchid',
 'lawngreen',
 'firebrick',
 'darkviolet',
 'lightskyblue',
 'aquamarine',
 'greenyellow',
 'whitesmoke',
 'midnightblue',
 'bisque',
 'darkmagenta',
 'darkslateblue',
 'sandybrown',
 'plum',
 'linen',
 'mediumorchid',
 'lightgreen',
 'goldenrod',
 'salmon',
 'aqua',
 'darkseagreen',
 'blueviolet',
 'peachpuff',
 'mediumvioletred',
 'moccasin',
 'thistle',
 'darkblue',
 'sienna',
 'mediumspringgreen',
 'paleturquoise',
 'darkgray',
 'violet',
 'cadetblue',
 'mediumturquoise',
 'orangered',
 'mediumaquamarine',
 'mintcream',
 'lightgoldenrodyellow',
 'lightslategray',
 'navy',
 'lightcyan',
 'mistyrose',
 'gray',
 'powderblue',
 'peru',
 'indigo',
 'steelblue',
 'blue',
 'lightsalmon',
 'lemonchiffon',
 'gainsboro',
 'hotpink',
 'darkturquoise',
 'lavender',
 'skyblue',
 'oldlace',
 'coral',
 'lightseagreen',
 'palegoldenrod',
 'green',
 'slateblue',
 'saddlebrown',
 'teal',
 'papayawhip',
 'limegreen',
 'dodgerblue',
 'lime',
 'white',
 'ghostwhite',
 'navajowhite',
 'darkkhaki',
 'indianred',
 'antiquewhite',
 'darkcyan',
 'deeppink',
 'darkorange',
 'lightsteelblue',
 'lightgray',
 'maroon',
 'slategray',
 'tan',
 'chartreuse',
 'lightyellow',
 'fuchsia',
 'azure',
 'gold',
 'tomato',
 'red',
 'royalblue',
 'cornsilk',
 'honeydew',
 'lightblue',
 'dimgray',
 'deepskyblue',
 'floralwhite',
 'mediumseagreen',
 'forestgreen',
 'yellowgreen',
 'cyan',
 'darkred',
 'khaki',
 'olivedrab',
 'rosybrown',
 'darkorchid',
 'burlywood',
 'darkgoldenrod',
 'lavenderblush',
 'cornflowerblue',
 'seashell',
 'palegreen',
 'pink',
 'brown',
 'yellow',
 'seagreen',
 'orange',
 'mediumblue',
 'darkolivegreen',
 'snow',
 'purple',
 'darksalmon',
 'aliceblue',
 'crimson',
 'olive',
 'wheat',
 'turquoise',
 'silver']

COLOR_NAMES = set(_COLOR_NAMES)


FONT_FAMILY_MAP = {
    u'华文细黑':'STXihei',
    u'华文黑体':'STHeiti',
    u'华文楷体':'STKaiti',
    u'华文宋体':'STSong',
    u'华文仿宋':'STFangsong',
    u'冬青黑体': 'Hiragino Sans GB',
    u'宋刻本秀': 'FZSongKeBenXiuKsiS-R-GB',
    u'儷黑':'LiHei Pro',
    u'丽黑':'LiHei Pro',
    u'儷宋':'LiSong Pro',
    u'丽宋':'LiSong Pro',
    u'標楷體':'BiauKai',
    u'标楷体':'BiauKai',
    u'兰亭黑': 'Lantinghei SC',
    u'隶变': 'Libian SC, Libian TC',
    u'报隶': 'Baoli SC, Baoli TC',
    u'翩翩体': 'HanziPen SC, HanziPen TC',
    u'娃娃体': 'Wawati, Wawati SC, Wawati TC',
    u'蘋果儷中黑':'Apple LiGothic Medium',
    u'苹果丽中黑':'Apple LiGothic Medium',
    u'蘋果儷細宋':'Apple LiSung Light',
    u'苹果丽细宋':'Apple LiSung Light',
    u'新細明體':'PMingLiU',
    u'新細明体':'PMingLiU',
    u'細明體':'MingLiU',
    u'細明体':'MingLiU',
    u'黑体':'SimHei, Heiti SC, Heiti TC',
    u'宋体':'Songti, SimSun, Songti SC, Songti TC',
    u'新宋体':'NSimSun',
    u'仿宋':'FangSong',
    u'楷体':'KaiTi, Kaiti SC, Kaiti TC',
    u'微軟正黑體':'Microsoft JhengHei',
    u'微軟正黑体':'Microsoft JhengHei',
    u'微软雅黑体':'Microsoft YaHei',
    u'隶书':'LiSu, Libian SC, Libian TC',
    u'幼圆':'YouYuan',
    u'华文中宋':'STZhongsong',
    u'方正舒体':'FZShuTi',
    u'方正姚体':'FZYaoti',
    u'华文彩云':'STCaiyun',
    u'华文琥珀':'STHupo',
    u'华文隶书':'STLiti',
    u'华文行楷':'STXingkai',
    u'华文新魏': 'STXinwei',
}


MARKDOWN_EXTS = ['.txt', '.md', '.markdown', '.mk']

def is_a_markdown_file(path):
    if not path:
        return False
    ext = os.path.splitext(path)[1].lower()
    return ext in MARKDOWN_EXTS




def is_color_value(value):
    if value in COLOR_NAMES or (value.startswith('#') and len(value)<=7) \
                or value.startswith('rgb(') or value.startswith('rgba('):
        return True
    else:
        return False


def smart_tag_style_for_block_html(block_html):
    # md_line & header, image 支持
    # [center, red, 17px, 120%]
    plain_text = re.sub(r'<[^<>]*>', '', block_html).replace(line_char, '') # line_char 可能存在的问题
    plain_text = plain_text.strip('\n').lstrip()
    tag_s = re.search(r'\[[^\^\[\]]+\]$', plain_text)
    if not tag_s:
        return block_html # ignore

    raw_tag_marker = tag_s.group()
    if '/' in raw_tag_marker: # / 是不允许出现的字符
        return block_html

    raw_tag = raw_tag_marker.strip('[]').strip().lower().replace(u'，', ',') # 全小写处理

    if ' ' in raw_tag and ',' not in raw_tag:
        # 没有 , 的情况下, 可以用空格进行对应
        raw_tag_list = raw_tag.split(' ')
    else:
        raw_tag_list = raw_tag.split(',')

    style_list = []
    font_family_tried = False
    for tag in raw_tag_list:
        tag = tag.strip()
        if tag in ['middle']:
            tag = 'center'
        # style_type = None
        if is_color_value(tag):
            # style_type = 'color'
            style_list.append('color:%s'%tag)
        elif tag.startswith('@') and is_color_value(tag[1:]):
            # @xxxx 是作为背景色
            style_list.append('background-color:%s'%tag[1:])
        elif tag.endswith('%'): # zoom
            # style_type = 'zoom'
            style_list.append('zoom:%s'%tag)
        elif re.match('\d+\.\d+$', tag):
            # 浮点, 认为是 line-height
            style_list.append('line-height:%s'%tag)
        elif re.match('\d+(px|pt|em)?$', tag, re.I): # 整数 font_size
            # style_type = 'font_size'
            if re.match(r'\d+$', tag):
                tag += 'px' # 自动补全 px 如果只是整数的话
            style_list.append('font-size:%s'%tag)
        elif tag in ['center', 'left', 'right']:
            # alignment
            style_list.append('text-align:%s'%tag)
            if tag != 'left':
                # 居中、居右的 text-indent 是没有意义的
                style_list.append('text-indent:0')
        elif tag and not font_family_tried:
            # as font-family, 但是 font family 仅仅尝试一次, 这样可以过滤掉一些无效值
            font_family = FONT_FAMILY_MAP.get(tag) or tag
            style_list.append('font-family:%s'%font_family)
            font_family_tried = True
        elif tag:
            # 只有有一个规则是不匹配的, 就直接return block_html
            return block_html

    raw_css_style = (';'.join(style_list)).replace("'", "\'")
    if raw_css_style:
        css_style = "style='%s'" % raw_css_style
        css_style = css_style.replace('\\g', '') # 以防被注入
        block_html = ''.join(block_html.rsplit(raw_tag_marker, 1)) # 先去掉原始声明的部分
        block_html = re.sub(r'^(\s*<[a-z0-9]+)( |>)', '\g<1> %s \g<2>'%css_style, block_html, flags=re.I)

    return block_html # at last






