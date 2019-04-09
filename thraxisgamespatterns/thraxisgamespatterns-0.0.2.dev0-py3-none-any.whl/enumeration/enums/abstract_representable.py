# package com.games.thraxis.framework.enumeration.enums;
#
# import java.io.Serializable;
#
# /##
#  # Created by Zack on 9/21/2017.
#  #/
#
# public interface TGRepresentable extends Serializable {
#
# 	String getCode();
#
# }
from abc import ABC, abstractmethod


class TGAbstractRepresentable(ABC):
    @abstractmethod
    def get_code(self):
        pass
