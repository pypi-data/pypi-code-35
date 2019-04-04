#import json
#from suds-jurko.sudsobject import asdict #for v3+
from suds.sudsobject import asdict

'''
Salesforce API will return two different payloads:
    - for SOAP it will be a SUDS object
    - for REST it will be a REST object

This library will help jsonify the salesforce response
no matter SOAP or REST
'''

def sfmc_to_json(object_name, obj):
    """Take an object and drop it into JSON, the object_name parameter is used
        to prefeix the JSON package"""
    if object_name is None:
        object_name = "element" 
    if isinstance(obj, dict):
        data = obj["items"]
    elif isinstance(obj, list):
        data = _list_of_suds_to_json(object_name, obj)
    key_prefix = (object_name+"s").lower()
    return { key_prefix : data }

def _recursive_asdict(d):
    """Convert Suds object (What API returns) into serializable format."""
    out = {}
    for k, v in asdict(d).items():
        if hasattr(v, "__keylist__"):
            out[k] = _recursive_asdict(v)
        elif isinstance(v, list):
            out[k] = []
            for item in v:
                if hasattr(item, "__keylist__"):
                    out[k].append(_recursive_asdict(item))
                else:
                    out[k].append(item)
        else:
            out[k] = v
    return out

def _suds_to_json(data):
    """Takes a suds object to a json object, will recurse and hand date objects"""
    json_string = json.dumps(_recursive_asdict(data), indent=4, sort_keys=True, default=str)
    return json.loads(json_string)

def _list_of_suds_to_json(object_name, list):
    """Processes a list of suds objects (can be nested) and turns in to json object"""
    data = []
    for item in list:
        my_json =  _suds_to_json(item)
        data.append(my_json)
    return data