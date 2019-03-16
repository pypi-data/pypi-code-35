#-------------------------------------------------------------------------------
# Name:        ttgallery
# Purpose:     Demostrate use of tkintertoy widgets
#
# Author:      mike.callahan
#
# Created:     11/22/2017
# Copyright:   (c) mike.callahan 2017
# License:     MIT
#-------------------------------------------------------------------------------

from tkintertoy import Window
import time, ttk

class Gui(object):

    def __init__(self):
        self.gui = Window()
        self.gui.setTitle('Tkintertoy Gallery')
        self.makeGui()

    def makeGui(self):
        # a simple menu
        self.gui.addMenu('ttmainmenu', self.gui.master)
        menu = [['command', {'label':'About', 'command':self.popAbout}],
            ['command', {'label':'ChooseColor', 'command':self.popColor}]]
        self.gui.addMenu('ttmenu', self.gui.get('ttmainmenu'), menu)
        self.gui.get('ttmainmenu').add('cascade', label='Menu', menu=self.gui.get('ttmenu'))
        self.gui.master['menu'] = self.gui.get('ttmainmenu')
        # Notebook
        tabs = ['Simple','Dialog','Multi','Other']
        self.pages = self.gui.addNotebook('ttnotebook', tabs)
        # Text Box
        self.gui.addText('ttext', 60, 10, 'Text Box')
        self.gui.plot('ttext', row=1)
        # Progress Bar
        self.gui.addProgress('ttprogress', 100, 'Progress Bar')
        self.gui.plot('ttprogress', row=2)
        # Command Buttons
        cmd = [['Collect',self.collect],['Exit', self.gui.cancel]]
        self.gui.addButton('ttbutton', cmd)
        self.gui.plot('ttbutton', row=3)
        # Notebook Pages
        self.makeSimple()
        self.makeDialog()
        self.makeMulti()
        self.makeOther()
        self.gui.plot('ttnotebook', row=0)

    def makeSimple(self):
        self.simplePage = self.pages[0]
        # Label
        self.simplePage.addLabel('ttlabel','','bold', text='This is a BOLD label')
        self.simplePage.plot('ttlabel', row=0)
        # Line
        self.simplePage.addLine('ttline')
        self.simplePage.plot('ttline', row=1)
        # Message
        self.simplePage.addMessage('ttmessage', 'Message Box')
        self.simplePage.set('ttmessage', 'Useful for multi-line messages')
        self.simplePage.plot('ttmessage', row=2)
        # Entry
        self.simplePage.addEntry('ttentry', 'Entry Box')
        self.simplePage.set('ttentry', 'Default Entry')
        self.simplePage.plot('ttentry', row=3)
        # Option
        alist = ['Option1','Option2','Option3']
        self.simplePage.addOption('ttoption', alist, 'Option Box')
        self.simplePage.set('ttoption', 'Option1')
        self.simplePage.plot('ttoption', row=5)
        # Combobox and Style
        acombo = ['ComboOption1','ComboOption2','ComboOption3']
        self.simplePage.addStyle('new.TCombobox', foreground='red')
        self.simplePage.addCombo('ttcombo', acombo, 'Combo Box', style='new.TCombobox')
        self.simplePage.plot('ttcombo', row=6)
        # Checkboxes
        achecks = ['CheckOption1','CheckOption2','CheckOption3']
        self.simplePage.addCheck('ttchecks', achecks, 'Check Box')
        self.simplePage.plot('ttchecks', row=7)
        # Radio Buttons
        aradio = ['RadioOption1','RadioOption2','RadioOption3']
        self.simplePage.addRadio('ttradio', aradio, 'RadioButton Box')
        self.simplePage.plot('ttradio', row=8)
        # Scale
        self.simplePage.addScale('ttscale', 2, [1,10], 'Scale Box')
        self.simplePage.plot('ttscale', row=9)
        adate = [[2,1,12],[2,1,31],[4,2000,2099]]
        # Spinners
        self.simplePage.addSpin('ttspin', adate, '/', 'Date Box')
        self.simplePage.set('ttspin', [11,17,2017])
        self.simplePage.plot('ttspin', row=10)

    def makeDialog(self):
        self.dialogPage = self.pages[1]
        # Open
        self.dialogPage.addOpen('ttopen', 40, 'Open Box')
        self.dialogPage.plot('ttopen', row=0)
        # SaveAs
        self.dialogPage.addSaveAs('ttsaveas', 40, 'Save As Box')
        self.dialogPage.plot('ttsaveas', row=1)
        # ChooseDir
        self.dialogPage.addChooseDir('ttchoosedir', 40, 'Choose Dir Box')
        self.dialogPage.plot('ttchoosedir', row=2)

    def popColor(self):
        # Color Chooser
        self.gui.set('ttext', str(self.gui.popColorChooser(title='Select a Color')))

    def popAbout(self):
        # Pop Up Message Box
        self.gui.popMessage('Tkintertoy Gallery')

    def makeMulti(self):
        self.multiPage = self.pages[2]
        # List
        alist = ['ListOption1','ListOption2','ListOption3']
        self.multiPage.addList('ttlist', 'List Box', alist, height=4)
        self.multiPage.plot('ttlist', row=0)
        # Ledger
        cols = [['column1',100],['column2',80],['column3',80]]
        self.multiPage.addLedger('ttledger', 4, cols, 'Ledger Box')
        self.multiPage.set('ttledger', [['header1','item1-1','item1-2']])
        self.multiPage.set('ttledger', [['header2','item2-1','item2-2']])
        self.multiPage.set('ttledger', [['header3','tiem3-1','item2-3']])
        self.multiPage.plot('ttledger', row=1)
        # Collector Frame
        self.subwin = self.multiPage.addFrame('ttframe', '', relief='groove')
        # -Combobox
        acombo = ['ComboOption2-1','ComboOption2-2','ComboOption2-3']
        self.subwin.addCombo('ttcombo2', acombo, 'Combo Box 2')
        self.subwin.plot('ttcombo2', row=0)
        # -Radio Button
        aradio = ['Radio2-1','Radio2-2','Radio2-3']
        self.subwin.addRadio('ttradio2',aradio, 'RadioButton Box 2')
        self.subwin.plot('ttradio2', row=1)
        # -Collector
        cols = [['Combo',100],['Radio', 100]]
        self.subwin.addCollector('ttcollector', 4, cols, ['ttcombo2','ttradio2'], 'Collector Box')
        self.subwin.plot('ttcollector', row=2)
        self.multiPage.plot('ttframe', row=2)

    def makeOther(self):
        self.otherPage = self.pages[3]
        # Canvas
        self.otherPage.addCanvas('ttcanvas', 300, 100, 'Canvas Box')
        self.otherPage.get('ttcanvas').create_oval(10 ,10 ,290 ,90 ,fill='green')
        self.otherPage.plot('ttcanvas', row=0)
        # Multipane
        paneTitles = ['Pane 1','Pane 2','Pane 3']
        panes = self.otherPage.addPanes('ttpane', paneTitles, orient='horizontal')
        for i in range(3):
            # -Label
            tag = 'ttlabel' + str(i)
            panes[i].addLabel(tag)
            panes[i].set(tag, 'Inner label {}'.format(i+1))
            panes[i].plot(tag)
        self.otherPage.plot('ttpane', row=1)

    def collect(self):
        # show contents of all widgets
        result = 'Contents of widgets\n  Simple Page:\n    '
        result += self.simplePage.get('ttlabel') + '\n    '
        result += self.simplePage.get('ttmessage') + '\n    '
        result += self.simplePage.get('ttentry') + '\n    '
        result += self.simplePage.get('ttcombo') + '\n    '
        result += str(self.simplePage.get('ttchecks')) + '\n    '
        result += str(self.simplePage.get('ttradio')) +'\n    '
        result += self.simplePage.get('ttoption') + '\n\n    '
        result += str(self.simplePage.get('ttscale')) + '\n\n    '
        result += str(self.simplePage.get('ttspin')) + '\n\n    '
        result += str(self.multiPage.get('ttlist')) + '\n    '
        self.gui.set('ttprogress', 33)
        self.gui.set('ttext', result, setValues=True)
        time.sleep(.5)
        result = '  File Page:\n    '
        result += self.dialogPage.get('ttopen') + '\n    '
        result += self.dialogPage.get('ttsaveas') + '\n    '
        result += self.dialogPage.get('ttchoosedir') + '\n    '
        self.gui.set('ttprogress', 66)
        self.gui.set('ttext', result)
        time.sleep(.5)
        result = '  Multi Page:\n    '
        result += str(self.multiPage.get('ttlist', True)) + '\n    '
        result += str(self.multiPage.get('ttledger', True)) + '\n    '
        result += str(self.subwin.get('ttcollector',True)) + '\n    '
        # Progress Bar
        self.gui.set('ttprogress', 100)
        self.gui.set('ttext', result)
        time.sleep(1.0)
        self.gui.set('ttprogress', 0)

def main():
    app = Gui()
    try:
        app.gui.waitforUser()
    except:
        errorMessage = app.gui.catchExcept()
        app.gui.popMessage(errorMessage, 'showwarning', 'Error')
        app.gui.destroy()

main()


