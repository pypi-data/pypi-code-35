#!/usr/bin/env python

# built-in libraries
import os
import pickle
import random
from time import sleep
from Tkinter import END
# external libraries
import pandas as pd
import numpy as np
# my wrapper
from collect_selected_bstack import *
from recordIDX import *
# my core
from bdreg import *
from pca_bdreg import *
from clusterSM import *

def main(BuildModel,csv,entries,modelname,clnum=None,progress_bar=None):
	print('## main.py')
	figdst = os.path.join(os.path.dirname(csv),modelname)
	if BuildModel:
		ch1,ch2 = collect_seleced_bstack(csv,BuildModel)

		VamModel = {
		"N":[],
		"bdrn":[],
		"mdd":[],
		"sdd":[],
		"pc":[],
		"latent":[],
		"clnum":[],
		"pcnum":[],
		"mincms":[],
		"testmean":[],
		"teststd":[],
		"boxcoxlambda":[],
		"C":[],
		"Z":[]
		}
		N = None

		ch = 'ch1'
		progress_bar["value"] = 10
		progress_bar.update()
		bdpc, bnreg, sc, VamModel = bdreg_main(ch1,N,VamModel,BuildModel)
		progress_bar["value"] = 20
		progress_bar.update()
		pc , score, latent, VamModel = pca_bdreg_main(bdpc,VamModel,BuildModel,ch)
		progress_bar["value"] = 30
		progress_bar.update()
		pcnum=None
		IDX,bdsubtype,C,VamModel = cluster_main(csv,modelname,score,pc,bdpc,clnum,pcnum,VamModel,BuildModel,ch,None,entries)
		progress_bar["value"] = 40
		progress_bar.update()
		if not os.path.exists(os.path.join(figdst,'model storage')):
			os.mkdir(os.path.join(figdst,'model storage'))
		if os.path.exists(os.path.join(os.path.join(figdst,'model storage'),modelname+'_ch1.pickle')):
			f=open(os.path.join(os.path.join(figdst,'model storage'),modelname + str(random.randint(0,100)) +'_ch1.pickle'),'wb')
			pickle.dump(VamModel,f)
			f.close()
		else:
			f=open(os.path.join(os.path.join(figdst,'model storage'),modelname+'_ch1.pickle'),'wb')
			pickle.dump(VamModel,f)
			f.close()
		progress_bar["value"] = 45
		progress_bar.update()
		#result = recordIDX(IDX,BuildModel,csv,ch)
		progress_bar["value"] = 50
		progress_bar.update() 

		ch = 'ch2'
		progress_bar["value"] = 55
		progress_bar.update()
		bdpc, bnreg, sc, VamModel = bdreg_main(ch2,N,VamModel,BuildModel)
		progress_bar["value"] = 60
		progress_bar.update()
		pc , score, latent, VamModel = pca_bdreg_main(bdpc,VamModel,BuildModel,ch)
		progress_bar["value"] = 70
		progress_bar.update()
		pcnum=None
		IDX,bdsubtype,C,VamModel = cluster_main(csv,modelname,score,pc,bdpc,clnum,pcnum,VamModel,BuildModel,ch,None,entries)
		progress_bar["value"] = 80
		progress_bar.update()

		if os.path.exists(os.path.join(os.path.join(figdst,'model storage'),modelname+'_ch2.pickle')):
			f=open(os.path.join(os.path.join(figdst,'model storage'),modelname + str(random.randint(0,100)) +'_nuclei.pickle'),'wb')
			pickle.dump(VamModel,f)
			f.close()
		else:
			f=open(os.path.join(os.path.join(figdst,'model storage'),modelname+'_ch2.pickle'),'wb')
			pickle.dump(VamModel,f)
			f.close()

		progress_bar["value"] = 90
		progress_bar.update()

		#result = recordIDX(IDX,BuildModel,csv,ch)
		progress_bar["value"] = 95
		progress_bar.update() 

	else:
		model_list = [os.path.abspath(os.path.join(modelname,_)) for _ in os.listdir(modelname) if _.lower().endswith('pickle')]
		UI = pd.read_csv(csv)
		setpaths = UI['set location']
		ch1ui= UI['ch1']
		ch2ui= UI['ch2']    
		condition = UI['condition']

		for setidx, setpath in enumerate(setpaths):
			pickles = [_ for _ in os.listdir(setpath) if _.lower().endswith('pickle')]

			c1_stack = [pd.read_pickle(os.path.join(setpath,pkl)) for pkl in pickles if ch1ui[setidx] in pkl]
			c2_stack = [pd.read_pickle(os.path.join(setpath,pkl)) for pkl in pickles if ch2ui[setidx] in pkl]
			
			ch1 = pd.concat(c1_stack,ignore_index=True)
			ch2 = pd.concat(c2_stack,ignore_index=True)

			progress_bar["value"] = 10
			progress_bar.update()

			try:
				f=open(model_list[0],'r')
			except:
				entries['Status'].delete(0,END) #global name END is not defined
				entries['Status'].insert(0,'the model does not exist. please replace model name to the one you built')
			VamModel = pickle.load(f)

			N = VamModel['N'] 
			ch = 'ch1'

			progress_bar["value"] = 20
			progress_bar.update()
			bdpc_new, bnreg_new, sc_new, VamModel = bdreg_main(ch1,N,VamModel,BuildModel)
			progress_bar["value"] = 30
			progress_bar.update()
			pc_new, score_new, latent_new, VamModel = pca_bdreg_main(bdpc_new,VamModel,BuildModel,ch)
			progress_bar["value"] = 40
			progress_bar.update()
			# if clnum != VamModel['clnum']:
			# 	raise NameError('Number of eigen-shape should remain same. To change the number, rebuild the model with the new number first')
			clnum=VamModel['clnum']
			pcnum=VamModel['pcnum']
			#pc_new goes in for sake of placing, but pc from the model is used in cluster_main
			IDX_new,bdsubtype_new,C_new,VamModel = cluster_main(csv,modelname,score_new,pc_new,bdpc_new,clnum,pcnum,VamModel,BuildModel,ch,condition[setidx],entries)
			progress_bar["value"] = 50
			progress_bar.update()

			
			result = recordIDX(IDX_new,BuildModel,csv,ch)

			try:
				f=open(model_list[1],'r')
			except:
				entries['Status'].delete(0,END)
				entries['Status'].insert(0,'Please use exact name of the model you have built to apply here')
			VamModel = pickle.load(f)

			N = VamModel['N'] 
			ch = 'ch2'
			progress_bar["value"] = 60
			progress_bar.update()
			bdpc_new, bnreg_new, sc_new, VamModel = bdreg_main(ch2,N,VamModel,BuildModel)
			progress_bar["value"] = 70
			progress_bar.update()
			pc_new, score_new, latent_new, VamModel = pca_bdreg_main(bdpc_new,VamModel,BuildModel,ch)
			progress_bar["value"] = 80
			progress_bar.update()
			clnum=VamModel['clnum']
			pcnum=VamModel['pcnum']
			#pc_new goes in for sake of placing, but pc from the model is used in cluster_main
			IDX_new,bdsubtype_new,C_new,VamModel = cluster_main(csv,modelname,score_new,pc_new,bdpc_new,clnum,pcnum,VamModel,BuildModel,ch,condition[setidx],entries)
			progress_bar["value"] = 90
			progress_bar.update()

			result = recordIDX(IDX_new,BuildModel,csv,ch)

		entries['Status'].delete(0,END)
		entries['Status'].insert(0,'applied the model')

