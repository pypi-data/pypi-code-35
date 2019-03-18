def map_list_of_dicts( list_of_dicts, *keys ):
    result = {}
    last_key = keys[-1]
    for d in list_of_dicts:
        last_map = result
        for k in keys[:-1]:
            last_map = last_map.setdefault( d[k], {} )
        last_map.setdefault( d[ last_key ], [] ).append( d )
    return result


def map_list_of_obj( list_of_obj, *keys ):
    result = {}
    last_key = keys[-1]
    for obj in list_of_obj:
        last_map = result
        for k in keys[:-1]:
            last_map = last_map.setdefault( getattr( obj, k, None ), {} )
        last_map.setdefault( getattr( obj, last_key, None ), [] ).append( obj )
    return result
