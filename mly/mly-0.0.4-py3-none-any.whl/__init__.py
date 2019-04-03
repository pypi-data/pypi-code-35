# -*- coding: utf-8 -*-


import os

def CreateMLyWorkbench():
    
    if os.path.exists('MLy_Workbench'):
        print('MLy_Workbench already exists')
    else:
        os.makedirs('MLy_Workbench')
            
    os.system('cd MLy_Workbench')
    os.system('mkdir datasets')
    os.system('cd datasets')
    os.system('mkdir cbc noise burst')
    os.system('cd noise')
    os.system('mkdir optimal sudo_real real')
    os.system('cd ../..')
    os.system('mkdir trainings ligo_data injections')
    os.system('cd injections')
    os.system('mkdir cbcs bursts')
    os.system('cd ../..')
    print('Workbench is complete!')
     
    return

def nullpath():
    pwd=os.getcwd()
    if 'MLy_Workbench' in pwd:
        null_path=path.split('MLy_Workbench')[0]+'MLy_Workbench'
    else:
        null_path=''
        print('Warning: null_path is empty, you should run import mla, CreateMLyWorkbench()'
              +' to create a workbench or specify null_path value here to avoid FileNotFound errors.')
    return(null_path)