import h5py
import numpy as np

def openPMDinfo(dataformat,
                filepath,
                file_list,
                fname,
                iterations,
                iteration):      

    ##############################################################
    # find field list
    ##############################################################
    field_list = []
    fi = h5py.File(fname,'r')
    item = fi['data/'+str(iteration)+'/fields']
    fields_group = item.items()
    nfields = len(fields_group)
        
    item = fi['data/'+str(iteration)+'/fields/E']
    coord_group = item.items()
    ncoord = len(coord_group)
    coord_list = []
    for i in np.arange(ncoord):
        coord_list.append(coord_group[i][0])

    for i in np.arange(nfields):
        for j in np.arange(ncoord):
            if fields_group[i][0] != 'rho':
                field_list.append(fields_group[i][0]+coord_list[j])
            else:
                field_list.append(fields_group[i][0])
                break

    ##############################################################
    # find the coordinate system, 'Cartesian or cylindrical
    ##############################################################
    item = fi['data/'+str(iteration)+'/fields/'+field_list[0][0]].attrs['geometry']
    if item == 'cartesian':
        coord_system = 'cartesian'
    else:
        coord_system = 'cylindrical'

    ##############################################################
    # find dimensionality
    ##############################################################
    item = fi['data/'+str(iteration)+'/fields/'+field_list[0][0]].attrs['axisLabels']
    dim = len(item)

    
    ##############################################################
    # find species list
    ##############################################################
    try: 
        dset= fi['data/'+str(iteration)+'/particles']
        lparticle = 1
    except KeyError:
        lparticle = 0

    if lparticle:

        species_list = dset.keys()
        mass_list = []
        numpart_list = []
        dpfact_list = {}
        for species in species_list:
            q = dset[species+'/charge'].attrs['value']
            m = dset[species+'/mass'].attrs['value']
            mass_list.append(m)

        for species in species_list:
            dset = fi['data/'+str(iteration)+'/particles/' \
                    +species+'/weighting']
            numpart = dset.shape[0]
            dpfact = int(np.ceil(1.*numpart/5e7))
            numpart_list.append(numpart)
            dpfact_list[species]=dpfact


        ##############################################################
        # pahse list
        ##############################################################
        if dim == 2:
            phase_list1 = []
            phase_list1.append(('x','z'))
            phase_list1.append(('px','z'))
            #phase_list1.append(('py','z'))
            phase_list1.append(('pz','z'))
            phase_list1.append(('ene','z'))
            phase_list1.append(('px','pz'))
            phase_list1.append(('x','px'))
            #phase_list1.append(('x','py'))
            phase_list1.append(('x','pz'))
            phase_list1.append(('x','ene'))
            #phase_list1.append(('ene','ang'))

        else:
        
            phase_list1 = []
            phase_list1.append(('x','z'))
            phase_list1.append(('px','z'))
            phase_list1.append(('py','z'))
            phase_list1.append(('pz','z'))
            phase_list1.append(('ene','z'))
            phase_list1.append(('px','pz'))
            phase_list1.append(('x','px'))
            phase_list1.append(('x','py'))
            phase_list1.append(('x','pz'))
            phase_list1.append(('x','ene'))
            #phase_list1.append(('ene','ang'))

            phase_list2 = []
            phase_list2.append(('y','x'))
            phase_list2.append(('px','x'))
            phase_list2.append(('py','x'))
            phase_list2.append(('pz','x'))
            phase_list2.append(('ene','x'))
            phase_list2.append(('py','px'))
            phase_list2.append(('y','px'))
            phase_list2.append(('y','py'))
            phase_list2.append(('y','pz'))
            phase_list2.append(('y','ene'))
            #phase_list2.append(('ene','ang'))

            phase_list3 = []
            phase_list3.append(('y','z'))
            phase_list3.append(('px','z'))
            phase_list3.append(('py','z'))
            phase_list3.append(('pz','z'))
            phase_list3.append(('ene','z'))
            phase_list3.append(('py','pz'))
            phase_list3.append(('y','px'))
            phase_list3.append(('y','py'))
            phase_list3.append(('y','pz'))
            phase_list3.append(('y','ene'))
            #phase_list3.append(('ene','ang'))


    ##############################################################
    # get times in fs unit
    ##############################################################
    taxis=np.zeros(len(file_list))
    s=0
    for files in file_list:
        fi = h5py.File(files,'r')
        dset=fi['/data/'+str(iterations[s])]
        time=dset.attrs['time']*1.e15
        taxis[s]=time
        s+=1  

    ##############################################################
    # get spatial axes at different times
    ##############################################################
    xaxis_dic = {}
    yaxis_dic = {}
    zaxis_dic = {}

    s = 0
    for files in file_list:
        fi = h5py.File(files,'r')

        if dim ==3:
            dset=fi['/data/'+str(iterations[s])+'/fields/E']
            dx,dy,dz=dset.attrs["gridSpacing"]
            xmin,ymin,zmin = dset.attrs['gridGlobalOffset']
            dset=fi['/data/'+str(iterations[s])+'/fields/E/x']
            nx,ny,nz = dset.shape
            xmax=nx*dx+xmin
            ymax=ny*dy+ymin
            zmax=nz*dz+zmin
            
            xaxis=1.*np.arange(nx)*(xmax-xmin)/nx+xmin
            yaxis=1.*np.arange(ny)*(ymax-ymin)/ny+ymin
            zaxis=1.*np.arange(nz)*(zmax-zmin)/nz+zmin
            xaxis*=1.e6
            yaxis*=1.e6
            zaxis*=1.e6

            dxfact = int(np.ceil(1.*nx/512))
            dyfact = int(np.ceil(1.*ny/512))
            dzfact = int(np.ceil(1.*nz/512))

            xaxis=xaxis[::dxfact]
            yaxis=yaxis[::dyfact]
            zaxis=zaxis[::dzfact]

        else:

            dset=fi['/data/'+str(iterations[s])+'/fields/E']
            dx,dz=dset.attrs["gridSpacing"]
            xmin,zmin = dset.attrs['gridGlobalOffset']
            dset=fi['/data/'+str(iterations[s])+'/fields/E/x']
            nx,nz = dset.shape
            ny = 1
            xmax=nx*dx+xmin
            zmax=nz*dz+zmin
            
            xaxis=1.*np.arange(nx)*(xmax-xmin)/nx+xmin
            zaxis=1.*np.arange(nz)*(zmax-zmin)/nz+zmin
            xaxis*=1.e6
            zaxis*=1.e6
            yaxis=np.array([0])

            dxfact = int(np.ceil(1.*nx/2048))
            dzfact = int(np.ceil(1.*nz/2048))
            dyfact = 1

            xaxis=xaxis[::dxfact]
            zaxis=zaxis[::dzfact]

        xaxis_dic[s] = xaxis
        yaxis_dic[s] = yaxis
        zaxis_dic[s] = zaxis
        
        s+=1

    param_dic = {}

    param_dic['iterations'] = iterations
    param_dic['dataformat'] = dataformat
    param_dic['field_list'] = field_list
    param_dic['coord_system'] = coord_system
    param_dic['dim'] = dim
    param_dic['taxis'] = taxis
    param_dic['xaxis_dic'] = xaxis_dic
    param_dic['yaxis_dic'] = yaxis_dic
    param_dic['zaxis_dic'] = zaxis_dic
    if lparticle:
        param_dic['species_list'] = species_list
        param_dic['phase_list1'] = phase_list1
        if dim == 3:
            param_dic['phase_list2'] = phase_list2
            param_dic['phase_list3'] = phase_list3
        param_dic['mass_list'] = mass_list

    param_dic['nx'] = nx
    param_dic['nz'] = nz
    param_dic['dxfact'] = dxfact
    param_dic['dyfact'] = dyfact
    param_dic['dzfact'] = dzfact
    param_dic['ny'] = ny
    if lparticle:
        param_dic['numpart_list'] = numpart_list
        param_dic['dpfact_list'] = dpfact_list

    return param_dic
