#!/usr/bin/env python
# -*- coding: utf-8 -*-

from six import string_types

BASE256 =  u"""⌀␁␂␃␄␅␆␇␈␉↲␋␌↼␎␏␐␑␒␓␔␕␖␗␘␙␚␛␜␝␞␟""" \
           u""" !"#$%&'()*+,-./0123456789:;<=>?""" \
           u"""@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_""" \
           u"""`abcdefghijklmnopqrstuvwxyz{|}~⇐""" \
           u"""ᄀᄁᄂᄃᄄᄅᄆᄇᄈᄉᄊᄋᄌᄍᄎᄏᄐᄑᄒᄓᄔᄕᄖᄗᄘᄙᄚᄛᄜᄝᄞᄟ"""\
           u"""ᄠᄡᄢᄣᄤᄥᄦᄧᄨᄩᄪᄫᄬᄭᄮᄯᄰᄱᄲᄳᄴᄵᄶᄷᄸᄹᄺᄻᄼᄽᄾᄿ"""\
           u"""ᅀᅁᅂᅃᅄᅅᅆᅇᅈᅉᅊᅋᅌᅍᅎᅏᅐᅑᅒᅓᅔᅕᅖᅗᅘᅙᅚᅛᅜᅝᅞ↯""" \
           u"""═║╒╓╔╕╖╗╘╙╚╛╜╝╞╟╠╡╢╣╤╥╦╧╨╩╪╫╬╭╮╯"""


DECODE_BASE256 = {c: i for i, c in enumerate(BASE256)}


def b256encode(buf):
    # type: (bytes) -> unicode
    """
    Encode bytes as base256 unicode string
    Args:
        buf: bytes-like

    Returns:
        string representation
    """
    return u''.join((BASE256[i] for i in bytearray(buf)))


def b256decode(unistr):
    # type: (string_types) -> bytearray
    dec = [DECODE_BASE256[c] for c in unistr]
    return bytearray(dec)


if __name__ == '__main__':
    print(len(BASE256))
    for i, c in enumerate(BASE256):
        print(u'{:02x}: {}'.format(i, b256encode([i])))



