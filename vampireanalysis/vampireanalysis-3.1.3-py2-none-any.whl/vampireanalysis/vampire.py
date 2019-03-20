#!/usr/bin/env python

# internal libraries
import os
from time import sleep
# interface libraries
from Tkinter import *
from ttk import *
import tkFileDialog as fd
# my files
from main import main
from getboundary import getboundary
from list_set import list_set
from sum_binary import sum_binary

def makeform(root, fields):
	entries = {}
	rows= []
	for field in fields:
		row = Frame(root)
		row.pack(side=TOP, fill=X, padx=5, pady=5)
		if  field =='Merge CellProfiler Segmented Objects' or field == 'Build Model' or field =='' or field == 'Apply Model': 
			lab = Label(row, width=30, text=field, anchor='w',font=("Helvetica", 16))
			lab.pack(side=LEFT)
		else:
			ent = Entry(row)
			if field == 'Number of eigen-shapes':
				ent.insert(0,"choose a number")
			elif field == 'Status':
				ent.insert(0,'welcome to the vampire analysis')
			elif field == 'Name of the model':
				ent.insert(0,'name your model')
			elif field == 'Image sets for building' or field == 'Image sets for applying' or field == 'List of segmented images':
				ent.insert(0,'<--- click to load csv')
			elif field == 'Model to apply':
				ent.insert(0,'<--- click to load model')
			else:ent.insert(0,"<--- click to search folder")
			ent.pack(side=RIGHT, expand=YES, fill=X)
			entries[field] = ent
			lab = Label(row, width=24, text=field, anchor='w')
			lab.pack(side=LEFT)
		rows.append(row)
	return entries,rows

def getdir(entries,target):
	entries['Status'].delete(0,END)
	entries['Status'].insert(0,'searching...')
	#################################################################
	folder = StringVar()
	foldername = fd.askdirectory()
	folder.set(foldername)
	folder = folder.get()
	entries[target].delete(0,END)
	entries[target].insert(0,folder)
	#################################################################
	entries['Status'].delete(0,END)
	entries['Status'].insert(0,'directory found...')

def getcsv(entries,target):
	entries['Status'].delete(0,END)
	entries['Status'].insert(0,'searching...')
	#################################################################
	folder = StringVar()
	foldername = fd.askopenfilename()
	folder.set(foldername)
	folder = folder.get()
	entries[target].delete(0,END)
	entries[target].insert(0,folder)
	#################################################################
	entries['Status'].delete(0,END)
	entries['Status'].insert(0,'directory found...')

def merge(entries,progress_bar):
	entries['Status'].delete(0,END)
	entries['Status'].insert(0,'merging...')
	#################################################################
	CPsubfolder = entries['Locate CellProfiler objects'].get() 
	CPsubfolder = os.path.abspath(CPsubfolder)
	# 'C:\\Users\\kuki\\Desktop\\cpoutput315\\Experiment1'
	labeledimfolder = os.path.join(CPsubfolder,'segmented images')
	if not os.path.isdir(labeledimfolder):
		os.mkdir(labeledimfolder)
		sum_binary(entries,CPsubfolder,progress_bar)
	#################################################################
	folder = os.path.join(CPsubfolder,'segmented images')
	list_set(folder)
	progress_bar["value"] = 100
	progress_bar.update()
	entries['Status'].delete(0,END)
	entries['Status'].insert(0,'merging completed...')

# def createobjectlist(entries,progress_bar):
# 	entries['Status'].delete(0,END)
# 	entries['Status'].insert(0,'creating object csv...')
# 	#################################################################
# 	# input definition
# 	folder = entries['List of segmented images'].get()
# 	# function
# 	folder = os.path.dirname(folder)
# 	getboundary(folder,progress_bar,entries)
# 	#################################################################
# 	progress_bar["value"] = 100
# 	progress_bar.update()
	

def Model(entries,BuildModel,progress_bar):
	entries['Status'].delete(0,END)
	entries['Status'].insert(0,'modeling initiated...')
	#################################################################
	# input definition
	if BuildModel == True:
		csv = entries['Image sets for building'].get() 
		clnum = entries['Number of eigen-shapes'].get()
		modelname = entries['Name of the model'].get() #name
	else:
		csv = entries['Image sets for applying'].get()
		modelname = entries['Model to apply'].get()  #path
		clnum=None 
	# function
	# folder = os.path.dirname(folder)
	getboundary(csv,progress_bar,entries)
	main(BuildModel,csv,entries,modelname,clnum,progress_bar)
	#################################################################
	progress_bar["value"] = 100
	progress_bar.update()
	entries['Status'].delete(0,END)
	entries['Status'].insert(0,'modeling completed...')

def vampire(): 
	root = Tk()
	root.style = Style()
	root.style.theme_use('clam')
	root.configure(background='#dcdad5')
	root.style.configure("red.Horizontal.TProgressbar", troughcolor ='gray',  background='#EA6676')
	root.title("Vampire Analysis")
	fields = ('Merge CellProfiler Segmented Objects','Locate CellProfiler objects','', #merge button
		'Build Model','Image sets for building', 'Number of eigen-shapes','Name of the model','', #build model button
		'Apply Model','Image sets for applying','Model to apply','','Status','')
	ents,rows = makeform(root, fields)
	root.bind('<Return>', (lambda event, e=ents: fetch(e))) 
	#####################################################################################################################
	progress_bar = Progressbar(rows[13], style="red.Horizontal.TProgressbar", orient="horizontal", mode="determinate",maximum=100)
	progress_bar.pack(side=RIGHT,padx=5,pady=5)
	#####################################################################################################################
	#function 1 : merge
	b1 = Button(rows[1],text='search folder', width=12,command=(lambda e=ents: getdir(e,'Locate CellProfiler objects')))
	b1.pack(side=RIGHT,padx=5,pady=5)
	#function 2
	#csvgen = BooleanVar()
	# checkb = Checkbutton(rows[2],text='create list of image sets',variable=csvgen)
	b2 = Button(rows[2],text='merge', width=6,command=(lambda e=ents: merge(e,progress_bar)))
	b2.pack(side=RIGHT,padx=5,pady=5)
	# checkb.pack(side=RIGHT,padx=5,pady=5)
	#####################################################################################################################
	# #function 3 : create csv
	# b3 = Button(rows[4],text='load csv', width=12,command=(lambda e=ents: getcsv(e,'List of segmented images')))
	# b3.pack(side=RIGHT,padx=5,pady=5)
	# #function 4_1 : create image csv
	# b4 = Button(rows[5],text='create',width=6,command=(lambda e=ents: createobjectlist(e,progress_bar)))
	# b4.pack(side=RIGHT,padx=5,pady=5)
	#####################################################################################################################
	#function 5 : Model 
	b5 = Button(rows[4],text='load csv', width=12,command=(lambda e=ents: getcsv(e,'Image sets for building')))
	b5.pack(side=RIGHT,padx=5,pady=5)
	#function 6
	b6 = Button(rows[7],text='build model',width=12,command=(lambda e=ents: Model(e,True,progress_bar)))
	b6.pack(side=RIGHT,padx=5,pady=5)
	#function 7
	b7 = Button(rows[9],text='load csv', width=12,command=(lambda e=ents: getcsv(e,'Image sets for applying')))
	b7.pack(side=RIGHT,padx=5,pady=5)
	#function 8
	b8 = Button(rows[10],text='load model', width=12,command=(lambda e=ents: getdir(e,'Model to apply')))
	b8.pack(side=RIGHT,padx=5,pady=5)
	#function 9
	b9 = Button(rows[11],text='apply model',width=12,command=(lambda e=ents: Model(e,False,progress_bar)))
	b9.pack(side=RIGHT,padx=5,pady=5)
	#####################################################################################################################
	#terminate
	quit = Button(root, text='Quit',width=6, command=root.quit)
	quit.pack(side=LEFT, padx=5, pady=5)
	root.mainloop()

vampire()