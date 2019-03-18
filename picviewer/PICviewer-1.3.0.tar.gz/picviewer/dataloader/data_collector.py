import numpy as np

from picviewer.dataloader.load_warpx import LoadWarpx
from picviewer.dataloader.load_openpmd import LoadOpenpmd
#from picviewer.dataloader.load_tristanmp import LoadTristanmp
from picviewer.dataplotter.cic_histogram import particle_energy

class DataCollector():
    """
        load field and paritcle data class

    """
    def __init__(self,Mainwindow):

        self.main = Mainwindow
        
        if self.main.dataformat == 'WarpX':
            self.loaddata = LoadWarpx()
        if self.main.dataformat == 'openPMD':
            self.loaddata = LoadOpenpmd()
        if self.main.dataformat == 'tristanMP':
            self.loaddata = LoadTristanmp()

    def loaddatasync(self):

        for l in np.arange(self.main.nrow*self.main.ncolumn):

            # self.field_select_panel = [True, True, False, ....]
            # self.main.phase_panel = [('x','z'),('px','z'), ...]   
            tstep = self.main.tstep_panel[l]
            if self.main.field_select_panel[l]:
                field = self.main.field_panel[l]
                amrlevel = self.main.amrlevel_panel[l]
                self.loadfield(field, tstep, amrlevel)
            else:
                species = self.main.species_panel[l]
                phase= self.main.phase_panel[l]

                self.loadparticle(species, phase, tstep)
    
    def loadfield(self, field=None, tstep=None, amrlevel=None):
        """
        load field data for a selected window panel

        """
        if field is None: 
            field = self.main.field_panel[self.main.panelselect-1]
            tstep = self.main.tstep_panel[self.main.panelselect-1]
            amrlevel = self.main.amrlevel_panel[self.main.panelselect-1]
        
        if (field,tstep,amrlevel) in self.main.fdata_container.keys():
        # if the field data already exist in fdata_container, skip loading
            pass
        else:
            self.main.fdata_container[(field,tstep,amrlevel)] = \
                self.loaddata.loadfield(
                    self.main.filepath,
                    self.main.dim,
                    self.main.dxfact,
                    self.main.dyfact,
                    self.main.dzfact,
                    self.main.iterations[tstep-1],
                    field,
                    amrlevel)

    def loadparticle(self, species=None, phase=None, tstep=None):
        """
        load particle data for a selected window panel

        """
        if species == None: 
            species = self.main.species_panel[self.main.panelselect-1]
            tstep = self.main.tstep_panel[self.main.panelselect-1]
             # phase = ('x','z'), ....
            phase = self.main.phase_panel[self.main.panelselect-1]
           
        position_variables = ['x','y','z']
        momentum_variables = ['px','py','pz']
        other_variables = ['ene', 'ang']

        # load weight variable always
        if (species,'w', tstep) in self.main.pdata_container.keys():
            pass # if the particle variable is in data container, skip loading
        else:
            self.main.pdata_container[(species,'w',tstep)] = \
                self.loaddata.loadparticle(
                    self.main.filepath,
                    self.main.dim,
                    self.main.dpfact,
                    self.main.iterations[tstep-1], 
                    species,
                    'w')

        # 2D 
        if self.main.dim == 2:
            # loop over the phase tuple elements, i.e., phase = ('x','z'), ('px','z'), ...
            for index in range(2):
                variable = phase[index]
                # if variable is in 'ene', load momentum variables 'px', 'py', 'pz
                if variable in other_variables:
                    for var in momentum_variables:
                        if (species,var,tstep) in self.main.pdata_container.keys():
                            pass
                        else:
                            self.main.pdata_container[(species,var,tstep)] = \
                                self.loaddata.loadparticle(
                                self.main.filepath,
                                self.main.dim,
                                self.main.dpfact,
                                self.main.iterations[tstep-1], 
                                species,
                                var)
                else:   # load the selected variable
                    if (species,variable, tstep) in self.main.pdata_container.keys():
                        pass
                    else:
                        self.main.pdata_container[(species,variable,tstep)] = \
                            self.loaddata.loadparticle(
                                self.main.filepath,
                                self.main.dim,
                                self.main.dpfact,
                                self.main.iterations[tstep-1], 
                                species,
                                variable)
                                
                if variable == 'ene':
                        if (species,variable,tstep) in self.main.pdata_container.keys():
                            pass
                        else:
                            self.main.pdata_container[(species,variable,tstep)] = \
                                    particle_energy(
                                        self.main.pdata_container[(species,'px',tstep)],
                                        self.main.pdata_container[(species,'py',tstep)],
                                        self.main.pdata_container[(species,'pz',tstep)])
            

        # for 3D, load 'x', 'y', 'z' regardless of the variable selection
        # becaues of the 2D slicing in the 3D volume
        else:
            for variable in position_variables:
                if (species,variable, tstep) in self.main.pdata_container.keys():
                    pass
                else:
                    self.main.pdata_container[(species,variable,tstep)] = \
                        self.loaddata.loadparticle(
                            self.main.filepath,
                            self.main.dim,
                            self.main.dpfact,
                            self.main.iterations[tstep-1], 
                            species,
                            variable)
            
            for index in range(2):
                variable = phase[index]
                if variable in momentum_variables:
                    if (species,variable, tstep) in self.main.pdata_container.keys():
                        pass
                    else:
                        self.main.pdata_container[(species,variable,tstep)] = \
                            self.loaddata.loadparticle(
                                self.main.filepath,
                                self.main.dim,
                                self.main.dpfact,
                                self.main.iterations[tstep-1], 
                                species,
                                variable)
                # If the variable is energy, angles, then load 'px', 'py', and 'pz'. 
                elif variable in other_variables:
                    for var in momentum_variables:
                        if (species,var,tstep) in self.main.pdata_container.keys():
                            pass
                        else:
                            self.main.pdata_container[(species,var,tstep)] = \
                                self.loaddata.loadparticle(
                                self.main.filepath,
                                self.main.dim,
                                self.main.dpfact,
                                self.main.iterations[tstep-1], 
                                species,
                                var)

                if variable == 'ene':
                    if (species,variable,tstep) in self.main.pdata_container.keys():
                        pass
                    else:
                        self.main.pdata_container[(species,variable,tstep)] = \
                                particle_energy(
                                    self.main.pdata_container[(species,'px',tstep)],
                                    self.main.pdata_container[(species,'py',tstep)],
                                    self.main.pdata_container[(species,'pz',tstep)])
