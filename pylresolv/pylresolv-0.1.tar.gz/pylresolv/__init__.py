# pylresolv -- DNS querying through libc libresolv.so using ctypes
# Copyright (C) 2019  Walter Doekes, OSSO B.V.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import print_function, unicode_literals
import ctypes

try:
    # Nice to have, can live without it though
    from enum import IntEnum
except ImportError:
    IntEnum = object

__all__ = ('ns_class', 'ns_parse', 'ns_sect', 'ns_type', 'res_query')
if str == bytes:
    # "TypeError: Item in ``from list'' must be str, not unicode"
    __all__ = tuple(i.encode('ascii') for i in __all__)  # py2 madness

__version__ = (0, 1)

_libresolv = ctypes.CDLL('libresolv.so')
_res_ninit = _libresolv.__res_ninit
_res_nquery = _libresolv.__res_nquery
_ns_initparse = _libresolv.ns_initparse
_ns_parserr = _libresolv.ns_parserr
_ns_name_uncompress = _libresolv.ns_name_uncompress

# <arpa/nameser.h>

NS_MAXMSG = 65535   # maximum message size
NS_MAXDNAME = 1025  # maximum domain name


class ns_sect(IntEnum):
    ns_s_qd = 0     # Query: Question
    ns_s_an = 1     # Query: Answer
    ns_s_ns = 2     # Query: Name servers
    ns_s_ar = 3     # Query|Update: Additional records
    ns_s_zn = 0     # Update: Zone
    ns_s_pr = 1     # Update: Prerequisites
    ns_s_ud = 2     # Update: Update
    ns_s_max = 4    # MAX


class ns_class(IntEnum):
    ns_c_in = 1     # Internet


class ns_type(IntEnum):
    ns_t_invalid = 0
    # VALID
    ns_t_a = 1
    ns_t_ns = 2
    ns_t_md = 3
    ns_t_mf = 4
    ns_t_cname = 5
    ns_t_soa = 6
    ns_t_mb = 7
    ns_t_mg = 8
    ns_t_mr = 9
    ns_t_null = 10
    ns_t_wks = 11
    ns_t_ptr = 12
    ns_t_hinfo = 13
    ns_t_minfo = 14
    ns_t_mx = 15
    ns_t_txt = 16
    ns_t_rp = 17
    ns_t_afsdb = 18
    ns_t_x25 = 19
    ns_t_isdn = 20
    ns_t_rt = 21
    ns_t_nsap = 22
    ns_t_nsap_ptr = 23
    ns_t_sig = 24
    ns_t_key = 25
    ns_t_px = 26
    ns_t_gpos = 27
    ns_t_aaaa = 28
    ns_t_loc = 29
    ns_t_nxt = 30
    ns_t_eid = 31
    ns_t_nimloc = 32
    ns_t_srv = 33
    ns_t_atma = 34
    ns_t_naptr = 35
    ns_t_kx = 36
    ns_t_cert = 37
    ns_t_a6 = 38
    ns_t_dname = 39
    ns_t_sink = 40
    ns_t_opt = 41
    ns_t_apl = 42
    ns_t_ds = 43
    ns_t_sshfp = 44
    ns_t_ipseckey = 45
    ns_t_rrsig = 46
    ns_t_nsec = 47
    ns_t_dnskey = 48
    ns_t_dhcid = 49
    ns_t_nsec3 = 50
    ns_t_nsec3param = 51
    ns_t_tlsa = 52
    ns_t_smimea = 53
    ns_t_hip = 55
    ns_t_ninfo = 56
    ns_t_rkey = 57
    ns_t_talink = 58
    ns_t_cds = 59
    ns_t_cdnskey = 60
    ns_t_openpgpkey = 61
    ns_t_csync = 62
    ns_t_spf = 99
    ns_t_uinfo = 100
    ns_t_uid = 101
    ns_t_gid = 102
    ns_t_unspec = 103
    ns_t_nid = 104
    ns_t_l32 = 105
    ns_t_l64 = 106
    ns_t_lp = 107
    ns_t_eui48 = 108
    ns_t_eui64 = 109
    ns_t_tkey = 249
    ns_t_tsig = 250
    ns_t_ixfr = 251
    ns_t_axfr = 252
    ns_t_mailb = 253
    ns_t_maila = 254
    ns_t_any = 255
    ns_t_uri = 256
    ns_t_caa = 257
    ns_t_avc = 258
    ns_t_ta = 32768
    ns_t_dlv = 32769
    # MAX
    ns_t_max = 65536

    @classmethod
    def handle_invalid(cls, msg, rr):
        if rr.ns_rr_class() != ns_class.ns_c_in:
            # Unexpected answer..?
            return None

        # Very basic "not implemented" handler.
        decoded = rr.ns_rr_rdata__human()
        return decoded

    @classmethod
    def handle_mx(cls, msg, rr):
        if (rr.ns_rr_class() != ns_class.ns_c_in or
                rr.ns_rr_type() != cls.ns_t_mx):
            # Unexpected answer..?
            return None

        priority = (
            ctypes.cast(
                rr.ns_rr_rdata(),
                ctypes.POINTER(ctypes.c_uint16.__ctype_be__))
            .contents.value)
        dstbuf = ctypes.create_string_buffer(NS_MAXDNAME)
        bytes_read = _ns_name_uncompress(
                msg.ns_msg_base(), msg.ns_msg_end(),
                rr.ns_rr_rdata__offset(2), dstbuf, len(dstbuf))
        if bytes_read < 0:
            # Strange..?
            return None
        try:
            decoded = bytearray(dstbuf).decode('utf-8').split('\x00')[0] or '.'
        except UnicodeDecodeError:
            # Unexpected encoding..?
            return None

        return (priority, decoded)


class _res_state_t(ctypes.Structure):
    _fields_ = (
        # Opaque data. Seen as 568 bytes in glibc6-2.27.
        ('padding', ctypes.c_uint32 * (1024 // 4)),  # 1024 bytes > 568
    )


class _ns_msg_t(ctypes.Structure):
    _fields_ = (
        # Partially opaque data. Seen as 80 bytes in glibc6-2.27.
        ('_msg', ctypes.POINTER(ctypes.c_ubyte)),
        ('_eom', ctypes.POINTER(ctypes.c_ubyte)),
        ('_id', ctypes.c_uint16),
        ('_flags', ctypes.c_uint16),
        ('_counts', ctypes.c_uint16 * ns_sect.ns_s_max),
        ('_sections', ctypes.POINTER(ctypes.c_ubyte) * ns_sect.ns_s_max),
        ('_sect', ctypes.c_uint),  # ns_sect enum
        ('_rrnum', ctypes.c_uint),
        ('_msg_ptr', ctypes.POINTER(ctypes.c_ubyte)),
    )

    def ns_msg_base(self):
        return self._msg

    def ns_msg_end(self):
        return self._eom

    def ns_msg_count(self, section):
        return self._counts[section]


class _ns_rr_t(ctypes.Structure):
    _fields_ = (
        ('name', ctypes.c_byte * NS_MAXDNAME),
        ('type', ctypes.c_uint16),
        ('rr_class', ctypes.c_uint16),
        ('ttl', ctypes.c_uint32),
        ('rdlength', ctypes.c_uint16),
        ('rdata', ctypes.POINTER(ctypes.c_ubyte)),
    )

    def ns_rr_name(self):
        return ('.' if self.name[0] == '\x00' else self.name)

    def ns_rr_class(self):
        return self.rr_class

    def ns_rr_type(self):
        return ns_type(self.type) if IntEnum != object else self.type

    def ns_rr_rdata(self):
        return self.rdata

    def ns_rr_rdata__offset(self, offset):
        return ctypes.byref(self.rdata.contents, offset)

    def ns_rr_rdata__human(self):
        return repr(bytearray(self.rdata[0:self.rdlength]))


def res_query(dname, class_=ns_class.ns_c_in, rr_type=ns_type.ns_t_a):
    """
    int res_nquery(
            res_state statep, const char *dname, int class, int type,
            unsigned char *answer, int anslen);

    Example::

        answer = res_query('gmail.com', rr_type=ns_type.ns_t_mx)
        ret = ns_parse(answer, handler=ns_type.handle_mx)
    """
    answer = ctypes.create_string_buffer(NS_MAXMSG)
    anslen = _res_nquery(
        ctypes.byref(_GLOBAL_STATEP), dname.encode('utf-8'),
        class_, rr_type, answer, len(answer))
    if anslen < 0:
        raise ValueError('res_query returned {}'.format(anslen))
    return answer[0:anslen]


def ns_parse(answer, handler=ns_type.handle_invalid):
    """
    int ns_initparse(const u_char *msg, int msglen, ns_msg *handle)
    #define ns_msg_count(handle, section) ((handle)._counts[section] + 0)
    int ns_parserr(ns_msg *handle, ns_sect section, int rrnum, ns_rr *rr)

    Example::

        answer = res_query('gmail.com', rr_type=ns_type.ns_t_mx)
        ret = ns_parse(answer, handler=ns_type.handle_mx)
    """
    msg = _ns_msg_t()  # "handle"
    if _ns_initparse(answer, len(answer), ctypes.byref(msg)) != 0:
        raise ValueError('ns_initparse failed to parse buffer')

    count = msg.ns_msg_count(ns_sect.ns_s_an)  # answer count
    retlist = []
    for rrnum in range(count):
        rr = _ns_rr_t()
        if _ns_parserr(
                ctypes.byref(msg), ns_sect.ns_s_an, rrnum,
                ctypes.byref(rr)) != 0:
            # Parse failure..?
            continue

        ret = handler(msg, rr)
        if ret:
            retlist.append(ret)

    return retlist


_GLOBAL_STATEP = _res_state_t()
if _res_ninit(ctypes.byref(_GLOBAL_STATEP)) != 0:
    # Initialize a single global state variable. Probably not thread
    # safe like this, but we're not using MT right now anyway.
    raise ValueError('Failure during res_ninit')


if __name__ == '__main__':
    answer = res_query('gmail.com', rr_type=ns_type.ns_t_a)
    ret = ns_parse(answer)
    print(ret)

    answer = res_query('gmail.com', rr_type=ns_type.ns_t_mx)
    ret = ns_parse(answer, handler=ns_type.handle_mx)
    print(ret)
