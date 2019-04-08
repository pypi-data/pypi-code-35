#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from croniter import croniter

class InquirerValidation:

    @staticmethod
    def check_cron(_, candidate):
        return croniter.is_valid(candidate)


    @staticmethod
    def check_int(_, candidate):
        try:
            int(candidate)
            return True
        except:
            return False

    @staticmethod
    def get_dict_from_args(args):

        d = {}
        if args:
            for k,v in [p.strip().split('=') for p in args.split(',')]:
                d[k] = v

        return d
