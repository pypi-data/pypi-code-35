from PyQt5 .QtCore import *#line:1
from PyQt5 .QtGui import *#line:2
from PyQt5 .QtWidgets import *#line:3
import sys #line:4
import json #line:5
import requests #line:6
Name =0 #line:7
posite_y =35 #line:8
left_imgs =""#line:9
right_imgs =""#line:10
app =""#line:11
class PyQt5_QDialog (QDialog ):#line:12
    def __init__ (O00O0O000O00O0O00 ):#line:13
        super ().__init__ ()#line:14
        O00O0O000O00O0O00 .setObjectName ("dialog")#line:15
    def setBackgroundColor (OO000O00OO0OOOOO0 ,OOO00O00O0OOO00OO ):#line:16
        OO000O00OO0OOOOO0 .setStyleSheet ("#dialog{background-color:"+OOO00O00O0OOO00OO +"}")#line:17
    def setBackground (O000000O0OO0O0OOO ,O0O0000O0O00O00O0 ):#line:18
        O000000O0OO0O0OOO .setStyleSheet ("#dialog{border-image:url("+O0O0000O0O00O00O0 +")}")#line:19
    def setResize (O0O00O00O00OOO000 ,O000OOO00O000OOOO ,OO00O000O000000O0 ):#line:20
        O0O00O00O00OOO000 .resize (O000OOO00O000OOOO ,OO00O000O000000O0 )#line:21
class PyQt5_Qlabel (QLabel ):#line:22
    clicked =pyqtSignal (QMouseEvent )#line:23
    def __init__ (O0000OO0000O0O0OO ,OO000OO0000O000O0 ,x =0 ,y =0 ,width =60 ,height =16 ):#line:24
        super ().__init__ (OO000OO0000O000O0 )#line:25
        O0000OO0000O0O0OO .widget =OO000OO0000O000O0 #line:26
        O0000OO0000O0O0OO .zeze =True #line:27
        O0000OO0000O0O0OO .menu =QMenu (O0000OO0000O0O0OO )#line:28
        O0000OO0000O0O0OO .customContextMenuRequested ['QPoint'].connect (lambda :O0000OO0000O0O0OO .menu .exec_ (QCursor .pos ()))#line:29
        O0000OO0000O0O0OO .setGeometry (x ,y ,width ,height )#line:30
    def setFontSize (O0O0O0000OO0OO00O ,OOO0O00OO000OO0O0 ):#line:31
        O0OOOOOO00000O0O0 =QFont ()#line:32
        O0OOOOOO00000O0O0 .setPixelSize (OOO0O00OO000OO0O0 )#line:33
        O0O0O0000OO0OO00O .setFont (O0OOOOOO00000O0O0 )#line:34
    def setFontFitSize (OOO00000O0OOOO0OO ,O0OOO00O000000O0O ):#line:35
        O0000OO000OOO0O00 =QFont ()#line:36
        O0000OO000OOO0O00 .setPointSize (O0OOO00O000000O0O )#line:37
        OOO00000O0OOOO0OO .setFont (O0000OO000OOO0O00 )#line:38
    def setBackground (O000O0O0OOO0O0OO0 ,O0OOOOO00OO000OOO ):#line:39
        O000O0O0OOO0O0OO0 .setStyleSheet (O000O0O0OOO0O0OO0 .styleSheet ()+"border-image:url("+O0OOOOO00OO000OOO +");")#line:40
    def setBackgroundColor (O0OOO0OO00O0OO000 ,O00O0O0O000O0OOOO ):#line:41
        O0OOO0OO00O0OO000 .setStyleSheet (O0OOO0OO00O0OO000 .styleSheet ()+"background-color:"+O00O0O0O000O0OOOO +";")#line:42
    def setTextColor (OO00OOO0OO0OO0OOO ,O0O000OOOOO0OOOOO ):#line:43
        OO00OOO0OO0OO0OOO .setStyleSheet (OO00OOO0OO0OO0OOO .styleSheet ()+"color:"+O0O000OOOOO0OOOOO +";")#line:44
    def mouseReleaseEvent (OOO0OOO0OO0OO00OO ,O0OOOO0OO0OOO0O0O ):#line:45
        OOO0OOO0OO0OO00OO .released .emit (O0OOOO0OO0OOO0O0O )#line:46
    released =pyqtSignal (QMouseEvent )#line:47
    pressed =pyqtSignal (QEvent )#line:48
    def mousePressEvent (O00O0O0O000O00OO0 ,OOO00000000O0O0O0 ):#line:49
        O00O0O0O000O00OO0 .pressed .emit (OOO00000000O0O0O0 )#line:50
        if OOO00000000O0O0O0 .buttons ()==Qt .LeftButton :#line:51
            O00O0O0O000O00OO0 .clicked .emit (OOO00000000O0O0O0 )#line:52
    moved =pyqtSignal (QMouseEvent )#line:53
    def mouseMoveEvent (OOO0O0000O000OOO0 ,OO00OOOO00O0O00OO ):#line:54
        OOO0O0000O000OOO0 .moved .emit (OO00OOOO00O0O00OO )#line:55
    doubleclicked =pyqtSignal (QMouseEvent )#line:56
    def mouseDoubleClickEvent (OOO0O0O0O00O00OOO ,O00OOO000O0O00000 ):#line:57
        if O00OOO000O0O00000 .buttons ()==Qt .LeftButton :#line:58
            OOO0O0O0O00O00OOO .doubleclicked .emit (O00OOO000O0O00000 )#line:59
    entered =pyqtSignal (QEnterEvent )#line:60
    def enterEvent (OO0O0OOO000O0O0OO ,OO0O0O0OOOOOO0000 ):#line:61
        OO0O0OOO000O0O0OO .entered .emit (OO0O0O0OOOOOO0000 )#line:62
    leaved =pyqtSignal (QEvent )#line:63
    def leaveEvent (OO0OO0O0OO00O00O0 ,OO0OOOOOOO0O0O000 ):#line:64
        OO0OO0O0OO00O00O0 .leaved .emit (OO0OOOOOOO0O0O000 )#line:65
    def addScorell (O00O00OO0OO00OO0O ,O00000OO0O0O00O0O ,O0O000O00000OOOO0 ,OO000OO0O0O00OOOO ,OO0OOOO0OO0000OO0 ):#line:66
        OO000OO0O0O00OOOO =O00O00OO0OO00OO0O .parent ().width ()+200 #line:67
        O00O00OO0OO00OO0O .a =PyQt5_QGroupBox (O00O00OO0OO00OO0O .parent (),O00000OO0O0O00O0O ,O0O000O00000OOOO0 ,OO000OO0O0O00OOOO ,OO0OOOO0OO0000OO0 )#line:68
        O00O00OO0OO00OO0O .a .setBorderWidth (0 )#line:69
        O00O00OO0OO00OO0O .scroll =QScrollArea ()#line:70
        O00O00OO0OO00OO0O .scroll .setWidget (O00O00OO0OO00OO0O )#line:71
        O00O00OO0OO00OO0O .scroll .setStyleSheet ("background-color:rgba(0,0,0,0)")#line:72
        O00O00OO0OO00OO0O .vbox =QVBoxLayout ()#line:73
        O00O00OO0OO00OO0O .vbox .setContentsMargins (0 ,0 ,0 ,0 )#line:74
        O00O00OO0OO00OO0O .vbox .addWidget (O00O00OO0OO00OO0O .scroll )#line:75
        O00O00OO0OO00OO0O .a .setLayout (O00O00OO0OO00OO0O .vbox )#line:76
    def setSize (O00OOO00OO0OOOOOO ,OOOO0OOO00OOO0O00 ):#line:77
        O00OOO00OO0OOOOOO .setFixedSize (OOOO0OOO00OOO0O00 )#line:78
    def refresh (O0OO0OO0O00000O0O ):#line:79
        if O0OO0OO0O00000O0O .zeze :#line:80
            O0OO0OO0O00000O0O .widget .resize (O0OO0OO0O00000O0O .widget .width ()+1 ,O0OO0OO0O00000O0O .widget .height ()+1 )#line:81
            O0OO0OO0O00000O0O .zeze =False #line:82
        else :#line:83
            O0OO0OO0O00000O0O .widget .resize (O0OO0OO0O00000O0O .widget .width ()-1 ,O0OO0OO0O00000O0O .widget .height ()-1 )#line:84
            O0OO0OO0O00000O0O .zeze =True #line:85
    def addRightMenu (O0000OO0OOO000O0O ,O000O00000O0OOOO0 ):#line:86
        O0000OO0OOO000O0O .setContextMenuPolicy (Qt .CustomContextMenu )#line:87
        O0000OO0OOO000O0O .menuAction =QAction (O000O00000O0OOOO0 ,O0000OO0OOO000O0O )#line:88
        O0000OO0OOO000O0O .menu .addAction (O0000OO0OOO000O0O .menuAction )#line:89
        return O0000OO0OOO000O0O .menuAction #line:90
class PyQt5_QGroupBox (QGroupBox ):#line:91
    def __init__ (O00O000OOOO000OOO ,O0O00OO0OO00OO00O ,x =0 ,y =0 ,width =120 ,height =80 ):#line:92
        super ().__init__ (O0O00OO0OO00OO00O )#line:93
        O00O000OOOO000OOO .setGeometry (x ,y ,width ,height )#line:94
        O00O000OOOO000OOO .setObjectName ("groupbox")#line:95
    def setBackground (O00O0OOO0O0O000O0 ,OOOO0O00000OO0OOO ):#line:96
        O00O0OOO0O0O000O0 .setStyleSheet ("#groupbox{border-image:url("+OOOO0O00000OO0OOO +")}")#line:97
    def setBackgroundColor (O0OO000O0O00OOO0O ,O00O0OOO0OO00000O ):#line:98
        O0OO000O0O00OOO0O .setStyleSheet ("#groupbox{background-color:"+O00O0OOO0OO00000O +"}")#line:99
    def setBorderWidth (O0O0OOO00OOO0OO0O ,OOOO0OO0OOOO00OO0 ):#line:100
        O0O0OOO00OOO0OO0O .setStyleSheet (O0O0OOO00OOO0OO0O .styleSheet ()+"border-width:"+str (OOOO0OO0OOOO00OO0 )+"px;border-style:solid;")#line:101
def SentContent (O00OOOOO0O00000O0 ):#line:102
    OO00O00O0OOOOOO0O =json .dumps ({"reqType":0 ,"perception":{"inputText":{"text":O00OOOOO0O00000O0 }},"userInfo":{"apiKey":"95032be1a13c40a981bd250fd4515f12","userId":"f7a65bc37f2a373d"}})#line:103
    return OO00O00O0OOOOOO0O #line:104
class UI_Name (PyQt5_QDialog ):#line:105
    def addTitle (O0OO00O0O00OO000O ,OO0O00000OOO0O0OO ):#line:106
        O0OO00O0O00OO000O .setWindowTitle (OO0O00000OOO0O0OO )#line:107
    def setBg (O0OOOO000O00OOO0O ,O000OOO0OO0OO0000 ):#line:108
        O0OOOO000O00OOO0O .setBackground (O000OOO0OO0OO0000 )#line:109
    def addText (OO00O00O0O000OOO0 ):#line:110
        OO00O00O0O000OOO0 .AllLabel =PyQt5_Qlabel (OO00O00O0O000OOO0 ,0 ,0 ,400 ,20000 )#line:111
        OO00O00O0O000OOO0 .AllLabel .addScorell (0 ,0 ,0 ,600 )#line:112
        OO00O00O0O000OOO0 .sent_edit ()#line:113
    def eventFilter (OO0000OOOOO000OO0 ,O00000O00O0O000OO ,OO000OOOOO0OOOOOO ):#line:114
        if O00000O00O0O000OO ==OO0000OOOOO000OO0 .effe :#line:115
            if OO000OOOOO0OOOOOO .type ()==QEvent .KeyPress and (str (OO000OOOOO0OOOOOO .key ())=="16777220"):#line:116
                if QApplication .keyboardModifiers ()==Qt .ShiftModifier :#line:117
                    if OO0000OOOOO000OO0 .effe .toPlainText ()!="":#line:118
                        global Name ,posite_y #line:119
                        O0O0O0O000OOOO00O =str (Name +1 )#line:120
                        OO0000OOOOO000OO0 .creat_me (O0O0O0O000OOOO00O ,posite_y )#line:121
                        OO0000OOOOO000OO0 .creat_message_me (O0O0O0O000OOOO00O ,(posite_y -5 ),OO0000OOOOO000OO0 .effe .toPlainText ())#line:122
                        OO0000OOOOO000OO0 .creat_robot (O0O0O0O000OOOO00O ,posite_y +85 )#line:123
                        OOOO000OOO0OOO0O0 =OO0000OOOOO000OO0 .chat_Robat (OO0000OOOOO000OO0 .effe .toPlainText ())#line:124
                        OO0000OOOOO000OO0 .creat_message_robot (O0O0O0O000OOOO00O ,(posite_y +80 ),OOOO000OOO0OOO0O0 )#line:125
                        posite_y +=170 #line:126
                        OO0000OOOOO000OO0 .effe .setPlainText ("")#line:127
                        OO0000OOOOO000OO0 .effe .setVisible (False )#line:128
                        OO0000OOOOO000OO0 .effe .setVisible (True )#line:129
                        return True #line:130
        return QDialog .eventFilter (OO0000OOOOO000OO0 ,O00000O00O0O000OO ,OO000OOOOO0OOOOOO )#line:131
    def left_img (OO00000000OOO0OO0 ,O0OOOOOOO0OO0000O ):#line:132
        global left_imgs #line:133
        left_imgs =O0OOOOOOO0OO0000O #line:134
    def right_img (OO000000000OOO000 ,OO00O00O00O00O000 ):#line:135
        global right_imgs #line:136
        right_imgs =OO00O00O00O00O000 #line:137
    def creat_robot (O0OO00OOOOO0OO0OO ,OO0OO0OO0O0OO0OO0 ,O000OOO000OO0OO0O ):#line:138
        OO0OO0OO0O0OO0OO0 ="name"+OO0OO0OO0O0OO0OO0 #line:139
        O0OO00OOOOO0OO0OO .name =PyQt5_Qlabel (O0OO00OOOOO0OO0OO .AllLabel ,20 ,O000OOO000OO0OO0O ,50 ,50 )#line:140
        O0OO00OOOOO0OO0OO .name .setBackground (left_imgs )#line:141
        O0OO00OOOOO0OO0OO .name .show ()#line:142
    def creat_me (O0OOO0OO0OO0OO0O0 ,O000OO00OOOOOOO0O ,O0OO00OOO0OOOO0O0 ):#line:143
        OO0OO0OO00O0O0OOO ="me"+O000OO00OOOOOOO0O #line:144
        O0OOO0OO0OO0OO0O0 .me =PyQt5_Qlabel (O0OOO0OO0OO0OO0O0 .AllLabel ,330 ,O0OO00OOO0OOOO0O0 ,40 ,40 )#line:145
        O0OOO0OO0OO0OO0O0 .me .setBackground (right_imgs )#line:146
        O0OOO0OO0OO0OO0O0 .me .show ()#line:147
    def creat_message_robot (OOO0OO0O0OO0OOOOO ,OO0OOO0O0O0O000O0 ,OOO000O0O00OOO00O ,OO0O00O0O0OOO000O ):#line:148
        OO00O0000O0O000O0 ="Group_robot"+OO0OOO0O0O0O000O0 #line:149
        O00O0OOO0O0OO000O ="robot_message"+OO0OOO0O0O0O000O0 #line:150
        OOO0OO0O0OO0OOOOO .Group =PyQt5_QGroupBox (OOO0OO0O0OO0OOOOO .AllLabel ,70 ,OOO000O0O00OOO00O ,230 ,55 )#line:151
        OOO0OO0O0OO0OOOOO .Group .show ()#line:152
        OOO0OO0O0OO0OOOOO .Label_bg =PyQt5_Qlabel (OOO0OO0O0OO0OOOOO .Group ,0 ,0 ,230 ,55 )#line:153
        OOO0OO0O0OO0OOOOO .Label_bg .setBackground ("img/message1.png")#line:154
        OOO0OO0O0OO0OOOOO .Label_bg .show ()#line:155
        OOO0OO0O0OO0OOOOO .robot_message =PyQt5_Qlabel (OOO0OO0O0OO0OOOOO .Group ,20 ,5 ,200 ,2000 )#line:156
        OOO0OO0O0OO0OOOOO .robot_message .setFont (QFont ("手札体-简",14 ,QFont .Bold ))#line:157
        OOO0OO0O0OO0OOOOO .robot_message .setWordWrap (True )#line:158
        OOO0OO0O0OO0OOOOO .robot_message .setText (OO0O00O0O0OOO000O )#line:159
        OOO0OO0O0OO0OOOOO .a =PyQt5_QGroupBox (OOO0OO0O0OO0OOOOO .robot_message .parent (),20 ,5 ,600 ,43 )#line:160
        OOO0OO0O0OO0OOOOO .a .setBorderWidth (0 )#line:161
        OOO0OO0O0OO0OOOOO .scroll =QScrollArea ()#line:162
        OOO0OO0O0OO0OOOOO .a .show ()#line:163
        OOO0OO0O0OO0OOOOO .scroll .setWidget (OOO0OO0O0OO0OOOOO .robot_message )#line:164
        OOO0OO0O0OO0OOOOO .scroll .setStyleSheet ("background-color:rgba(0,0,0,0)")#line:165
        OOO0OO0O0OO0OOOOO .scroll .show ()#line:166
        OOO0OO0O0OO0OOOOO .vbox =QVBoxLayout ()#line:167
        OOO0OO0O0OO0OOOOO .vbox .setContentsMargins (0 ,0 ,0 ,0 )#line:168
        OOO0OO0O0OO0OOOOO .vbox .addWidget (OOO0OO0O0OO0OOOOO .scroll )#line:169
        OOO0OO0O0OO0OOOOO .a .setLayout (OOO0OO0O0OO0OOOOO .vbox )#line:170
        OOO0OO0O0OO0OOOOO .robot_message .setAlignment (Qt .AlignTop )#line:171
        OOO0OO0O0OO0OOOOO .robot_message .show ()#line:172
    def creat_message_me (O0000OOOO00000OOO ,OO00OO0O000OOOOO0 ,O0OOOOOOO0OOO0000 ,O0OO0O0O000O0O00O ):#line:173
        OOO0OOO0O0O0000O0 ="Group_me"+OO00OO0O000OOOOO0 #line:174
        O00O0O0O0OO00OO0O ="me_message"+OO00OO0O000OOOOO0 #line:175
        O0000OOOO00000OOO .Group =PyQt5_QGroupBox (O0000OOOO00000OOO .AllLabel ,90 ,O0OOOOOOO0OOO0000 ,230 ,55 )#line:176
        O0000OOOO00000OOO .Group .show ()#line:177
        O0000OOOO00000OOO .Label_bg =PyQt5_Qlabel (O0000OOOO00000OOO .Group ,0 ,0 ,230 ,55 )#line:178
        O0000OOOO00000OOO .Label_bg .setBackground ("img/message2.png")#line:179
        O0000OOOO00000OOO .Label_bg .show ()#line:180
        O0000OOOO00000OOO .me_message =PyQt5_Qlabel (O0000OOOO00000OOO .Group ,10 ,5 ,200 ,2000 )#line:181
        O0000OOOO00000OOO .me_message .setFont (QFont ("手札体-简",14 ,QFont .Bold ))#line:182
        O0000OOOO00000OOO .me_message .setWordWrap (True )#line:183
        O0000OOOO00000OOO .me_message .setText (O0OO0O0O000O0O00O )#line:184
        O0000OOOO00000OOO .a =PyQt5_QGroupBox (O0000OOOO00000OOO .me_message .parent (),10 ,5 ,600 ,43 )#line:185
        O0000OOOO00000OOO .a .setBorderWidth (0 )#line:186
        O0000OOOO00000OOO .scroll =QScrollArea ()#line:187
        O0000OOOO00000OOO .a .show ()#line:188
        O0000OOOO00000OOO .scroll .setWidget (O0000OOOO00000OOO .me_message )#line:189
        O0000OOOO00000OOO .scroll .setStyleSheet ("background-color:rgba(0,0,0,0)")#line:190
        O0000OOOO00000OOO .scroll .show ()#line:191
        O0000OOOO00000OOO .vbox =QVBoxLayout ()#line:192
        O0000OOOO00000OOO .vbox .setContentsMargins (0 ,0 ,0 ,0 )#line:193
        O0000OOOO00000OOO .vbox .addWidget (O0000OOOO00000OOO .scroll )#line:194
        O0000OOOO00000OOO .a .setLayout (O0000OOOO00000OOO .vbox )#line:195
        O0000OOOO00000OOO .me_message .setAlignment (Qt .AlignTop )#line:196
        O0000OOOO00000OOO .me_message .show ()#line:197
    def sent_edit (OOOOOO0OO0O0O00O0 ):#line:198
        OOOOOO0OO0O0O00O0 .labg =PyQt5_QGroupBox (OOOOOO0OO0O0O00O0 ,0 ,560 ,415 ,40 )#line:199
        OOOOOO0OO0O0O00O0 .labg .setBackground ("img/chat_bgg.png")#line:200
        OOOOOO0OO0O0O00O0 .label1 =PyQt5_Qlabel (OOOOOO0OO0O0O00O0 .labg ,300 ,10 ,20 ,20 )#line:201
        OOOOOO0OO0O0O00O0 .label1 .setBackground ("img/shift.png")#line:202
        OOOOOO0OO0O0O00O0 .label2 =PyQt5_Qlabel (OOOOOO0OO0O0O00O0 .labg ,320 ,10 ,15 ,15 )#line:203
        OOOOOO0OO0O0O00O0 .label2 .setBackground ("img/add_add.png")#line:204
        OOOOOO0OO0O0O00O0 .label3 =PyQt5_Qlabel (OOOOOO0OO0O0O00O0 .labg ,337 ,10 ,20 ,20 )#line:205
        OOOOOO0OO0O0O00O0 .label3 .setBackground ("img/enter.png")#line:206
        OOOOOO0OO0O0O00O0 .effe =QTextEdit (OOOOOO0OO0O0O00O0 .labg )#line:207
        OOOOOO0OO0O0O00O0 .effe .setGeometry (QRect (0 ,0 ,415 ,40 ))#line:208
        OOOOOO0OO0O0O00O0 .effe .setStyleSheet ("background-color:rgba(0,0,0,0)")#line:209
        OOOOOO0OO0O0O00O0 .effe .setFont (QFont ("手札体-简",15 ,QFont .Bold ))#line:210
        OOOOOO0OO0O0O00O0 .effe .installEventFilter (OOOOOO0OO0O0O00O0 )#line:211
    def chat_Robat (O0OO0OO0OO00O0O0O ,O00OOOOOOO0OOO0OO ):#line:212
        OO00O000O000O0OOO =SentContent (O00OOOOOOO0OOO0OO )#line:213
        O00OOOO0O00O0OO0O ='http://openapi.tuling123.com/openapi/api/v2'#line:214
        O00O0O0OO0OOOO000 =requests .post (O00OOOO0O00O0OO0O ,data =OO00O000O000O0OOO )#line:215
        OO00O0OO0OO0O0OOO =json .loads (O00O0O0OO0OOOO000 .text )#line:216
        OO00O0OO0OO0O0OOO =OO00O0OO0OO0O0OOO ['results'][0 ]['values']#line:217
        if 'text'in OO00O0OO0OO0O0OOO :#line:218
            return OO00O0OO0OO0O0OOO ["text"]#line:219
        else :#line:220
            return "我不知道啊，你问的问题太难了！"#line:221
    def end_dialog (O0O00OO0OOOO0O00O ):#line:222
        O0O00OO0OOOO0O00O .setFixedSize (400 ,600 )#line:223
        O0O00OO0OOOO0O00O .show ()#line:224
        app .exec_ ()#line:225
def creat_dialog ():#line:226
    global app #line:227
    app =QApplication (sys .argv )#line:228

