import  re
import  requests
PARSE_SLICE = re.compile(r'(\:\d*\:?\-?\d*)')
SUB_PARSE = re.compile(r'\[(.+)\]')


def getKeys(p) -> (str, list):
    if '[' in p and ']' in p:
        pk = [i.strip() for i in SUB_PARSE.findall(p)[0].split(',')]
    else:
        pk = []
    new_p = SUB_PARSE.sub('', p)
    return  new_p, pk


def ParseSlice(p) -> (str, slice):
    parse_slice_num = PARSE_SLICE.findall(p)
    if parse_slice_num:
        pp = parse_slice_num[0][1:]
        if ':' in pp:
            start,end = pp.split(":")
            start = int(start)
            if end:
                end = int(end)
            else:
                end = None

        else:
            start = int(pp)
            end = start +1

        

        new_p = PARSE_SLICE.sub('', p)
        
        return new_p,slice(start, end)

    return p,slice(None)


