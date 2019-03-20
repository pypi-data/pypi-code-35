#!/usr/bin/env python

# built-in libraries
from time import sleep
import os
import re
# external libraries
import numpy as np 
from PIL import Image

def sum_binary(entries,experiment,progress_bar):
	labeledimfolder = os.path.join(experiment,'segmented images')
	setfolders = [_ for _ in os.listdir(experiment) if (os.path.isdir(os.path.join(experiment,_)) and _ != 'segmented images')]
	setfolderpaths = [os.path.join(experiment,_) for _ in setfolders]
	progress = 0
	for setidx, setid in enumerate(setfolderpaths):
		imfolders = [_ for _ in os.listdir(setid) if os.path.isdir(os.path.join(setid,_))]
		imfolders.sort(key=lambda f: int(filter(str.isdigit,f)))
		imfolderpaths = [os.path.join(setid,_) for _ in imfolders]
		for imidx,imid in enumerate(imfolderpaths):
			masks = [_ for _ in os.listdir(imid) if _.lower().endswith('.tiff')]
			#maskpaths = [os.path.join(imid,_) for _ in masks]
			objectname = list(set([re.split('_+',_)[0] for _ in masks])) # [cell, nuclei]
			## objectname is very limited by re.split. The objectname is something infront of _
			## but this is okay for cell profiler usage.
			for objidx, obj in enumerate(objectname):
				progress = progress + int( (100/len(setfolderpaths)/len(imfolderpaths))*objidx/len(objectname) )
				progress_bar["value"] = progress
				progress_bar.update()
				objs = [_ for _ in masks if obj in _]
				objpaths = [os.path.join(imid,_) for _ in objs]
				for idx, im in enumerate(objpaths):
					addim = np.asarray(Image.open(im))  
					addim = addim.copy()
					addim[addim>0] = idx
					if idx == 0: ims = 0
					ims = addim + ims
				labeledim = Image.fromarray((ims).astype('uint16'))
				labeledsetfolder = os.path.join(labeledimfolder,os.path.basename(setid))
				if not os.path.isdir(labeledsetfolder):
					os.mkdir(labeledsetfolder)
				dst = os.path.join(labeledsetfolder, obj+'_'+setfolders[setidx]+'_'+imfolders[imidx])
				labeledim.save(dst+'.tiff')
#sum_binary('/Users/jacquelinekumer/Desktop/cpoutput315/Experiment1')			
# sum_binary('C:\\Users\\kuki\\Desktop\\cpoutput315\\Experiment1')	

