from utils.datadict import DataDictionnary
import configparser
import datetime

cfg = configparser.ConfigParser()
cfg.read('./config.txt')
default = cfg['default_sl']
#base = cfg['general'].get('date_format_in_sap',None)

if default.get('valid_from') == "today":
    valid = datetime.datetime.today().strftime(cfg['general'].get('date_format_in_sap'))
else:
    valid = default.get('valid_from')

if default.get('fixed',None).lower() == 'false':
    fixed = False
else:
    fixed = True

if default.get('blocked',None).lower() == 'false':
    blocked = False
else:
    blocked = True

DEFAULT_SL = DataDictionnary({"Valid From" : valid,
                              "Valid To" : default.get('valid_to','31.12.9999'),
                              "Vendor": default.get('vendor',None),
                              "POrg": default.get('porg',None),
                              "Vendor Plant" : default.get('vendor_plant',None),
                              "Unit": default.get('unit',None),
                              "Agreement Nb" : default.get('agreement_nb',None),
                              "Agreement Item" : default.get('agreement_item',None),
                              "Fixed" : fixed,
                              "Blocked" : blocked,
                              "MRP" : default.get('mrp',None),})



