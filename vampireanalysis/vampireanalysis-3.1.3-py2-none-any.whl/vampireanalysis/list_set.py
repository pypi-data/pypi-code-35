#!/usr/bin/env python

# built-in libraries
import os
from time import sleep
# external libraries
import pandas as pd
import numpy as np

def modeling_ledger(exp):
	d= {'condition': [],
		'set number':[],
		'set location':[],
		'note':[],
		'ch1':[],
		'ch2':[]}	
	emptycsv_df = pd.DataFrame(data=d)
	emptycsv_df = emptycsv_df[['condition','set number','set location','note','ch1','ch2']]
	emptycsv_dst1 = os.path.join(exp,'image sets to build model.csv')
	emptycsv_dst2 = os.path.join(exp,'image sets to apply model.csv')
	emptycsv_df.to_csv(emptycsv_dst1, index=False)
	emptycsv_df.to_csv(emptycsv_dst2, index=False)

def list_set(folder): #folder == cpoutput folder
	folder = os.path.abspath(folder)
	setfolders = [_ for _ in os.listdir(folder) if os.path.isdir(os.path.join(folder,_))]
	setfolderpaths = [os.path.join(folder,_) for _ in setfolders]
	exp = os.path.split(os.path.split(folder)[0])[0]
	expname = [os.path.split(os.path.split(folder)[0])[1]]*len(setfolders)
	d= {'condition': expname,
		'set number':setfolders,
		'set location':setfolderpaths,
		'note':['None']*len(setfolders),
		'ch1':['ch1']*len(setfolders),
		'ch2':['ch2']*len(setfolders)}	
	dd = dict([ (k,pd.Series(v)) for k,v in d.items()])
	df = pd.DataFrame(data=dd)
	df = df[['condition','set number','set location','note','ch1','ch2']]
	df.to_csv(os.path.join(folder , 'segmented image set location.csv'), index=False)

	if not os.path.exists(os.path.join(exp,'image sets for building model.csv')):
		modeling_ledger(exp)

# list_set('C:\\Users\\kuki\\Desktop\\cpoutput315\\Experiment1\\labeled image')