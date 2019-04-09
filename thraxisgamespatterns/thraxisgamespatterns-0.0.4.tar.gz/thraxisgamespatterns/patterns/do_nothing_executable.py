# package com.games.thraxis.framework.patterns;
#
# /##
#  # Created by Zack on 9/25/2017.
#  #/
#
# public class TGDoNothingExecutable implements TGExecutable {
#
# 	public static final TGDoNothingExecutable DEFAULT = new TGDoNothingExecutable();
#
# 	private TGDoNothingExecutable() {
# 	}
#
# 	@Override
# 	public void execute() {
# 		//Do nothing
# 	}
# }
from patterns.abstract_executable import TGAbstractExecutable


class TGDoNothingExecutable(TGAbstractExecutable):

    def execute(self):
        # Do nothing.
        pass


DEFAULT = TGDoNothingExecutable()
