#!/bin/env python3

import socket
import os
from pathlib import Path  # requires python 3.5
import sys
import yaml
import struct
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import argparse


def setup_parser():

    parser = argparse.ArgumentParser(
        prog="Epgnotify",
        description="Parses EPG data from VDR, checks against search config and sends mail. Already sent programs are stored in a cache to avoid multiple notifications on same program.",
    )

    parser.add_argument(
        "--config",
        type=str,
        metavar="file",
        help="Config file. If not given ~/epgnotify.yml is used.",
    )

    parser.add_argument(
        "--stdout",
        action="store_true",
        default=False,
        help="Additionally print result to stdout",
    )

    parser.add_argument(
        "--cache-file",
        type=str,
        metavar="file",
        help="Optionally, cache file location, default epgnotfiy.cache.yaml in home directory is used. Use /dev/null to disable caching.",
    )

    parser.add_argument(
        "--epg-dst-file",
        type=str,
        default=None,
        metavar="file",
        help="Store received EPG data to a file",
    )

    return parser


def read_till_msg(sock, msg):
    """
    Reads from socket until stream ends in msg.

    Parameter
    ---------
    sock : socket
        Socket to read from

    msg : bytearray
        bytearray

    Returns
    ------
    str

    """
    d = b""
    while True:
        data = sock.recv(4096)
        d += data
        if d.endswith(msg):
            break

    return d.decode("utf-8", "backslashreplace")


def programlist_to_html(program_list, link_base=None):
    """
    Generates nicely formatted HTML file from list of programs.
    """

    HTML_hdr = """
    <!DOCTYPE html>
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <style type="text/css">
    ul {padding-left:2em;}
    table {width: 100%}
    td {text-align: center;}
    td.lft {text-align: left;}
    table, th, td { border: 1px solid black; }
    </style>
    <title>epgnotify list</title>
    </head>
    <body>
    <table>
    <tr>
    <th><b>Channel</b></th>
    <th><b>Program</b></th>
    <th><b>Description</b></th>
    <th><b>Match</b></th>
    <th><b>Streams</b></th>
    </tr>
    """

    HTML_ftr = """
    </table></body></html>"""

    lst = []
    for p in program_list:
        lst.append("<tr>")

        eid, starttime, duration = p["E"].split(" ")

        duration = float(duration)
        starttime = int(starttime)
        # starttime=time.strftime('%Y-%m-%d %H:%M:%S',  time.gmtime(starttime))
        # starttime=time.strftime('%a %b %d %H:%M:%S %Z %Y',
        #                        time.localtime(starttime))

        starttime = time.asctime(time.localtime(starttime))
        # add channel info
        cid, cname = p["C"].split(" ", 1)
        s = "<td>{}<br><b>{}</b><br>{}</td>".format(cid, cname, eid)
        lst.append(s)

        # add program info
        s = "<td>{}<br><b>{}</b><br>".format(starttime, p["T"])
        if "G" in p:
            s += "Genre: {}<br>".format(p["G"])
        s += "Duration (min): {}".format(int(duration // 60))

        s += '<br><a href="{}/vdradmin.pl?aktion=timer_new_form&epg_id={}&channel_id={}&referer={}">Link to vdradmin-am</a>'.format(
            link_base, int(eid), cid, "Li92ZHJhZG1pbi5wbD9ha3Rpb249dGltZXJfbGlzdA=="
        )
        # Li92ZHJhZG1pbi5wbD9ha3Rpb249dGltZXJfbGlzdA== is base64 encoded
        # for "./vdradmin.pl?aktion=timer_list"

        s += "</td>"
        lst.append(s)

        # add description
        s = "<td>"
        if "S" in p:
            s += "<b>S: </b>" + p["S"]
        if "D" in p:
            if "S" in p:
                s += "<br>"
            s += "<b>D: </b>" + p["D"]
        s += "</td>"
        lst.append(s)

        # add matches
        s = '<td class="lft"><ul><li>{}</li></ul></td>'.format(p["hit"])
        lst.append(s)

        # add streams
        s = "<td><ul>"
        if "X" in p:
            for x in p["X"]:
                s += "<li>{}/<li>".format(x)
        s += "</ul></td>"
        lst.append(s)

        lst.append("</tr>")

    return HTML_hdr + "\n".join(lst) + HTML_ftr


# search_config={
#    'title': [ {'title': 'Moderne Wunder',
#                'nosubtitle': ['Episode 24',
#                         'Hubschrauber',
#                         'Retrotechnik',
#                         'Groß & Klein',
#                         'Handwerk']
#                },
#                'Abenteuer Erde',
#                'Avengers',
#               'Auf Enteckungsreise',
#               ],
#    'notitle': ['Ö3',],
#    'nochannel': ['Sky Cinema', 'SYFY HD', 'Discovery HD'],
#    }


def check_program(program, search_config):

    T = program["T"]

    # title blacklist
    if "notitle" in search_config:
        for t in search_config["notitle"]:
            if t == T:
                return False

    # channel blacklist
    if "nochannel" in search_config:
        for noC in search_config["nochannel"]:
            if noC in program["C"]:
                return False

    # title match
    for t in search_config["title"]:
        if t == T:
            program["hit"] = "title " + t
            return True

    # in title
    for t in search_config["intitle"]:
        # just detect title
        if type(t) == str and t in T:
            program["hit"] = "intitle " + t
            return True

        # title detection with blacklist
        if type(t) == dict and t["intitle"] in T:
            # if search has subtitle blacklist and program has subtitle
            if "notintitle" in t:
                for notintitle in t["notintitle"]:
                    if notintitle in T:
                        return False
            if "notinsubtitle" in t and "S" in program:
                for nosub in t["notinsubtitle"]:
                    if nosub in program["S"]:
                        return False
            if "nosubtitle" in t and "S" in program:
                for nosub in t["nosubtitle"]:
                    if nosub == program["S"]:
                        return False
            if "notitle" in t:
                for notitle in t["notitle"]:
                    if notitle == T:
                        return False

            program["hit"] = "title " + t["intitle"]
            return True

    # in subtitle
    if "insubtitle" in search_config and "S" in program:
        for t in search_config["insubtitle"]:
            if t in program["S"]:
                program["hit"] = "insubtitle"
                return True

    # in description
    if "indescription" in search_config and "D" in program:
        for t in search_config["indescription"]:
            # detect string in description
            if t in program["D"]:
                program["hit"] = "indescription " + t
                return True

    return False


def send_email(HTML_string, subject_string, config):
    # send email

    if "from_email" in config:
        sender = config["from_email"]
    else:
        sender = config["email"]

    receiver = config["email"]

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject_string
    msg["From"] = sender
    msg["To"] = receiver

    # text='See HTML'
    # part1=MIMEText(text,'plain')
    # msg.attach(part1)

    # html mail
    part2 = MIMEText(HTML_string, "html")
    msg.attach(part2)

    smtp = smtplib.SMTP("localhost")
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.close()


def main():
    parser = setup_parser()
    args = parser.parse_args()

    # with open('search_config.yml', 'w') as outfile:
    #    yaml.dump(search_config, outfile, default_flow_style=False, allow_unicode=True)

    # load config
    if not args.config:
        filename = os.path.join(str(Path.home()), "epgnotify.yml")
    else:
        filename = args.config
    with open(filename, "r") as f:
        config = yaml.load(f)

    # load cache (already sent notifications)
    if not args.cache_file:
        cache_file = os.path.join(str(Path.home()), "epgnotify.cache.yml")
    else:
        cache_file = args.cache_file
    if os.path.isfile(cache_file):
        with open(cache_file, "r") as f:
            cache = yaml.load(f)
    else:
        cache = []

    # make socket connection to VDR
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = config["vdrhost"]
    port = config["vdrport"]
    sock.connect((host, port))
    sock.settimeout(10)

    # get and check VDR's greeting message
    data = read_till_msg(sock, "\n".encode())
    if not data.startswith("220 "):
        raise Exception("Got unexpected greeting message: " + data)
    if not data.endswith("UTF-8\r\n"):
        raise Exception("Encoding does not seem to be UTF-8")

    # request EPG data
    sock.send("LSTE\n".encode("utf-8"))
    data = read_till_msg(sock, b"215 End of EPG data\r\n")

    # close connection
    sock.send("QUIT\n".encode("utf-8"))

    if args.epg_dst_file:
        with open(args.epg_dst_file, "w") as f:
            f.write(data)

    # parse EPG data and store interesting programs in a list
    program_list = []
    all_programs = []
    for line in data.split("\n"):
        if len(line) < 5:
            continue
        # print(len(line), line[4:])
        hdr = line[4]
        if hdr == "C":  # start of a new channel section
            channel = line[6:]
        elif hdr == "c":  # end of a channel secion
            pass
        elif hdr == "E":  # start of a new program
            program = {"E": line[6:].rsplit(" ", 2)[0]}
        elif hdr in "TSDGRV":  # program description
            program[hdr] = line[6:]
        elif hdr == "X":  # streams (can occur many times)
            if "X" not in program:
                program["X"] = []
            program["X"].append(line[6:])
        elif hdr == "e":  # end of a program description
            program["C"] = channel
            all_programs.append(program)
            if check_program(program, config) and program not in cache:
                # print(program)
                program_list.append(program)
        else:
            raise Exception("Got unexpected line: " + line)

    # convert to nice HTML table
    if "vdradmin_link" in config:
        link_base = config["vdradmin_link"]
    else:
        link_base = None
    HTML_string = programlist_to_html(program_list, link_base)

    # print to stdout
    if args.stdout:
        print(HTML_string)

    # send via mail
    if "email" in config:
        subject_string = "epgnotify found {} new programs for you".format(
            len(program_list)
        )

        send_email(HTML_string, subject_string, config)

    # prevent infinitely growing cache by purging
    # programs from cache that are not in EPG data any more
    cache = [c for c in cache if c not in all_programs]

    # add currently found programs to cache
    cache.extend(program_list)

    # sort cache (makes it much easier to debug)
    cache = sorted(cache, key=lambda k: k["E"])

    # write cache
    with open(cache_file, "w") as f:
        yaml.dump(cache, f, allow_unicode=True)


if __name__ == "__main__":
    main()
