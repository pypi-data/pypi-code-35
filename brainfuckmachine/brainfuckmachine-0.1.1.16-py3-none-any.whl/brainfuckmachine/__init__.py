#!/usr/bin/env python3
import sys
import hy
hy.eval(hy.read_str(open(sys.prefix+"/lib_brainfuckmachine.hy","r+").read())) # wtf knows but it should be in one piece
