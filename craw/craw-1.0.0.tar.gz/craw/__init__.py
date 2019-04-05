###########################################################################
#                                                                         #
# This file is part of Counter RNAseq Window (craw) package.              #
#                                                                         #
#    Authors: Bertrand Neron                                              #
#    Copyright (c) 2017-2019  Institut Pasteur (Paris).                   #
#    see COPYRIGHT file for details.                                      #
#                                                                         #
#    craw is free software: you can redistribute it and/or modify         #
#    it under the terms of the GNU General Public License as published by #
#    the Free Software Foundation, either version 3 of the License, or    #
#    (at your option) any later version.                                  #
#                                                                         #
#    craw is distributed in the hope that it will be useful,              #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of       #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.                 #
#    See the GNU General Public License for more details.                 #
#                                                                         #
#    You should have received a copy of the GNU General Public License    #
#    along with craw (see COPYING file).                                  #
#    If not, see <http://www.gnu.org/licenses/>.                          #
#                                                                         #
###########################################################################


import sys
import logging

__version__ = '1.0.0'


def get_version_message():
    """

    :return: A human readable version of the craw package version
    :rtype: string
    """
    version_text = "craw {0} | Python {1}.{2}".format(__version__,
                                                      sys.version_info.major,
                                                      sys.version_info.minor)
    return version_text


def init_logger(log_level, out=True):
    """
    Initiate the "root" logger for craw library
    all logger create in craw package inherits from this root logger
    This logger write logs on sys.stderr
    
    :param log_level: the level of the logger 
    :type log_level: int 
    """
    craw_log = logging.getLogger('craw')
    if out:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(fmt='{levelname} : {name} : {message}', style='{')
        handler.setFormatter(formatter)
        craw_log.addHandler(handler)
    else:
        null_handler = logging.NullHandler()
        craw_log.addHandler(null_handler)
    craw_log.setLevel(log_level)
    craw_log.propagate = False
