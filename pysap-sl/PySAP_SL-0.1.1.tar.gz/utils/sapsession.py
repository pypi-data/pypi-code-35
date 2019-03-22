import sys, win32com.client
from pywintypes import com_error

class SapSession():
    
    def __init__(self,system):
        self.System = system
        self.attach_session()

    def attach_session(self):
        SapGuiAuto = win32com.client.GetObject("SAPGUI")
        if not type(SapGuiAuto) == win32com.client.CDispatch:
            print('error')
            return

        application = SapGuiAuto.GetScriptingEngine
        if not type(application) == win32com.client.CDispatch:
            SapGuiAuto = None
            print('error')
            return

        for connection in application.Children:
            if type(connection) == win32com.client.CDispatch:
                for session in connection.Children:
                    if type(session) == win32com.client.CDispatch and session.Info.SystemName + session.Info.Client == self.System :
                        self.Session = session
                        break

        if not self.Session:
            connection = None
            application = None
            SapGuiAuto = None
            session = None
            print("Error during attach_session")
        else:
            print("Session successfully attached")


    def verify_gui_element(self, gui_element_id):
        if self.Session:
            try:
                self.Session.findById(gui_element_id).text
                return True
            except com_error:
                return False
        else:
            print('No SAP session attached')
            return False

    def verify_transaction_success(self):
        if self.Session.findById("wnd[0]/sbar").MessageType == "S":
            return True
        else:
            return False

        
