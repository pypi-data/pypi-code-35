import numpy as np

import yt
from yt.funcs import mylog
mylog.setLevel(0)


def WarpXinfo(dataformat,
                file_path,
                file_list,
                fname,
                iterations,
                iteration):      

    ##############################################################
    # find field list
    ##############################################################
    field_list = []
    ds = yt.load(fname)
    field_list_all = ds.field_list
    nfields_all = len(field_list_all)
    for i in np.arange(nfields_all):
        if field_list_all[i][0] == 'boxlib':
            field_list.append(field_list_all[i][1])

    ##############################################################
    # find the coordinate system, 'Cartesian or cylindrical
    ##############################################################
    if ds.parameters['geometry.coord_sys'] == '0':
        coord_system = 'cartesian'
    else:
        coord_system = 'cylindrical'

    ##############################################################
    # find dimensionality
    ##############################################################
    if ds.domain_dimensions[2] > 1:
        dim = 3
    elif ds.domain_dimensions[1] == 1:
        dim = 1
    else: 
        dim = 2
    
    ##############################################################
    # find species list
    ##############################################################
    ds.index
    species_list_all=ds.particle_types
    mass_list = []
    species_list = []
    numpart_list = []
    dpfact_list = {}
    for species in species_list_all:
        if species[0] != 'a':
            try:
                q = ds.parameters[species+'.charge']
                m = ds.parameters[species+'.mass']
                mass_list.append(m)
            except KeyError:
                pass
            species_list.append(species)

            numpart = ds.particle_type_counts[species]
            numpart_list.append(numpart)
            dpfact = int(np.ceil(1.*numpart/1e8))
            dpfact_list[species]=dpfact
            
    ##############################################################
    # AMR level: level 0 , level 1, .....
    ##############################################################
    level = []
    for grids in ds.index.grids:
        level.append(grids.Level)
    amrlevel = np.max(level)

                
    ##############################################################
    # phase list
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
    # get times in fs unis
    ##############################################################
    taxis=np.zeros(len(file_list))
    s=0
    for files in file_list:
        ds = yt.load(files)
        time=ds.current_time.d*1.e15
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
        ds = yt.load(files)

        if dim == 3:

            xmin=ds.domain_left_edge[0].d*1.e6
            ymin=ds.domain_left_edge[1].d*1.e6
            zmin=ds.domain_left_edge[2].d*1.e6
            xmax=ds.domain_right_edge[0].d*1.e6
            ymax=ds.domain_right_edge[1].d*1.e6
            zmax=ds.domain_right_edge[2].d*1.e6
            nx = ds.domain_dimensions[0]
            ny = ds.domain_dimensions[1]
            nz = ds.domain_dimensions[2]

            xaxis=1.*np.arange(nx)*(xmax-xmin)/nx+xmin
            yaxis=1.*np.arange(ny)*(ymax-ymin)/ny+ymin
            zaxis=1.*np.arange(nz)*(zmax-zmin)/nz+zmin

            dxfact = int(np.ceil(1.*nx/256))
            dyfact = int(np.ceil(1.*ny/256))
            dzfact = int(np.ceil(1.*nz/512))

            xaxis=xaxis[::dxfact]
            yaxis=yaxis[::dyfact]
            zaxis=zaxis[::dzfact]

        else:
            xmin=ds.domain_left_edge[0].d*1.e6
            zmin=ds.domain_left_edge[1].d*1.e6
            xmax=ds.domain_right_edge[0].d*1.e6
            zmax=ds.domain_right_edge[1].d*1.e6
            nx = ds.domain_dimensions[0]
            nz = ds.domain_dimensions[1]

            xaxis=1.*np.arange(nx)*(xmax-xmin)/nx+xmin
            zaxis=1.*np.arange(nz)*(zmax-zmin)/nz+zmin
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
    param_dic['species_list'] = species_list
    param_dic['phase_list1'] = phase_list1
    if dim == 3:
        param_dic['phase_list2'] = phase_list2
        param_dic['phase_list3'] = phase_list3
    param_dic['mass_list'] = mass_list

    param_dic['dxfact'] = dxfact
    param_dic['dyfact'] = dyfact
    param_dic['dzfact'] = dzfact
    param_dic['numpart_list'] = numpart_list
    param_dic['dpfact_list'] = dpfact_list

    param_dic['amrlevel'] = amrlevel

    return param_dic
