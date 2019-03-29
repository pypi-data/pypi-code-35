import os


def create_folders():

    """
    Ensure that Program folders are available and created in the 
    users home directory.    
    """

    dir_ = os.path.expanduser('~') + '/SimplePass/'
    dir_import = dir_ + '/import/'
    dir_store = dir_ + '/store/'
   
    if not os.path.exists(dir_):
        try:  
            os.mkdir(dir_)
        except OSError:  
            print ("Creation of the directory %s failed" % dir_)
        else:  
            print ("Successfully created the directory %s " % dir_)
            os.mkdir(dir_import)
            os.mkdir(dir_store)
    else:
        print('%s already exists.' % dir_)


if __name__ == '__main__':
    create_folders()