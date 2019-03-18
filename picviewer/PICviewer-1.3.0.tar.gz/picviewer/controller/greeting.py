
import picviewer

class Greeting():

    def __init__(self,Mainwindow):

        self.main = Mainwindow

        version = picviewer.__version__
    
        tstep = len(self.main.iterations)
        xaxis = self.main.xaxis_dic[tstep-1]
        yaxis = self.main.yaxis_dic[tstep-1]
        zaxis = self.main.zaxis_dic[tstep-1]
        
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print('Welcome to PICviewer  \ (•◡•) / ')
        print('Developed by Jaehong Park (LBNL), v.%s copyright @ LBNL'%version)
        #print('DOE CODE, ID# 19363')
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print('Load %s %dD simulation data'%(self.main.dataformat, self.main.dim))
        if self.main.dataformat == 'WarpX':
            print(' AMR level = ',self.main.amrlevel)
        print('Field data dims=',(len(xaxis),len(yaxis),len(zaxis)))
        print('--> downsample factor',(self.main.dxfact,self.main.dyfact,self.main.dzfact))
        print('field list', self.main.field_list)
        try:
            species_list = self.main.species_list
            lparticle = 1
        except AttributeError:
            lparticle = 0
        if lparticle:
            print('species list', self.main.species_list)
            print('species mass list', self.main.mass_list)
            print('particle number from source ',self.main.numpart_list)
            print('particle downsample factor',self.main.dpfact)
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')