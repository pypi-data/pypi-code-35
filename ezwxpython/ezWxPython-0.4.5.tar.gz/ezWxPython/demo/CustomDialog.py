import os
import sys
import time
import wx
import ezWxPython as ew

dialog_layout = [
    [ ew.Text('', expand=True,proportion=1,key='text'), 
      ew.Line(),
      ew.Button("OK") ],
]

def onExit(event):
    appWin.close()
   
def onAbout(event):
    appWin.messageBox("About", "TextEntry Demo\nzdiv")

def onButton(event):
    appWin.dialog("Custom Dialog Demo",dialog_layout)

menu_def = { 
    "File" : { 
        "Exit" : [ onExit, wx.ART_QUIT ],
    }, 
    "Help" : { 
        "About" : onAbout 
    },
}

body_def = [
    [ ew.Text('', expand=True,proportion=1,key='text'), 
      ew.Line(),
      ew.Button("Dialog",handler=onButton,key='button'), ],
]

status_def = [
    ["Ready", -1],
]

layout = {
    "menu"   : menu_def,
    "body"   : body_def, 
    "status"   : status_def, 
}

######################################################################
# Main
######################################################################

if __name__ == "__main__":
    appWin = ew.WxApp(u"Menu Demo", 320, 240)
    appWin.makeLayout(layout)
    appWin.run()
