# system modules
import collections
import json
import datetime
import io
import re
import hashlib
import csv
from urllib.parse import urlencode

# internal modules

# external modules


def parse_msgpack(d):
    """
    Parse :mod:`msgpack` encoded data.

    Args:
        d (bytes): the encoded msgpack data

    Raises:
        ImportError : if mod:`msgpack` is not installed
        ValueError: if the data could not be decoded
    """
    try:
        import msgpack
    except ImportError as e:  # prama: no cover
        raise type(e)("This server cannot decode msgpack formatted data")
    try:
        unpacked = msgpack.unpackb(d, raw=False)
    except msgpack.ExtraData as e:
        while len(d):
            try:
                unpacked = msgpack.unpackb(d, raw=False)
                break
            except msgpack.ExtraData:
                d = d[:-1]  # drop last byte
        if not len(d):
            raise ValueError("Could not decode MsgPack")
    return unpacked


def salted_checksum(payload, salt, algorithm):
    """
    Salt a given payload and calculate the checksum with a hash function

    Args:
        payload (str or bytes): the payload
        salt (str or bytes): the salt
        algorithm (str): the hash function as available in
            :any:`hashlib.algorithms_guaranteed`

    Returns:
        str : the hexadecimal checksum
    """
    payload = payload.encode() if isinstance(payload, str) else payload
    salt = salt.encode() if isinstance(salt, str) else salt
    h = hashlib.new(algorithm)
    h.update(bytearray(payload))
    h.update(bytearray(salt))
    return h.hexdigest()


def listdict_to_dictlist(d):
    """
    Convert a :any:`dict` of lists to a list of dicts

    Args:
        d (dict): the dict of lists

    Returns:
        list : list of dicts
    """
    return [dict(zip(d, t)) for t in zip(*d.values())]


def dictlist_to_listdict(l, fun=lambda x: x):
    """
    Convert a list of dicts to a dict of lists

    Args:
        l (list): the list of dicts
        fun (callable): callable to manipulate the values

    Returns:
        dict : dict of lists
    """
    d = collections.defaultdict(list)
    for e in l:
        for k, v in e.items():
            d[k].append(fun(v))
    return dict(d)


def str2num(s):
    try:
        i = int(s)
    except ValueError:
        i = None
    try:
        f = float(s)
    except ValueError:
        f = None
    return s if i == f is None else (i if i == f else f)


def csv2table(fd):
    csvreader = csv.DictReader(fd)
    return dictlist_to_listdict(csvreader, fun=str2num)


def header_cols_to_table(header, rows):
    d = collections.defaultdict(list)
    for row in rows:
        for h, r in zip(header, row):
            d[h].append(r)
    return dict(d)


def table2dict(header, rows):
    d = collections.defaultdict(list)
    for row in rows:
        for h, r in zip(header, row):
            d[h].append(r)
    return dict(d)


def dictlist2form(l):
    return "&".join([urlencode(row) for row in l])


def table2html(header, rows):
    table = ""
    table += "<table>\n"
    table += "<tr>\n"
    table += "\n".join(["<th>{}</th>".format(x) for x in header])
    table += "\n</tr>\n"
    for row in rows:
        table += "<tr>\n"
        table += "\n".join(
            "<td>{}</td>".format(x if x is not None else "") for x in row
        )
        table += "\n</tr>\n"
    table += "</table>\n"
    return table


def table2json(header, rows):
    L = [{c: v for c, v in zip(header, row)} for row in rows]
    return json.dumps(L, default=str, indent=4, sort_keys=True)


def table2csv(header, rows):
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=header)
    writer.writeheader()
    for row in rows:
        writer.writerow({c: v for c, v in zip(header, row)})
    return buf.getvalue()


def sqlsep(l):
    quoter = {
        type(None): lambda x: "NULL",
        str: lambda x: "'{}'".format(sanitize(x)),
    }
    return ",".join([quoter.get(type(x), lambda x: str(x))(x) for x in l])


def sanitize(value):
    return re.sub("[^a-z0-9.:+_ -]", "", str(value), flags=re.IGNORECASE)


def urlencode_multi_dict(d):
    return "&".join(
        [
            urlencode({k: v for k, v in zip(d.keys(), values)})
            for values in zip(*d.values())
        ]
    )


def dictkeys2lower(d):
    return {k.lower(): v for k, v in d.items()}


def unix_timestamp(dt):
    if dt.tzinfo:
        dt = dt.astimezone(datetime.timezone.utc)
    else:
        dt = dt.replace(tzinfo=datetime.timezone.utc)
    return int(
        (
            dt - datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
        ).total_seconds()
    )


def utc_datetime_from_unix_timestamp(seconds):
    return datetime.datetime(
        1970, 1, 1, tzinfo=datetime.timezone.utc
    ) + datetime.timedelta(seconds=int(seconds))


def header_from_cursor(cursor):
    return [c[0] for c in cursor.description]
