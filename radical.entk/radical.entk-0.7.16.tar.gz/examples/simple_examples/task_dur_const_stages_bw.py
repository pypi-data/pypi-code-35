from radical.entk import Pipeline, Stage, Task, AppManager, ResourceManager
import os, sys

# ------------------------------------------------------------------------------
# Set default verbosity

if not os.environ.get('RADICAL_ENTK_VERBOSE'):
    os.environ['RADICAL_ENTK_VERBOSE'] = 'INFO'

if not os.environ.get('RADICAL_PILOT_DBURL'):
    os.environ['RADICAL_PILOT_DBURL'] = "mongodb://138.201.86.166:27017/ee_exp_4c"

CUR_STAGE = 1
MAX_NUM_TASKS = 8
CUR_TASKS = 4
CUR_CORES = MAX_NUM_TASKS/CUR_TASKS
MAX_STAGES = 1

def generate_pipeline():
    
    def func_condition():

        global CUR_STAGE
    
        if CUR_STAGE <= MAX_STAGES:
            CUR_STAGE += 1
            return True

        return False

    def func_on_true():

        global CUR_STAGE, CUR_TASKS, CUR_CORES, p
        CUR_TASKS = CUR_TASKS*2
        CUR_CORES = CUR_CORES/2

        s = Stage()

        for i in range(CUR_TASKS):
            t = Task()    
            #t.pre_exec = ['module swap PrgEnv-pgi PrgEnv-gnu','module load fftw boost','export LD_LIBRARY_PATH="/ccs/proj/bip149/gromacs-nonmpi/lib64:$LD_LIBRARY_PATH:$CRAY_LD_LIBRARY_PATH"']
            #t.executable = ['/ccs/proj/bip149/gromacs-nonmpi/bin/gmx_d']   
            #t.link_input_data = ['$SHARED/index.ndx','$SHARED/input.gro','$SHARED/topol.top','$SHARED/grompp.mdp']
            #t.link_input_data = ['$SHARED/topol.tpr']
            #t.arguments = ['grompp','-n','index.ndx','-f','grompp.mdp','-c','input.gro','-maxwarn','1'] 
            #t.arguments = ['mdrun','-ntomp',CUR_CORES,'-nt',CUR_CORES,'-pin','on','-pinoffset','0']
            t.executable = ['/bin/sleep']
            t.arguments = ['30']
            t.cores = CUR_CORES

            # Add the Task to the Stage
            s.add_tasks(t)

        # Add post-exec to the Stage
        s.post_exec = {
                       'condition': func_condition,
                       'on_true': func_on_true,
                       'on_false': func_on_false
                    }

        p.add_stages(s)

    def func_on_false():
        print 'Done'

    # Create a Pipeline object
    p = Pipeline()

    # Create a Stage object 
    s1 = Stage()

    for i in range(CUR_TASKS):

        t1 = Task()    
        #t1.pre_exec = ['module swap PrgEnv-pgi PrgEnv-gnu','module load fftw boost','export LD_LIBRARY_PATH="/ccs/proj/bip149/gromacs-nonmpi/lib64:$LD_LIBRARY_PATH:$CRAY_LD_LIBRARY_PATH"']
        #t1.executable = ['/ccs/proj/bip149/gromacs-nonmpi/bin/gmx_d']   
        #t1.arguments = ['grompp','-n','index.ndx','-f','grompp.mdp','-c','input.gro','-maxwarn','1']
        #t1.arguments = ['mdrun','-nt',CUR_CORES,'-ntomp',CUR_CORES,'-pin','on','-pinoffset','0']
        #t1.link_input_data = ['$SHARED/index.ndx','$SHARED/input.gro','$SHARED/topol.top','$SHARED/grompp.mdp']
        t1.executable = ['/bin/sleep']
        t1.arguments = ['30']
        #t1.link_input_data = ['$SHARED/topol.tpr']
        t1.cores = CUR_CORES

        # Add the Task to the Stage
        s1.add_tasks(t1)

    # Add post-exec to the Stage
    s1.post_exec = {
                       'condition': func_condition,
                       'on_true': func_on_true,
                       'on_false': func_on_false
                   }

    # Add Stage to the Pipeline
    p.add_stages(s1)    

    return p

if __name__ == '__main__':

    duration = 30

    # Create a dictionary describe four mandatory keys:
    # resource, walltime, cores and project
    # resource is 'local.localhost' to execute locally
    res_dict = {

            'resource': 'ncsa.bw',
            #'walltime': (MAX_STAGES*duration)/60 + 20,
            'walltime': 30,
            'cores': MAX_NUM_TASKS+16,
            'access_schema': 'gsissh',
            'project': 'gk4'
    }

    # Create Resource Manager object with the above resource description
    rman = ResourceManager(res_dict)
    #rman.shared_data = ['./index.ndx','./input.gro','./topol.top','./grompp.mdp']
    #rman.shared_data = ['./topol.tpr']

    # Create Application Manager
    #appman = AppManager(hostname='csc190specfem.marble.ccs.ornl.gov', port=30672)
    appman = AppManager()

    # Assign resource manager to the Application Manager
    appman.resource_manager = rman

    p = generate_pipeline()
    
    # Assign the workflow as a set of Pipelines to the Application Manager
    appman.assign_workflow(set([p]))

    # Run the Application Manager
    appman.run()

