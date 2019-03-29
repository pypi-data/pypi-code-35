#!/usr/bin/python3
# coding: utf-8

from tkinter import *
from random import *
from PIL import Image
from PIL import ImageTk
import time
from math import ceil
import threading
import os,pkg_resources

class eniseboard():    
    def __init__(self,**kwargs):
        # lecture des arguments
        self.__hsize         = kwargs.pop('hsize',9)
        self.__vsize         = kwargs.pop('vsize',9)
        self.__cell          = kwargs.pop('cell',60)
        self.__grid          = kwargs.pop('grid',False)
        self.__special       = kwargs.pop('special','normal')
        self.__subgrid       = kwargs.pop('subgrid',False)
        self.__subon         = kwargs.pop('subon',self.__subgrid)
        self.__title         = kwargs.pop('title','Enise Board')
        self.__console       = kwargs.pop('console',False)
        self.__consolePlace  = kwargs.pop('consolePlace','down')
        self.__info          = kwargs.pop('info',False)
        self.__infoPlace     = kwargs.pop('infoPlace','top')
        self.__infoLines     = kwargs.pop('infoLines',2)
        self.__bgcolor       = kwargs.pop('bgcolor','ivory')
        self.__init          = kwargs.pop('init',lambda a:None)
        self.__click         = kwargs.pop('click',lambda a,b:None)
        self.__hover         = kwargs.pop('hover',lambda a,b:None)
        self.__key           = kwargs.pop('key',lambda a,b:None)
        # autres attributs
        self.__dir         = pkg_resources.resource_filename('eniseboard',
                                                             'demos/taquinimages/')
        self.__empty       = self.__dir+'empty.png'
        self.__images      = {}
        self.__subimages   = {}
        self.__bgimages    = {}
        self.__infoTexts   = {}
        self.__select      = []
        self.__hovernum    = -1
        self.__subhovernum = -1
        self.__defblinkcol = 'yellow'
        self.__font        = 'TkFixedFont 8 bold'
        self.__infoFont    = 'TkFixedFont 12 bold'
        self.__infoHeight  = 20
        self.__boarderr    = 2
        self.__animate     = []
        # la fenêtre
        self.__root       = Tk()
        self.__root.title(self.__title)
        # le canvas de jeu
        if self.__info:
            infozone = self.__infoLines*self.__infoHeight+2
        else:
            infozone = 0
        if self.__infoPlace=='top':
            self.__infoDec = infozone
        else:
            self.__infoDec = 0
        w = self.__boarderr+self.__cell*self.__hsize
        h = infozone + self.__boarderr+self.__cell*self.__vsize
        self.__board    = Canvas(self.__root,bg=self.__bgcolor,borderwidth=0,
                                    width=w,height=h,highlightthickness=0)
        self.__board.grid(row=0,column=0,padx=10,pady=10,
                            ipadx=self.__boarderr//2,ipady=self.__boarderr//2)
        # la console
        if self.__console:
            if self.__consolePlace=='down':
                self.__msg     = Frame(self.__root)
                self.__display = Text(self.__msg,width=20,height=4,
                                    font=self.__font,state=DISABLED)
                self.__display.grid(row=0,column=0,padx=0,pady=0,sticky=W+E)#
                scroll = Scrollbar(self.__msg,command=self.__display.yview,width=12)
                self.__display.configure(yscrollcommand=scroll.set)
                scroll.grid(row=0,column=1,padx=0,pady=1,ipadx=0,sticky=N+S)#
                self.__msg.grid(row=1,column=0,padx=10,pady=(0,10),sticky=W+E)
                self.__msg.columnconfigure(0,weight=1)
            elif self.__consolePlace=='right':
                self.__msg     = Frame(self.__root)
                self.__display = Text(self.__msg,width=20,height=4,
                                    font=self.__font,state=DISABLED)
                self.__display.grid(row=0,column=0,padx=0,pady=0,sticky=N+S)
                scroll = Scrollbar(self.__msg,command=self.__display.yview,width=8)
                self.__display.configure(yscrollcommand=scroll.set)
                scroll.grid(row=0,column=1,padx=0,pady=1,ipadx=2,sticky=S+N)
                self.__msg.grid(row=0,column=1,padx=(0,10),pady=(10,10),sticky=N+S)
                self.__msg.rowconfigure(0,weight=1)
        # les images de fonds de cellules
        image = self.__bgimage(self.__empty,0,0)
        self.__backgroundcells = [ [  self.__board.create_image(
                                self.__boarderr+(2*col+1)*self.__cell/2,
                                self.__infoDec+self.__boarderr+(2*row+1)*self.__cell/2,
                                image=image,
                                tag='backgroundcell') 
                            for col in range(self.__hsize) ] 
                            for row in range(self.__vsize) ]
        # les fonds de cellules
        self.__backgrounds = [[ self.__board.create_rectangle(
                        self.__boarderr+col*self.__cell,
                        self.__infoDec+self.__boarderr+row*self.__cell,
                        self.__boarderr+(col+1)*self.__cell,
                        self.__infoDec+self.__boarderr+(row+1)*self.__cell,
                        width=0,tag='background')
                for col in range(self.__hsize)]
                for row in range(self.__vsize)]
        # les fonds de sous cellules (subon=True)
        if self.__subon:
            self.__subbackgrounds = [[[ self.__board.create_rectangle(
                self.__boarderr+col*self.__cell+subcell%3*self.__cell//3,
                self.__infoDec+self.__boarderr+row*self.__cell+subcell//3*self.__cell//3,
                self.__boarderr+col*self.__cell+(subcell%3+1)*self.__cell//3,
                self.__infoDec+self.__boarderr+row*self.__cell+(subcell//3+1)*self.__cell//3,
                        width=0,tag='subbackground')
                for subcell in range(9)]
                for col in range(self.__hsize)]
                for row in range(self.__vsize)]
        # le quadrillage interne (subgrid=True)
        if self.__subgrid:
            # vertical
            for col in range(1,3*self.__hsize):
                if col%3!=0:
                    self.__board.create_line(self.__boarderr+col*self.__cell//3,
                                self.__infoDec+self.__boarderr+0,
                                self.__boarderr+col*self.__cell//3,
                                self.__infoDec+self.__boarderr+self.__vsize*self.__cell,
                                width=1,fill='grey80')
            # horizontal
            for row in range(1,3*self.__vsize):
                if row%3!=0:
                    self.__board.create_line(self.__boarderr+0,
                                self.__infoDec+self.__boarderr+row*self.__cell//3,
                                self.__boarderr+self.__hsize*self.__cell,
                                self.__infoDec+self.__boarderr+row*self.__cell//3,
                                width=1,fill='grey80')
        # le quadrillage principal (grid=True)
        if self.__grid:
            # vertical
            for col in range(1,self.__hsize):
                if col%3==0 and self.__special=='sudoku':
                    width=4
                else:
                    width=2
                self.__board.create_line(self.__boarderr+col*self.__cell,
                                self.__infoDec+self.__boarderr+0,
                                self.__boarderr+col*self.__cell,
                                self.__infoDec+self.__boarderr+self.__vsize*self.__cell,
                                width=width)
            # horizontal
            for row in range(1,self.__vsize):
                if row%3==0 and self.__special=='sudoku':
                    width=4
                else:
                    width=2
                self.__board.create_line(self.__boarderr+0,
                                self.__infoDec+self.__boarderr+row*self.__cell,
                                self.__boarderr+self.__hsize*self.__cell,
                                self.__infoDec+self.__boarderr+row*self.__cell,width=width)
        # les cellules
        image = self.__image(self.__empty,0,0)
        self.__cells = [ [  self.__board.create_image(
                                self.__boarderr+(2*col+1)*self.__cell/2,
                                self.__infoDec+self.__boarderr+(2*row+1)*self.__cell/2,
                                image=image,tag='cell') 
                            for col in range(self.__hsize) ] 
                            for row in range(self.__vsize) ]
        # les sous-cellules (subon=True)
        if self.__subon:
            name = os.path.splitext(os.path.basename(self.__empty))[0]
            self.__subimage(self.__empty,0,0)
            key  = str(0)+'-'+str(0)+'-'+name
            self.__subcells = [[ [  self.__board.create_image(  
                self.__boarderr+col*self.__cell+(subcell%3*2+1)*self.__cell//3//2,
                self.__infoDec+self.__boarderr+row*self.__cell+
                                        (subcell//3*2+1)*self.__cell//3//2,
                image=self.__subimages[key],
                tag='subcell')
                    for subcell in range(9) ] 
                    for col in range(self.__hsize) ] 
                    for row in range(self.__vsize) ]
        # callbacks
        self.__board.bind( '<Button>',   self.__boardclick )
        self.__board.bind( '<Motion>',   self.__boardmotion )
        self.__root.bind(  '<KeyPress>', self.__boardkey )
        # contournement d'un bug de dimensionnement de la fenêtre
        self.__root.update()
        self.__root.geometry(str(self.__root.winfo_reqwidth())+
                    'x'+str(self.__root.winfo_reqheight()))
        # appel du callback d'initialisation
        self.__init(self)
        # boucle d'événements
        self.__root.mainloop()
        
    def __boardclick(self,event):
        """ handler de l'événement tkinter <Button> """
        if not self.__animate:
            if (      self.__boarderr<=event.x<=self.__board.winfo_width() 
                and self.__infoDec+self.__boarderr<=event.y<=self.__board.winfo_height()  ):
                numcell = self.__numcell(event.x,event.y)
                info    =  {}
                info['row'] = self.__num2coords(numcell)[0]
                info['col'] = self.__num2coords(numcell)[1]
                if self.__subon:
                    info['subcell']=self.__subcell(event.x,event.y)
                self.__addmods(event.state,info)
                if event.num==1:
                    info['button1']=True
                elif event.num==3:
                    info['button3']=True
                else:
                    return
                self.__click(self,info) 

    def __boardmotion(self,event):
        """ handler de l'événement tkinter <Motion> """
        if not self.__animate:
            if (      self.__boarderr<=event.x<=self.__board.winfo_width() 
                and self.__infoDec+self.__boarderr<=event.y<=self.__board.winfo_height()  ):
                numcell = self.__numcell(event.x,event.y)
                oldnum  = self.__hovernum
                subcell = self.__subcell(event.x,event.y)
                oldsub  = self.__subhovernum
                if numcell!=oldnum: 
                    # changement de cellule
                    self.__hovernum    = numcell
                    self.__subhovernum = subcell
                    info = {}
                    self.__addmods(event.state,info)
                    if oldnum>=0:
                        info['row']     = self.__num2coords(oldnum)[0]
                        info['col']     = self.__num2coords(oldnum)[1]
                        if self.__subon:
                            info['subcell'] = oldsub
                            info['type']    = 'subleave'
                            self.__hover(self,info)
                        info['type']    = 'leave'
                        self.__hover(self,info)
                    if self.__subon:
                        info['subcell'] = subcell
                    info['row']     = self.__num2coords(numcell)[0]
                    info['col']     = self.__num2coords(numcell)[1]
                    info['type']    = 'enter'
                    self.__hover(self,info)
                    if self.__subon:
                        info['type']    = 'subenter'
                        self.__hover(self,info)
                elif self.__subon and numcell==oldnum and subcell!=oldsub:
                    # changement de sous-cellule
                    self.__hovernum    = numcell
                    self.__subhovernum = subcell
                    info = {}
                    info['row']     = self.__num2coords(numcell)[0]
                    info['col']     = self.__num2coords(numcell)[1]
                    self.__addmods(event.state,info)
                    if oldsub>=0:
                        info['subcell'] = oldsub
                        info['type']    = 'subleave'
                        self.__hover(self,info)
                    info['subcell'] = subcell
                    info['type']    = 'subenter'
                    self.__hover(self,info)
        
    def __boardkey(self,event):
        """ handler de l'événement tkinter <KeyPress> """
        if not self.__animate:
            info = { 'keysym' : self.__keysym(event.keysym) }
            self.__addmods(event.state,info)
            self.__key(self,info)
        
    def __addmods(self,state,info):
        """ ajoute les clés de modificateurs au dictionnaire info """
        mods = {
            0x0001:'shift',
            0x0004:'control',
            0x0100:'button1',
            # 0x0200:'button2',
            0x0400:'button3'
            # 0x0008:'alt',
            # 0x0080:'altgr'
        }
        for mask in mods.keys():
            info[mods[mask]]=bool(state&mask)
    
    def __numcell(self,x,y):
        """ numéro de la case aux coordonnées (x,y) du Canvas """
        col = max(min((x-self.__boarderr)//self.__cell,self.__hsize-1),0)
        row = max(min((y-self.__boarderr-self.__infoDec)//self.__cell,self.__vsize-1),0)
        return row*self.__hsize+col
        
    def __subcell(self,x,y):
        """ numéro de la sous-case aux coordonnées (x,y) du Canvas """
        col    = max(min((x-self.__boarderr)//self.__cell,self.__hsize-1),0)
        row    = max(min((y-self.__boarderr-self.__infoDec)//self.__cell,self.__vsize-1),0)
        subcol = max(min(((x-self.__boarderr)-col*self.__cell)//(self.__cell//3),2),0)
        subrow = max(min(((y-self.__boarderr-self.__infoDec)
                            -row*self.__cell)//(self.__cell//3),2),0)
        return subrow*3+subcol
        
    def __keysym(self,keysym):
        """ enlève le préfixe des 'keysym' des flèches """
        if keysym.find('KP_')==0:
            return keysym[3:]
        else:
            return keysym
    
    def __image(self,fileName,angle,padding,force=False):
        """ crée et mémorise une PhotoImage pour une cellule """
        name = os.path.splitext(os.path.basename(fileName))[0]
        key  = str(angle)+'-'+str(padding)+'-'+name
        if key not in self.__images.keys() or force:
            img          = Image.open(fileName).rotate(angle)
            width,height = img.size
            img          = img.resize((self.__cell-2*padding,self.__cell-2*padding),Image.LANCZOS)
            self.__images[key] = ImageTk.PhotoImage(img)
        return self.__images[key]
    
    def __bgimage(self,fileName,angle,padding,force=False):
        """ crée et mémorise une PhotoImage pour un fond de cellule """
        name = os.path.splitext(os.path.basename(fileName))[0]
        key  = str(angle)+'-'+str(padding)+'-'+name
        if key not in self.__bgimages.keys() or force:
            img          = Image.open(fileName).rotate(angle)
            width,height = img.size
            img          = img.resize((self.__cell-2*padding,self.__cell-2*padding),Image.LANCZOS)
            self.__bgimages[key] = ImageTk.PhotoImage(img)
        return self.__bgimages[key]
              
    def __subimage(self,fileName,angle,padding,force=False):
        """ crée et mémorise une PhotoImage pour une sous-cellule """
        name = os.path.splitext(os.path.basename(fileName))[0]
        key  = str(angle)+'-'+str(padding)+'-'+name
        if key not in self.__subimages.keys() or force:
            img          = Image.open(fileName).rotate(angle)
            width,height = img.size
            img          = img.resize((self.__cell//3-2*padding,self.__cell//3-2*padding),Image.LANCZOS)
            self.__subimages[key] = ImageTk.PhotoImage(img)
        return self.__subimages[key]
            
    def __num2coords(self,num):
        """ retourne la position (ligne,colonne) dans la grille d'une cellule 
            à partir de son numéro """
        return num//self.__hsize , num%self.__hsize   
                 
    def __coords2num(self,row,col):
        """ retourne le numéro d'une cellule 
            à partir de sa position (ligne,colonne) dans la grille """
        return row*self.__hsize+col
        
    def selectOne(self,row,col,**kwargs):
        """ sélectionne une cellule et déselectionne les autres """
        color = kwargs.pop('color','red')
        if 0<=row<self.__vsize and 0<=col<self.__hsize:
            for num,id in self.__select:
                self.__board.delete(id)
            self.__select = [[  self.__coords2num(row,col),
                                self.__board.create_rectangle(
                                    self.__boarderr+col*self.__cell,
                                    self.__infoDec+self.__boarderr+row*self.__cell,
                                    self.__boarderr+(col+1)*self.__cell,
                                    self.__infoDec+self.__boarderr+(row+1)*self.__cell,
                                    outline=color,width=4,tag='select') 
                            ]] 
        
    def select(self,row,col,**kwargs):
        """ étend la sélection à la cellule repérée par sa ligne et sa colonne """
        color = kwargs.pop('color','red')
        if 0<=row<self.__vsize and 0<=col<self.__hsize:
            self.__select.append([  self.__coords2num(row,col),
                                self.__board.create_rectangle(
                                    self.__boarderr+col*self.__cell,
                                    self.__infoDec+self.__boarderr+row*self.__cell,
                                    self.__boarderr+(col+1)*self.__cell,
                                    self.__infoDec+self.__boarderr+(row+1)*self.__cell,
                                    outline=color,width=4,tag='select') 
                            ])    
                                
    def unSelectAll(self):
        """ déselectionne toutes les cellules sélectionnées """
        for num,id in self.__select:    
            self.__board.delete(id)
        self.__select = []
                                        
    def getSelection(self):
        """ retourne les coordonnées des cellules sélectionnées """
        if len(self.__select)>0:
            return  [   {   
                            'row':self.__num2coords(self.__select[i][0])[0],
                            'col':self.__num2coords(self.__select[i][0])[1]
                        }
                        for i in range(len(self.__select))  ]
        else:
            return self.__select
            
    def animate(self,row,col,rowd,cold,delay,**kwargs):
        """ anime une image « fantôme » """
        callback = kwargs.pop('end',lambda:None)
        args     = kwargs.pop('args',[])
        
        image = self.__board.itemcget(self.__cells[row][col],'image')
        ghost = self.__board.create_image(
                    self.__boarderr+(2*col+1)*self.__cell/2,
                    self.__infoDec+self.__boarderr+(2*row+1)*self.__cell/2,
                    image=image,
                    tag='cell')
        xs,ys = self.__board.coords(ghost)
        xd,yd = self.__board.coords(self.__cells[rowd][cold])
        self.delImage(row,col)
        def move(xs,ys,xd,yd,steps,delay):
            deltaX = (xd-xs)//steps
            deltaY = (yd-ys)//steps
            x,y    = self.__board.coords(ghost)
            if abs(xd-x)>abs(deltaX) or abs(yd-y)>abs(deltaY):
                self.__board.move(ghost,deltaX,deltaY)
                time.sleep(delay//steps/1000)
                threading.Thread(target=move, args=[xs,ys,xd,yd,steps,delay]).start()
            else:
                self.__board.delete(ghost)
                self.__board.itemconfigure(self.__cells[rowd][cold],image=image)
                callback(*args)
                self.__animate.pop()
        self.__animate.append(1)
        threading.Thread(target=move, args=[xs,ys,xd,yd,delay//10,delay]).start()
       
        
    def setImage(self,row,col,fileName,**kwargs):
        """ place une image dans une cellule repérée par sa ligne et sa colonne """
        if fileName=='':
            self.__board.itemconfigure(self.__cells[row][col],image=self.__image(self.__empty,0,0))
        else:
            angle   = kwargs.pop('rotate',0)
            padding = kwargs.pop('padding',2)
            force   = kwargs.pop('force',False)
            image   = self.__image(fileName,angle,padding,force)
            self.__board.itemconfigure(self.__cells[row][col],image=image)
                                        
    def delImage(self,row,col):
        """ efface l'image d'une cellule repérée par sa ligne et sa colonne """
        self.__board.itemconfigure(self.__cells[row][col],image=self.__image(self.__empty,0,0))
        
    def setSubImage(self,row,col,subcell,fileName,**kwargs):
        """ place une image dans une sous-cellule repérée par sa ligne et sa colonne """
        if fileName=='':
            self.__board.itemconfigure(self.__subcells[row][col][subcell],
                                        image=self.__subimage(self.__empty,0,0))
        else:
            angle   = kwargs.pop('rotate',0)
            padding = kwargs.pop('padding',2)
            force   = kwargs.pop('force',False)
            image   = self.__subimage(fileName,angle,padding,force)
            self.__board.itemconfigure(self.__subcells[row][col][subcell],image=image)
        
    def delSubImage(self,row,col,subcell):
        """ efface l'image d'une sous-cellule repérée par sa ligne et sa colonne """
        self.__board.itemconfigure(self.__subcells[row][col][subcell],
                                    image=self.__subimage(self.__empty,0,0))
        
    def setBgImage(self,row,col,fileName,**kwargs):
        """ place une image de fond pour une cellule repérée par sa ligne et sa colonne """
        if fileName=='':
            self.__board.itemconfigure(self.__backgroundcells[row][col],
                                        image=self.__bgimage(self.__empty,0,0))
        else:
            angle   = kwargs.pop('rotate',0)
            padding = kwargs.pop('padding',0)
            force   = kwargs.pop('force',False)
            image   = self.__bgimage(fileName,angle,padding,force)
            self.__board.itemconfigure(self.__backgroundcells[row][col],image=image)
                                        
    def delBgImage(self,row,col):
        """ efface l'image de fond pour une cellule repérée par sa ligne et sa colonne """
        self.__board.itemconfigure(self.__backgroundcells[row][col],
                                    image=self.__bgimage(self.__empty,0,0))
        
    def setBgColor(self,row,col,color):
        """ définit la couleur de fond d'une cellule repérée par sa ligne et sa colonne """
        self.__board.itemconfigure(self.__backgrounds[row][col],fill=color)
        
    def setBgBorder(self,row,col,width):
        """ définit la bordure du fond d'une cellule repérée par son numéro
            au sein d'une cellule donnée par sa ligne et sa colonne """
        self.__board.itemconfigure(self.__backgrounds[row][col],width=width)
        
    def setSubBgColor(self,row,col,subcell,color):
        """ définit la couleur de fond d'une sous-cellule repérée par sa ligne et sa colonne """
        self.__board.itemconfigure(self.__subbackgrounds[row][col][subcell],fill=color)
            
    def blink(self,row,col,**kwargs):
        """ fait clignoter le fond d'une cellule repérée par sa ligne et sa colonne """
        oldcolor = self.__board.itemcget(self.__backgrounds[row][col],'fill')
        blinkCol = kwargs.pop('color',self.__defblinkcol)
        if oldcolor!=blinkCol:
            self.setBgColor(row,col,blinkCol)
            def putItBack(color):
                time.sleep(.1)
                self.setBgColor(row,col,color)
            threading.Thread(target=putItBack, args=[oldcolor]).start()   
                     
    def blinkSub(self,row,col,subcell,**kwargs):
        """ fait clignoter le fond d'une sous-cellule repérée par son numéro
            au sein d'une cellule donnée par sa ligne et sa colonne """
        oldcolor = self.__board.itemcget(self.__subbackgrounds[row][col][subcell],'fill')
        blinkCol = kwargs.pop('color',self.__defblinkcol)
        if oldcolor!=blinkCol:
            self.setSubBgColor(row,col,subcell,blinkCol)
            def putItBack(color):
                time.sleep(.1)
                self.setSubBgColor(row,col,subcell,color)
            threading.Thread(target=putItBack, args=[oldcolor]).start()
        
    def console(self,*args):
        """ envoie les arguments à l'affichage dans la console """
        if not self.__console:
            print(args)
            return
        msg = ' '.join([str(a) for a in args])
        if not self.__display.get(1.0, "end-1c")=='':
            msg = '\n'+msg
        self.__display.config(state=NORMAL)
        self.__display.insert(END,msg)
        self.__display.yview(END)
        self.__display.config(state=DISABLED)
        
    def display(self,*args,**kwargs):
        """ envoie les arguments à l'affichage dans la zone d'information du joueur """
        if not self.__info:
            print(args)
            return
        color = kwargs.pop('color','black')
        row   = kwargs.pop('row',0)
        col   = kwargs.pop('col',0)
        text  = ' '.join([str(a) for a in args])
        key   = '-'.join([str(row),str(col)])
        if key in self.__infoTexts :
            textId = self.__infoTexts[key]
            self.__board.itemconfigure(textId,text=text,fill=color)
        else:
            if self.__infoPlace == 'down':
                decalage = self.__cell*self.__vsize+self.__boarderr
            else:
                decalage = 0
            self.__infoTexts[key] = self.__board.create_text(
                        self.__boarderr+col*11,
                        decalage+self.__boarderr+row*self.__infoHeight,
                        text = text,anchor='nw',
                        font = self.__infoFont,
                        fill=color)

    def unDisplay(self,row,col): 
        """ efface une information de la zone d'information du joueur """
        key   = '-'.join([str(row),str(col)])
        if key in self.infoTexts :
            self.__board.delete(self.__infoTexts[key]) 
            
    def end(self):
        """ fermeture de la fenêtre """
        self.__root.destroy()
        
    def after(self,*args):
        self.__root.after(*args)
        
        
        
    
        
        
        