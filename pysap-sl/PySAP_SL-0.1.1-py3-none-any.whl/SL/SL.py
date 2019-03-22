import utils.DEFAULT

class SL():
    
    def __init__(self, material, plant, app, data=None):
        self.Material = material
        self.Plant = plant
        self.app = app
        self.session = app.Session
        
        if data:
            self.Data = [utils.DEFAULT.DEFAULT_SL.get_copy()] * len(data)
            for count, sl_dict in enumerate(data):
                self.Data[count].update_default(sl_dict)
        else:
            self.Data = [utils.DEFAULT.DEFAULT_SL.get_copy()]

    def __str__(self):
        return "Source list for mat {} on plant {} \n {}".format(self.Material, self.Plant, self.Data)

    def __repr__(self):
        return "Source list for mat {} on plant {} \n{}".format(self.Material, self.Plant, self.Data)

    def pre_run(self):
        for data in self.Data:
            data.clear_none()
            
    def update_data(self, new_data, reset=False):
        if reset == True:
            self.Data = [utils.DEFAULT.DEFAULT_SL.get_copy()] * len(new_data)

        if len(new_data) > len(self.Data):
            diff = len(new_data) - len(self.Data)
            add = [utils.DEFAULT.DEFAULT_SL.get_copy()] * diff
            self.Data =  self.Data + add
            
        for count, sl_dict in enumerate(new_data):
            self.Data[count].update_default(sl_dict)

    def update_sl(self, ignore_warning=True):

        self.pre_run()
        
        self.session.findById("wnd[0]/tbar[0]/okcd").text = "/nMe01"
        self.session.findById("wnd[0]").sendVKey(0)
        self.session.findById("wnd[0]/usr/ctxtEORD-MATNR").text = self.Material
        self.session.findById("wnd[0]/usr/ctxtEORD-WERKS").text = self.Plant
        self.session.findById("wnd[0]").sendVKey(0)

        if ignore_warning:
            while self.session.findById("wnd[0]/sbar").MessageType == "W":
                self.session.findById("wnd[0]").sendVKey(0)
    
        if self.session.findById("wnd[0]/sbar").MessageType == "E":
            return None
        
        for sl in self.Data:
            
            cnt = 0
            
            while self.session.findById("wnd[0]/usr/tblSAPLMEORTC_0205/ctxtEORD-VDATU[0,{}]".format(cnt)).text:
                if sl['Vendor'] == self.session.findById("wnd[0]/usr/tblSAPLMEORTC_0205/ctxtEORD-LIFNR[2,{}]".format(cnt)).text:
                    break
                else:
                    cnt += 1
        
            self.session.findById("wnd[0]/usr/tblSAPLMEORTC_0205/ctxtEORD-VDATU[0,{}]".format(cnt)).text = sl['Valid From']
            self.session.findById("wnd[0]/usr/tblSAPLMEORTC_0205/ctxtEORD-BDATU[1,{}]".format(cnt)).text = sl['Valid To']
            self.session.findById("wnd[0]/usr/tblSAPLMEORTC_0205/ctxtEORD-LIFNR[2,{}]".format(cnt)).text = sl['Vendor']
            self.session.findById("wnd[0]/usr/tblSAPLMEORTC_0205/ctxtEORD-EKORG[3,{}]".format(cnt)).text = sl['POrg']
            print(sl)
            self.session.findById("wnd[0]/usr/tblSAPLMEORTC_0205/ctxtEORD-RESWK[4,{}]".format(cnt)).text = sl['Vendor Plant']
            self.session.findById("wnd[0]/usr/tblSAPLMEORTC_0205/ctxtEORD-MEINS[5,{}]".format(cnt)).text = sl['Unit']
            self.session.findById("wnd[0]/usr/tblSAPLMEORTC_0205/ctxtEORD-EBELN[6,{}]".format(cnt)).text = sl['Agreement Nb']
            self.session.findById("wnd[0]/usr/tblSAPLMEORTC_0205/ctxtEORD-EBELP[7,{}]".format(cnt)).text = sl['Agreement Item']
        
            if sl['Blocked']:
                self.session.findById("wnd[0]/usr/tblSAPLMEORTC_0205/chkEORD-NOTKZ[9,{}]".format(cnt)).selected = True
            else:
                self.session.findById("wnd[0]/usr/tblSAPLMEORTC_0205/chkEORD-NOTKZ[9,{}]".format(cnt)).selected = False

            if sl['Fixed']:
                self.session.findById("wnd[0]/usr/tblSAPLMEORTC_0205/chkRM06W-FESKZ[8,{}]".format(cnt)).selected = True
            else:
                self.session.findById("wnd[0]/usr/tblSAPLMEORTC_0205/chkRM06W-FESKZ[8,{}]".format(cnt)).selected = False
                
            self.session.findById("wnd[0]/usr/tblSAPLMEORTC_0205/ctxtEORD-AUTET[10,{}]".format(cnt)).text = sl['MRP']
            
        self.session.findById("wnd[0]").sendVKey(11)

        if ignore_warning:
            while self.session.findById("wnd[0]/sbar").MessageType == "W":
                self.session.findById("wnd[0]").sendVKey(0)

        if self.session.findById("wnd[0]/sbar").MessageType == "E":
            return None
        
        if self.app.verify_transaction_success() == False:
            print("Error occured")

    def create_sl(self, ignore_warning=True):

        self.pre_run()
        
        if self.is_exist() == True:
            print("SL already exist for this mat-plant, please use update_sl method instead")
            return None
        
        self.session.findById("wnd[0]/tbar[0]/okcd").text = "/nMe01"
        self.session.findById("wnd[0]").sendVKey(0)
        self.session.findById("wnd[0]/usr/ctxtEORD-MATNR").text = self.Material
        self.session.findById("wnd[0]/usr/ctxtEORD-WERKS").text = self.Plant
        self.session.findById("wnd[0]").sendVKey(0)

        if ignore_warning:
            while self.session.findById("wnd[0]/sbar").MessageType == "W":
                self.session.findById("wnd[0]").sendVKey(0)

        if self.session.findById("wnd[0]/sbar").MessageType == "E":
            return None

        cnt = 0
        
        for sl in self.Data:
            print(sl)
            self.session.findById("wnd[0]/usr/tblSAPLMEORTC_0205/ctxtEORD-VDATU[0,{}]".format(cnt)).text = sl['Valid From']
            self.session.findById("wnd[0]/usr/tblSAPLMEORTC_0205/ctxtEORD-BDATU[1,{}]".format(cnt)).text = sl['Valid To']
            self.session.findById("wnd[0]/usr/tblSAPLMEORTC_0205/ctxtEORD-LIFNR[2,{}]".format(cnt)).text = sl['Vendor']
            self.session.findById("wnd[0]/usr/tblSAPLMEORTC_0205/ctxtEORD-EKORG[3,{}]".format(cnt)).text = sl['POrg']
            self.session.findById("wnd[0]/usr/tblSAPLMEORTC_0205/ctxtEORD-RESWK[4,{}]".format(cnt)).text = sl['Vendor Plant']
            self.session.findById("wnd[0]/usr/tblSAPLMEORTC_0205/ctxtEORD-MEINS[5,{}]".format(cnt)).text = sl['Unit']
            self.session.findById("wnd[0]/usr/tblSAPLMEORTC_0205/ctxtEORD-EBELN[6,{}]".format(cnt)).text = sl['Agreement Nb']
            self.session.findById("wnd[0]/usr/tblSAPLMEORTC_0205/ctxtEORD-EBELP[7,{}]".format(cnt)).text = sl['Agreement Item']
        
            if sl['Blocked']:
                self.session.findById("wnd[0]/usr/tblSAPLMEORTC_0205/chkEORD-NOTKZ[9,{}]".format(cnt)).selected = True
            if sl['Fixed']:
                self.session.findById("wnd[0]/usr/tblSAPLMEORTC_0205/chkRM06W-FESKZ[8,{}]".format(cnt)).selected = True
                
            self.session.findById("wnd[0]/usr/tblSAPLMEORTC_0205/ctxtEORD-AUTET[10,{}]".format(cnt)).text = sl['MRP']
            cnt += 1
            
        self.session.findById("wnd[0]").sendVKey(11)

        if ignore_warning:
            while self.session.findById("wnd[0]/sbar").MessageType == "W":
                self.session.findById("wnd[0]").sendVKey(0)

        if self.session.findById("wnd[0]/sbar").MessageType == "E":
            return None
        
        if self.app.verify_transaction_success() == False:
            print("Error occured")

        print("SL creation executed with success for mat-plant {} -- {}".format(self.Material, self.Plant))
        
    def extract_sl(self):
        
        self.session.findById("wnd[0]/tbar[0]/okcd").text = "/nMe03"
        self.session.findById("wnd[0]").sendVKey(0)
        self.session.findById("wnd[0]/usr/ctxtEORD-MATNR").text = self.Material
        self.session.findById("wnd[0]/usr/ctxtEORD-WERKS").text = self.Plant
        self.session.findById("wnd[0]").sendVKey(0)

        while self.session.findById("wnd[0]/sbar").MessageType == "W":
            self.session.findById("wnd[0]").sendVKey(0)

        if self.session.findById("wnd[0]/sbar").MessageType == "E":
            return None
            
        cnt = 0
        sl_list = []
        
        while self.session.findById("wnd[0]/usr/tblSAPLMEORTC_0205/ctxtEORD-VDATU[0,{}]".format(cnt)).text:
            
            sl_dict = utils.DEFAULT.DEFAULT_SL.get_copy()
            
            sl_dict['Valid From'] = self.session.findById("wnd[0]/usr/tblSAPLMEORTC_0205/ctxtEORD-VDATU[0,{}]".format(cnt)).text
            sl_dict['Valid To'] = self.session.findById("wnd[0]/usr/tblSAPLMEORTC_0205/ctxtEORD-BDATU[1,{}]".format(cnt)).text
            sl_dict['Vendor'] = self.session.findById("wnd[0]/usr/tblSAPLMEORTC_0205/ctxtEORD-LIFNR[2,{}]".format(cnt)).text
            sl_dict['POrg'] = self.session.findById("wnd[0]/usr/tblSAPLMEORTC_0205/ctxtEORD-EKORG[3,{}]".format(cnt)).text
            sl_dict['Vendor Plant'] = self.session.findById("wnd[0]/usr/tblSAPLMEORTC_0205/ctxtEORD-RESWK[4,{}]".format(cnt)).text
            sl_dict['Unit'] = self.session.findById("wnd[0]/usr/tblSAPLMEORTC_0205/ctxtEORD-MEINS[5,{}]".format(cnt)).text
            sl_dict['Agreement Nb'] = self.session.findById("wnd[0]/usr/tblSAPLMEORTC_0205/ctxtEORD-EBELN[6,{}]".format(cnt)).text
            sl_dict['Agreement Item'] = self.session.findById("wnd[0]/usr/tblSAPLMEORTC_0205/ctxtEORD-EBELP[7,{}]".format(cnt)).text
            sl_dict['Blocked'] = self.session.findById("wnd[0]/usr/tblSAPLMEORTC_0205/chkEORD-NOTKZ[9,{}]".format(cnt)).selected
            sl_dict['Fixed'] = self.session.findById("wnd[0]/usr/tblSAPLMEORTC_0205/chkRM06W-FESKZ[8,{}]".format(cnt)).selected
            sl_dict['MRP'] = self.session.findById("wnd[0]/usr/tblSAPLMEORTC_0205/ctxtEORD-AUTET[10,{}]".format(cnt)).text
            
            cnt += 1
            sl_list.append(sl_dict)

        print("{} record for source list of {} - {}".format(cnt, self.Material, self.Plant))
        for dct in sl_list:
            print("----------------------")
            for key, value in dct.items():
                print(key + ": " + str(value))
            print("----------------------")

        return sl_list, cnt

    def delete_sl(self, sl_position=0,delete_all=False, delete_vendor=None, ignore_warning=True):
        
        self.session.findById("wnd[0]/tbar[0]/okcd").text = "/nMe01"
        self.session.findById("wnd[0]").sendVKey(0)
        self.session.findById("wnd[0]/usr/ctxtEORD-MATNR").text = self.Material
        self.session.findById("wnd[0]/usr/ctxtEORD-WERKS").text = self.Plant
        self.session.findById("wnd[0]").sendVKey(0)

        if ignore_warning:
            while self.session.findById("wnd[0]/sbar").MessageType == "W":
                self.session.findById("wnd[0]").sendVKey(0)

        if self.session.findById("wnd[0]/sbar").MessageType == "E":
            return None
        
        if delete_all == True:
            self.session.findById("wnd[0]").sendVKey(28)
            
        elif delete_vendor:
            cnt = 0
            while self.session.findById("wnd[0]/usr/tblSAPLMEORTC_0205/ctxtEORD-VDATU[0,{}]".format(cnt)).text:
                if delete_vendor == self.session.findById("wnd[0]/usr/tblSAPLMEORTC_0205/ctxtEORD-LIFNR[2,{}]".format(cnt)).text:
                    self.session.findById("wnd[0]/usr/tblSAPLMEORTC_0205").getAbsoluteRow(cnt).selected = True
                else:
                    cnt += 1
            
        else:
            self.session.findById("wnd[0]/usr/tblSAPLMEORTC_0205").getAbsoluteRow(sl_position).selected = True
            
        self.session.findById("wnd[0]").sendVKey(14)
        self.session.findById("wnd[1]/usr/btnSPOP-OPTION1").press()
        self.session.findById("wnd[0]").sendVKey(11)

        if ignore_warning:
            while self.session.findById("wnd[0]/sbar").MessageType == "W":
                self.session.findById("wnd[0]").sendVKey(0)

        if self.session.findById("wnd[0]/sbar").MessageType == "E":
            return None
        
        if self.app.verify_transaction_success() == False:
            print("Error occured")    

    def is_exist(self):
        
        self.session.findById("wnd[0]/tbar[0]/okcd").text = "/nMe03"
        self.session.findById("wnd[0]").sendVKey(0)
        self.session.findById("wnd[0]/usr/ctxtEORD-MATNR").text = self.Material
        self.session.findById("wnd[0]/usr/ctxtEORD-WERKS").text = self.Plant
        self.session.findById("wnd[0]").sendVKey(0)

        while self.session.findById("wnd[0]/sbar").MessageType == "W":
            self.session.findById("wnd[0]").sendVKey(0)

        if self.session.findById("wnd[0]/sbar").MessageType == "E":
            return False
        if self.session.findById("wnd[0]/usr/tblSAPLMEORTC_0205/ctxtEORD-VDATU[0,0]").text == "":
            return False
        else:
            return True

    def copy_sl_values(self):
        self.Data = self.extract_sl()[0]
        
