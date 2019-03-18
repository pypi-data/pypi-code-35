
import glob
import numpy as np

import picviewer.dataloader.get_warpxinfo as warpxinfo
import picviewer.dataloader.get_openpmdinfo as openpmdinfo
#import picviewer.dataloader.get_tristanmpinfo as tristanmpinfo


class DataInfo:

    def datainfo(self, filepath):
        """
        load simulation parameters

        Returns: param={} dictionary
        """

        # warpX data file
        file_list1 = glob.glob(filepath + '/plt?????')

        # openPMD data file
        file_list2 = glob.glob(filepath + '/data????????.h5')

        # tristan-MP data file
        file_list3 = glob.glob(filepath + '/flds.tot.???')

        if len(file_list1) != 0:
            dataformat = 'WarpX'
            file_list = file_list1
            getDatainfo = warpxinfo.WarpXinfo
        elif len(file_list2) != 0:
            dataformat = 'openPMD'
            file_list = file_list2
            getDatainfo = openpmdinfo.openPMDinfo
        elif len(file_list3) != 0:
            dataformat = 'tristanMP'
            file_list = file_list3
            getDatainfo = tristanmpinfo.tristanMPinfo

            
        if dataformat == 'WarpX':
            iterations = [ int(file_name[len(file_name)-5:]) for file_name in file_list ]
            
        elif dataformat == 'openPMD':
            iterations = [ int(file_name[len(file_name)-11:len(file_name)-3]) for file_name in file_list ]
 
        elif dataformat == 'tristanMP':
            iterations = [ int(file_name[len(file_name)-3:len(file_name)]) for file_name in file_list ]
            
        file_list.sort()
        iterations.sort()
        tmax = len(iterations)


        param_dic = getDatainfo(
                        dataformat,
                        filepath,
                        file_list,
                        file_list[tmax-1],
                        iterations,
                        iterations[tmax-1])

        return param_dic


  #  def updata_domain(self,
  #          filepath,
  #          dataformat,
  #          dim,
  #         iteration):

  #      if dataformat == 'WarpX':
  #          updata_domain_axes = warpxinfo.update_domain_axes
  #      elif dataformat == 'openPMD':
  #          updata_domain_axes = openpmdinfo.update_domain_axes

  #      xaxis, yaxis, zaxis = updata_domain_axes(
  #              filepath,
  #              dataformat,
  #              dim,
  #              iteration)


  #      return xaxis, yaxis, zaxis

        
    
