import h5py
import numpy as np

class LoadTristanmp:
   
    def loadfield(self, 
                filepath,
                dim, 
                iteration, 
                field):

        fname = filepath+'/flds.tot.'+str('%3.3d'%(iteration))
        fi = h5py.File(fname, 'r')
        if field[1] == 'x':
            dset = fi[field[0]+'y']
        elif field[1] == 'y':
            dset = fi[field[0]+'z']
        elif field[1] == 'z':
            dset = fi[field[0]+'x']
        elif field[2] == 'x':
            dset = fi[field[0:2]+'y'+field[3:]]
        elif field[2] == 'y':
            dset = fi[field[0:2]+'z'+field[3:]]
        elif field[2] == 'z':
            dset = fi[field[0:2]+'x'+field[3:]]
        else:
            dset = fi[field]
        
        tempdata = dset[()]

        tempdata=np.float32(tempdata)
        #tempdata = tempdata.T
        tempdata = tempdata[0,:,:]

        return tempdata

