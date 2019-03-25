# --------------------------------------------------------------------
# Configuration for EC4SAP Clients
# --------------------------------------------------------------------

#
# Debug level
#
# ignore | default | error
#
CFG_DEBUG="ignore"

#
# Abiquo API Endpoints
#
CFG_API_URL_INT = "https://testportal.sap.cloudservice.swisscom.com/api"
CFG_API_VERSION_INT = "4.5"
CFG_API_URL_PRD = "https://portal.sap.cloudservice.swisscom.com/api"
CFG_API_VERSION_PRD = "4.5"
CFG_API_DEFAULT = "prd"

#
# CSV Export : Format of a row
#
# map with Column-Name / Column-Value
#
CSV_FORMAT_VM = [("FQDN", "fqdn"),
                 ("ABQ_ID", "name"),
                 ("VAPP", "virtualappliance"),
                 ("TENANT", "enterprise"),
                 ("CPU", "cpu"),
                 ("RAM", "ram"),
                 ("IP", "nic*")]

CSV_FORMAT_IP = [("IP", "ip"),
                 ("VDC", "virtualdatacenter"),
                 ("NETWORK", "networkName"),
                 ("VM", "usedBy")]
#
# vm filter
#
# for full list see: https://wiki.abiquo.com/api/latest/virtualmachine.html
#
CFG_VM_FILTER = {}
CFG_VM_FILTER["type"] = ["MANAGED","CAPTURED"]
#CFG_VM_FILTER["protected"] = [True,False]
#CFG_VM_FILTER["state"] = ["ON","OFF", "PAUSED", "CONFIGURED", "LOCKED", "NOT_ALLOCATED", "ALLOCATED", "UNKNOWN"]

#
# ip filter
#
# for full list see: https://wiki.abiquo.com/api/latest//privateip.html
#
CFG_IP_FILTER = {}
CFG_IP_FILTER["usedBy"] = ["*"]

