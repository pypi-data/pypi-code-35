# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, unicode_literals

import re

import pyparsing as pp
import simplejson as json
import typepy

from .._const import Tc, TcSubCommand
from .._logger import logger
from ._interface import AbstractParser


class TcQdiscParser(AbstractParser):
    __RE_DIRECT_QLEN = re.compile("direct_qlen (?P<number>[0-9]+)")

    @property
    def _tc_subcommand(self):
        return TcSubCommand.QDISC.value

    def __init__(self, con):
        super(TcQdiscParser, self).__init__()

        self.__con = con

    def __parse_direct_qlen(self, line):
        m = self.__RE_DIRECT_QLEN.search(line)
        if m is None:
            return

        self.__parsed_param["direct_qlen"] = int(m.group("number"))

    def parse(self, device, text):
        self._clear()

        if typepy.is_null_string(text):
            return []

        text = text.strip()
        entry_list = []

        for line in text.splitlines():
            if typepy.is_null_string(line):
                continue

            line = self._to_unicode(line.lstrip())

            if re.search("^qdisc netem |^qdisc htb |^qdisc tbf ", line) is None:
                continue

            if re.search("^qdisc htb ", line) is not None:
                self.__parse_direct_qlen(line)
                continue

            if re.search("^qdisc netem ", line) is not None:
                self.__parse_netem_param(line, "parent", pp.hexnums + ":")

            self.__parsed_param[Tc.Param.DEVICE] = device
            self.__parse_netem_param(line, "netem", pp.hexnums + ":", "handle")
            self.__parse_netem_param(line, "delay", pp.nums + ".msu")
            self.__parse_netem_delay_distro(line)
            self.__parse_netem_param(line, "loss", pp.nums + ".%")
            self.__parse_netem_param(line, "duplicate", pp.nums + ".%")
            self.__parse_netem_param(line, "corrupt", pp.nums + ".%")
            self.__parse_netem_param(line, "reorder", pp.nums + ".%")
            self.__parse_bandwidth_rate(line)

            logger.debug("parse a qdisc entry: {}".format(self.__parsed_param))

            entry_list.append(self.__parsed_param)

            self._clear()

        if entry_list:
            self.__con.create_table_from_data_matrix(
                self._tc_subcommand,
                [
                    Tc.Param.DEVICE,
                    "parent",
                    "handle",
                    "delay",
                    "delay-distro",
                    "loss",
                    "duplicate",
                    "corrupt",
                    "reorder",
                    "rate",
                ],
                entry_list,
            )

        logger.debug(
            "tc {:s} parse result: {}".format(self._tc_subcommand, json.dumps(entry_list, indent=4))
        )

        return entry_list

    def _clear(self):
        self.__parsed_param = {}

    def __parse_netem_delay_distro(self, line):
        parse_param_name = "delay"
        pattern = (
            pp.SkipTo(parse_param_name, include=True)
            + pp.Word(pp.nums + ".msu")
            + pp.Word(pp.nums + ".msu")
        )

        try:
            parsed_list = pattern.parseString(line)
            self.__parsed_param[parse_param_name] = parsed_list[2]
            self.__parsed_param["delay-distro"] = parsed_list[3]
        except pp.ParseException:
            pass

    def __parse_netem_param(self, line, parse_param_name, word_pattern, key_name=None):
        pattern = pp.SkipTo(parse_param_name, include=True) + pp.Word(word_pattern)
        if not key_name:
            key_name = parse_param_name

        try:
            result = pattern.parseString(line)[-1]
            if typepy.is_not_null_string(result):
                self.__parsed_param[key_name] = result
        except pp.ParseException:
            pass

    def __parse_bandwidth_rate(self, line):
        parse_param_name = "rate"
        pattern = pp.SkipTo(parse_param_name, include=True) + pp.Word(pp.alphanums + "." + ":")

        try:
            result = pattern.parseString(line)[-1]
            if typepy.is_not_null_string(result):
                result = result.rstrip("bit")
                self.__parsed_param[parse_param_name] = result
        except pp.ParseException:
            pass
