#!/usr/bin/env python

# built-in libraries
import os
from time import sleep
import re
from Tkinter import END
# external libraries
from PIL import Image
from scipy.ndimage.measurements import center_of_mass, label
from scipy.ndimage import generate_binary_structure
import numpy as np
import cv2
import pandas as pd
from skimage import measure

def createimstack(ch,setfolder):
	imlist = [_ for _ in os.listdir(setfolder) if _.lower().endswith('.tiff')]
	imlist = [_ for _ in imlist if ch.lower() in _.lower()] 
	#imlist.sort(key=lambda f: int(filter(str.isdigit,f)))
	imlist = sorted(imlist)
	imlistpath = [os.path.join(setfolder,_) for _ in imlist]
	imstack = [np.array(Image.open(im)) for im in imlistpath]
	return imstack,imlistpath,imlist

def check_label_status(im):
	if len(list(set(im.flatten()))[1:])>1: return 'labeled' 

def mask2boundary(mask):
	contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	contour = np.empty(2)
	for i in range(len(contours[0])):
		contour = np.vstack((contours[0][i][0],contour))
	contour=contour[0:-1]
	contour.T[0] = contour.T[0]+1
	contour.T[1] = contour.T[1]+1
	boundary = np.empty((2,len(contour.T[1])))
	boundary[0] = contour.T[1]
	boundary[1] = contour.T[0]
	boundary = boundary.T.astype(int)
	return boundary

def getboundary(csv,progress_bar,entries):
	UI = pd.read_csv(csv)
	setpaths = UI['set location']
	for setfolderidx, setfolder in enumerate(setpaths):
		progress_bar["value"] = 100*setfolderidx/len(setpaths)  
		progress_bar.update()										
		ch1= UI['ch1'][setfolderidx]
		ch2= UI['ch2'][setfolderidx]
		for ch in [ch1,ch2]:
			imstack,imlistpath,imlist = createimstack(ch,setfolder)
			try: 
				inputim = check_label_status(imstack[0]) #intensity label in greyscale
			except:
				entries['Status'].delete(0,END)
				entries['Status'].insert(0,'The channel columns in the segmented image set location.csv need to be updated')
				return
			if inputim is not 'labeled':
				s = generate_binary_structure(2,2)
				imstack = [label(im,structure=s)[0] for im in imstack]
			registry=[]
			registry_dst = os.path.join(setfolder,ch+'_centroid.pickle')
			boundarymaster=[]
			boundarydst = os.path.join(setfolder,ch+'_boundary_coordinate_stack.pickle')
			if os.path.exists(boundarydst): continue
			if os.path.exists(registry_dst): continue
			for imidx, im in enumerate(imstack):
				labels = list(set(im.flatten()))[1:]
				for objidx,lab in enumerate(labels):
					mask = np.array((im==lab).astype(int),dtype='uint8')
					centroid = [int(np.around(_,0)) for _ in center_of_mass(mask)]
					centroid.reverse() # swap to correct x,y
					prop = measure.regionprops(mask,coordinates='rc')[0]
					area = prop['area']
					perimeter= prop['perimeter']
					majoraxis = prop['major_axis_length']
					minoraxis = prop['minor_axis_length']
					circularity = 4*np.pi*area/ perimeter**2
					AR = majoraxis/minoraxis
					props = [area,perimeter,majoraxis,minoraxis,circularity,AR]
					fronttag = [imlist[imidx],imidx+1,objidx+1]
					registry_item = fronttag + centroid +  props
					boundary = mask2boundary(mask)
					if len(boundary)<10:
						print 'len is too low'
						continue
					registry.append(registry_item)
					boundarymaster.append(boundary)
			if not os.path.exists(boundarydst):
				df = pd.DataFrame(boundarymaster)
				df.to_pickle(boundarydst)
			if not os.path.exists(registry_dst):
				df_registry = pd.DataFrame(registry)
				df_registry.columns = ['Filename','ImageID','ObjectID','X','Y','Area','Perimeter','Major Axis','Minor Axis','Circularity','Aspect Ratio']
				df_registry.index = df_registry.index+1
				df_registry.to_csv(os.path.join(setfolder,ch+'_registry.csv'))
	entries['Status'].delete(0,END)
	entries['Status'].insert(0,'object csv created...')
	return

