import pandas as pd
import os
import cv2
import numpy as np
from time import sleep
import re

csvpath = 'C:/Users/kuki/Desktop/corrected_v3_cp/Experiment1/segmented images/1/Cells_object_ledger.csv'
csv = pd.read_csv(csvpath)
X = csv['X']
Y = csv['Y']
filename = csv['Filename']
uniquename = list(set(filename))
uniquename.sort()

cellpath = 'C:/Users/kuki/Desktop/mp sample v3/image set 1/'
savepath = 'C:/Users/kuki/Desktop/mp sample v3/image set 1/cropped'
if not os.path.isdir(savepath):
	os.mkdir(savepath)
imlist = [_ for _ in os.listdir(cellpath) if 'c1' in _]

for idx, elem in enumerate(uniquename):
	x = X.loc[filename == uniquename[idx]].values 
	y = Y.loc[filename == uniquename[idx]].values 
	keyword = re.search('1_(.+?).tiff', elem).group(1)
	img = cv2.imread(os.path.join(cellpath,'xy'+keyword+'c1.tif'))
	for xcoordidx, xcoord in enumerate(x):
		crop_img = img[ y[xcoordidx]-50:y[xcoordidx]+50, xcoord-50:xcoord+50 ]
		cv2.imwrite(os.path.join(savepath,elem[0:-5]+'_'+str(xcoord)+'_'+str(y[xcoordidx])+'.jpg'),crop_img)
