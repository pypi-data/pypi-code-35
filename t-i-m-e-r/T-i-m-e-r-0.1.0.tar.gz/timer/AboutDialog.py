import tkinter as tk
import tkinter.font as tfont

from .lib.Dialog import Dialog
from .lib.InfoText import InfoText

from . import APP, VERSION, SITE


class AboutDialog(Dialog):
    def __init__(self, master):
        Dialog.__init__(self, master)

        self.toplevel.title('About')
        self.toplevel.resizable(False, False)

        font1 = tfont.Font(font=('Helvetica', 12))
        font2 = font1.copy(); font2['weight'] = 'bold'
        font3 = font1.copy(); font3['underline'] = True

        fonts_by_name = {'font1': font1, 'font2': font2}

        infotext = InfoText(self.toplevel)
        infotext.text.pack(expand=True, fill=tk.BOTH)

        infotext.text.configure(wrap=tk.WORD, font=font1, padx=12, pady=12, borderwidth=0, highlightthickness=0, background='#FFF', cursor='arrow', width=48, height=5)

        def visit_site(_, *, token):
            import webbrowser

            s = ''.join(_[1] for _ in infotext.text.dump(token['begin'], token['end'], text=True))
            webbrowser.open(s, autoraise=False)

        def onenter(_, *, token):
            infotext.text.configure(cursor='hand2')
            infotext.text.tag_configure(token['tag'], font=font3)

        def onleave(_, *, token):
            infotext.text.configure(cursor='arrow')
            infotext.text.tag_configure(token['tag'], font=font1)

        funcs_by_name = {'visit_site': visit_site, 'onenter': onenter, 'onleave': onleave}

        infotext.show('<h1 font="font2" spacing3="6">%s %s</h1>\nA better count-down timer in tkinter. Visit <a foreground="blue" spacing2="6" BINDINGS="ButtonRelease-1 => visit_site, Enter => onenter, Leave => onleave">%s</a> for more information.' % (APP, VERSION, SITE), funcs_by_name=funcs_by_name, fonts_by_name=fonts_by_name)
