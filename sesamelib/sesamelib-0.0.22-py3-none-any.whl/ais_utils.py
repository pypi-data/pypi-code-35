import io
import time
import traceback


import ais.stream

# ais types
GLOBAL = "global"
BRITTANY = "brittany"


def decode(msg, *,  ais_type=GLOBAL):
    """Decode a single msg in binary format.

    Note that in the brittany dataset taglblock timestamps are found in the cdv
    files, not the raw files. While the raw file can be decoded by the libais,
    the cdv files contains on each line the station timestamps and the raw ais
    message. This prevent us to decode with the same logic the cdv and the raw
    files. Since we want to keep the tagblock timestamp, we need to
    differentiate two cases
    """
    def _decode(raw):
        f = io.StringIO(raw)
        msg = None
        for msg in ais.stream.decode(f):
            pass
        f.close()
        return msg

    decoded = {}
    try:
        if ais_type == GLOBAL:
            decoded = _decode(msg)
        elif ais_type == BRITTANY:
            day, hour, _msg = msg.split(" ")
            decoded = _decode(_msg)
            if decoded:
                tagblock_timestamp = time.mktime(
                    time.strptime("%s %s" % (day, hour), "%Y/%m/%d %H:%M:%S"))
                decoded.update({"tagblock_timestamp": tagblock_timestamp})
        else:
            raise Exception("ais_type not recognized")
    except:
        print(msg)
        traceback.print_exc()
        with open("decoding_errors.txt", "w") as f:
            f.write(msg)
    return decoded


if __name__ == "__main__":
    # global type (taken from the dataset)
    msg = "\c:1488326400,s:rORBCOMM115*2E\!AIVDM,1,1,,B,15RjRh002>SlpSgkSM;a>GCp00S9,0*5B"
    decoded = decode(msg, ais_type=GLOBAL)
    print(decoded)
    # brittany type (taken from the dataset) -- will be decoded without station
    # timestamp
    msg = "!AIVDM,1,1,,A,13JEhD7P1>w`ApbK`Q8K??w22@CD,0*12"
    decoded = decode(msg, ais_type=GLOBAL)
    print(decoded)
    # brittany type (taken from the dataset)
    msg =  "2011/07/08 14:30:34 !AIVDM,1,1,,A,13JEhD7P1>w`ApbK`Q8K??w22@CD,0*12"
    decoded = decode(msg, ais_type=BRITTANY)
    print(decoded)
