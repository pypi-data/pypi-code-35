# package com.games.thraxis.framework.patterns;
#
# /##
#  # Created by Zack on 9/25/2017.
#  #/
#
# public interface TGExecutable {
#
# 	void execute();
# }

from abc import ABC, abstractmethod


class TGAbstractExecutable(ABC):

    @abstractmethod
    def execute(self):
        pass
