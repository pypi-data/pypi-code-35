from radical.entk import Pipeline, Stage, Task, AppManager, ResourceManager
import os

# ------------------------------------------------------------------------------
# Set default verbosity

if os.environ.get('RADICAL_ENTK_VERBOSE') == None:
    os.environ['RADICAL_ENTK_VERBOSE'] = 'INFO'


def generate_pipeline():
    
    # Create a Pipeline object
    p = Pipeline()

    # Create a Stage object 
    s1 = Stage()

    # Create a Task object which creates a file named 'output.txt' of size 1 MB
    t1 = Task()    
    t1.executable = ['/bin/bash']   
    t1.arguments = ['-l', '-c', 'base64 /dev/urandom | head -c 1000000 > output.txt'] 
    t1.cpu_reqs = { 'processes': 1, 
                    'process_type': None, 
                    'threads_per_process': 1, 
                    'thread_type': None}
    t1.gpu_reqs = { 'processes': 1, 
                    'process_type': None, 
                    'threads_per_process': 1, 
                    'thread_type': None}

    # Add the Task to the Stage
    s1.add_tasks(t1)

    # Add Stage to the Pipeline
    p.add_stages(s1)

    return p

if __name__ == '__main__':


    # Create a dictionary describe four mandatory keys:
    # resource, walltime, cores and project
    # resource is 'local.localhost' to execute locally
    res_dict = {

            'resource': 'ncsa.bw_aprun',
            'walltime': 10,
            'cpus': 32,
            'gpus': 2,
            #'project': 'gk4',
            'project': 'bamm'
    }

    # Create Resource Manager object with the above resource description
    rman = ResourceManager(res_dict)

    # Create Application Manager
    appman = AppManager(autoterminate=False)

    # Assign resource manager to the Application Manager
    appman.resource_manager = rman

    p = generate_pipeline()
    
    # Assign the workflow as a set of Pipelines to the Application Manager
    appman.assign_workflow(set([p]))

    # Run the Application Manager
    appman.run()

    p = generate_pipeline()
    print p.uid

    # Assign the workflow as a set of Pipelines to the Application Manager
    appman.assign_workflow(set([p]))

    # Run the Application Manager
    appman.run()

    appman.resource_terminate()

