from eniseboard import *
from random import *
from PIL import Image
import tempfile
import os, pkg_resources

class tux():
    def __init__(self):
        self.__dir = pkg_resources.resource_filename('eniseboard', 'demos/penguinimage/')
        eniseboard( hsize=3,vsize=3,cell=120,grid=True,console=True,info=True,
                title='Penguin',init=self.__initialiser,click=self.__clicSouris)
                
    def __initialiser(self,board):
        board.console('Cliquez pour placer Tux')
            
    def __clicSouris(self,board,event):
        i = event['row']
        j = event['col']
        selection = board.getSelection()
        if len(selection)>0:
            coords = selection[0]
            board.delImage(coords['row'],coords['col'])
        board.setImage(i,j,self.__dir+'penguin.png')
        board.selectOne(i,j)
        board.display('Tux est en (',i,',',j,')')
        
class taquin():    
    def __init__(self,largeur=4,cell=150): 
        print("Mode d'emploi")
        print("=============")
        print("   - mélanger le taquin : touche S")
        print("   - changer d'image    : touches 1 à 5 ")
        print("   - jouer au clavier   : flèches")
        print("   - jouer à la souris  : clic gauche")
        print("   - quitter le jeu     : Ctrl+Q")
        self.__idir    = pkg_resources.resource_filename('eniseboard', 'demos/taquinimages/')
        self.__sdir    = self.__idir+'sources/'
        self.__tdir    = tempfile.mkdtemp()+'/'
        self.__largeur = largeur  # nombre de pieces par ligne/colonne
        self.__numero  = 1        # numero du fichier source
        self.__cell    = cell     # largeur d'une pièce en pixels
        eniseboard( hsize=self.__largeur,vsize=self.__largeur,cell=self.__cell,grid=True,
                    title='Taquin',bgcolor='midnight blue',info=True,infoPlace='top',
                    infoLines=1,click=self.__clicSouris,key=self.__clavier,
                    init=self.__initialiser,hover=self.__survolSouris)
        
    def __initialiser(self,game):
        self.__fabriquerImages(self.__numero)
        self.__remettreAZero()  
        self.__mettreAJour(game)
 
    def __clicSouris(self,game,info):
        move = self.__mobile(info['row'],info['col'])
        if move:
            self.__bouger(game,*move)
    
    def __bouger(self,game,dir,nb):
        game.unSelectAll()
        for i in range(nb):
            rowS,colS,rowD,colD = self.__calculerBouger(dir)
            if rowS!=rowD or colS!=colD:
                self.__coup += 1
                tile = self.__taquin[rowS][colS]
                self.__taquin[rowS][colS] = self.__vide
                self.__taquin[rowD][colD] = tile
                game.display('Mouvements :',self.__coup,color='dark orange')
                game.animate(rowS,colS,rowD,colD,200)

            
    def __survolSouris(self,game,info):
        if info['type']=='enter':
            if self.__mobile(info['row'],info['col']):
                game.selectOne(info['row'],info['col'],color='chartreuse')
            else:
                game.selectOne(info['row'],info['col'],color='red')
        
    def __clavier(self,game,info):
        if len(game.getSelection())>0:
            game.unSelectAll()
        if info['keysym']=='q' and info['control']:
            game.end()
        elif info['keysym'] in ['Right','Left','Down','Up']:
            self.__bouger(game,info['keysym'],1)
        elif info['keysym']=='s':
            self.__melanger(game)
            self.__mettreAJour(game)
        elif info['keysym']=='r':
            self.__remettreAZero()
            self.__mettreAJour(game)
        elif info['keysym'] in [str(i) for i in range(1,len(os.listdir(self.__sdir))+1)]:
            self.__fabriquerImages(int(info['keysym'])-1)
            self.__remettreAZero()
            self.__mettreAJour(game,True)
        elif info['keysym']=='b':
            for j in range(self.__largeur):
                for i in range(self.__largeur):
                    game.animate(self.__largeur-i-2,
                                self.__largeur-j-1,
                                self.__largeur-i-1,
                                self.__largeur-j-1,200)
         
    def __mettreAJour(self,game,reload=False):
        """ met à jour l'affichage du taquin """
        for row in range(self.__largeur):
            for col in range(self.__largeur):
                game.setImage(row,col,self.__images[self.__taquin[row][col]],padding=1,force=reload)
                if self.__taquin[row][col]==self.__vide:
                    game.blink(row,col,color='dark orange')
        game.display('Mouvements :',self.__coup,color='dark orange')
                
    def __melanger(self,game):
        """ mélange le taquin """
        for direction in [choice(['Right','Left','Down','Up']) for i in range(200)]:
            rowS,colS,rowD,colD = self.__calculerBouger(direction)
            tile = self.__taquin[rowS][colS]
            self.__taquin[rowS][colS] = self.__vide
            self.__taquin[rowD][colD] = tile
        self.__coup = 0
        
    def __calculerBouger(self,dir):
        """ bouge une pièce du taquin dans la direction indiquée 
            et retourne les 4 coordonnées avant / après """
        row,col = self.__positionVide()
        dx,dy = (0,0)
        if dir=='Right':
            if col>0:
                dx,dy = (0,1)
        elif dir=='Left':
            if col<self.__largeur-1:
                dx,dy = (0,-1)
        elif dir=='Down':
            if row>0:
                dx,dy = (1,0)
        elif dir=='Up':
            if row<self.__largeur-1:
                dx,dy = (-1,0)
        return row-dx,col-dy,row,col
        
                
    def __positionVide(self,):
        """ renvoie un tuple donnant la position de la place vide """
        for i in range(len(self.__taquin)):
            for j in range(len(self.__taquin[i])):
                if self.__taquin[i][j]==self.__vide:
                    return i,j
    
    def __mobile(self,i,j):
        """ si la pièce (i,j) est déplaçable, renvoie
            la direction dans laquelle on peut la déplacer
            ainsi que le nombre total de pièces à déplacer
            sinon renvoie False """
        row,col = self.__positionVide()
        if  self.__taquin[i][j]==self.__vide or (i!=row and j!=col):
            return False
        elif i==row:
            if col-j>0:
                return 'Right',col-j
            else:
                return 'Left',j-col
        else:
            if row-i>0:
                return 'Down',row-i
            else:
                return 'Up',i-row
    
    def __remettreAZero(self,):
        """ réinitialise le taquin """
        self.__coup    = 0
        self.__taquin  = [[self.__largeur*i+j for j in range(self.__largeur)] 
                                for i in range(self.__largeur)]
        
    def __fabriquerImages(self,num):
        """ fabrique toutes les images du taquin à partir d'une image source """
        # fabrication des images
        image  = Image.open([ self.__sdir+f for f in os.listdir(self.__sdir) 
                                if ( os.path.splitext(f)[1].lower()=='.png'
                                    or os.path.splitext(f)[1].lower()=='.jpg') ][num])
        width,height = image.size
        for col in range(self.__largeur):
            for row in range(self.__largeur):
                img = image.crop((col*width//self.__largeur,row*width//self.__largeur,
                                    (col+1)*width//self.__largeur,(row+1)*width//self.__largeur))
                img.save(self.__tdir+str(row*self.__largeur+col)+'.png')
        # traitement de la case vide
        self.__vide    = self.__largeur**2-1
        Image.open(self.__idir+'empty.png').save(self.__tdir+str(self.__vide)+'.png')
        # mise à jour de la liste des noms des images
        self.__images  = [self.__tdir+str(i)+'.png' for i in range(self.__largeur**2)]

    
