#!/usr/bin/env python

# built-in libraries
import os
from time import sleep
# external libraries
import pandas as pd
import numpy as np

def collect_seleced_bstack(csv,buildmodel):
	print('## collect_selected_bstack.py')
	if buildmodel:
		UI = pd.read_csv(csv)
		setpaths = UI['set location']
		ch1= UI['ch1']
		ch2= UI['ch2']
		c1_stacks = []
		c2_stacks = []
		for setidx, setpath in enumerate(setpaths):
			pickles = [_ for _ in os.listdir(setpath) if _.lower().endswith('pickle')]
			c1_stack = [pd.read_pickle(os.path.join(setpath,pkl)) for pkl in pickles if ch1[setidx] in pkl]
			c2_stack = [pd.read_pickle(os.path.join(setpath,pkl)) for pkl in pickles if ch2[setidx] in pkl]
			c1_stacks = c1_stacks + c1_stack
			c2_stacks = c2_stacks + c2_stack

		df_c1 = pd.concat(c1_stacks,ignore_index=True)
		df_c2 = pd.concat(c2_stacks,ignore_index=True)
		return df_c1,df_c2

	else: 
		raise NameError('collect_seleced_bstack is only for buildmodel')
		return
