# Treep, copyright 2019 Max Planck Gesellschaft
# Author : Vincent Berenz 

# This file is part of Treep.

#    Treep is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    Treep is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with Treep.  If not, see <https://www.gnu.org/licenses/>.


import os
from repository import Repository
from project import Project
from projects import Projects
from configuration import Configuration
from exceptions import TreepConfigFolderNotFound

try :
    import yaml
except:
    raise Exception("failed to import pyyaml. You may try:  pip install pyyaml")

import repository


CONFIG_FOLDER_PREFIX = "treep_"
REPOSITORIES_FILE = "repositories.yaml"
PROJECTS_FILE = "projects.yaml"
CONFIGURATION_FILE = "configuration.yaml"


def _find_root(starting_dir=None):

    def _found(path):
        global CONFIG_FOLDER_PREFIX
        files  = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
        treep_folders = [f for f in files if f.startswith(CONFIG_FOLDER_PREFIX)]
        if len(treep_folders)==0 :
            return None
        return treep_folders
        
    if starting_dir is None:
        starting_dir = os.getcwd()

    current_dir = starting_dir

    config_folders = _found(current_dir)
    while not config_folders:
        try :
            current_dir = os.path.abspath(current_dir+os.sep+"..")
            if current_dir == "/":
                return None,None
            config_folders = _found(current_dir)
        except:
            return None,None

    return current_dir,config_folders


def _relative_to_absolute_path(path):

    global REPOSITORIES_FILE
    starting_path = os.getcwd()
    root,_ = _find_root(REPOSITORIES_FILE)
    if root is None:
        raise Exception("failed to find treep root containing "+starting_path)
    return os.path.abspath(root+os.sep+path)


def _get_workspace_path():

    root,_ = _find_root()
    return root+os.sep+"workspace"+os.sep


def _yaml_to_repositories(yaml_content,configuration):

    valid_keys = ['origin','path','branch','commit','tag']

    repositories = []

    for repository,value in yaml_content.iteritems():
        
        for key in value.keys():
            if key not in valid_keys:
                raise Exception('invalid key for repository '+repository+": "+key)
        
        try :
            path = value['path']
        except :
            raise Exception("failed to find path for repository "+repository)

        try :
            origin = value['origin']
            origin = configuration.get_origin(repository,origin)
        except :
            origin = configuration.get_origin(repository,None)

        try :
            branch = value['branch']
        except :
            branch = 'master'

        try :
            commit = value['commit']
        except :
            commit = None

        try :
            tag = value['tag']
        except :
            tag = None
            
        repositories.append( Repository ( repository,
                                          origin,
                                          path,
                                          branch=branch,
                                          commit=commit,
                                          tag=tag ) )
        
    return repositories

        
def _yaml_to_configuration(yaml_content):

    origin_prefixes = {}
    
    valid_fields = ["origin_prefixes"]

    for field in yaml_content:

        if field not in valid_fields:
            raise Exception("invalid field in treep configuration yaml file: "+str(field))

        if field == "origin_prefixes":

            origin_prefixes = yaml_content[field]

    return Configuration(origin_prefixes)

    
def _yaml_to_projects(yaml_content):

    valid_keys = ['repos','parent_projects']
    
    projects = []

    for project in yaml_content:
        
        for key in yaml_content[project].keys():
            if key not in valid_keys:
                raise Exception('invalid key for project '+project+": "+key)
        
        try :
            repos = yaml_content[project]['repos']
        except :
            repos = []

        try :
            parent_projects = yaml_content[project]['parent_projects']
        except :
            parent_projects = []
            
        projects.append( Project( project,
                                  parent_projects,
                                  repos) )

    return projects



def _read_yaml_file(configuration_folder,file_,optional=False):

    root,_  = _find_root()
    if root is None:
        global CONFIG_FOLDER_PREFIX
        raise Exception("failed to find treep root folder containing the prefix '"+CONFIG_FOLDER_PREFIX+"'")

    abs_path = os.path.abspath(root+os.sep+configuration_folder+os.sep+file_)
    if not os.path.isfile(abs_path):
        if optional:
            return None
        else:
            raise Exception(abs_path+" does not seem to exist")

    try :
        with open(abs_path,"r") as f:
            content = f.readlines()
    except Exception as e:
        raise Exception("failed to read file content "+abs_path+": "+str(e))

    try :
        content = yaml.load("\n".join(content))
    except Exception as e:
        raise Exception("failed to parse yaml file "+abs_path+": "+str(e))

    return content
    

def _read_configuration_file(configuration_folder):

    global CONFIGURATION_FILE

    yaml_content = _read_yaml_file(configuration_folder,CONFIGURATION_FILE,optional=True)
    if yaml_content is None:
        configuration = Configuration({})
    else:
        configuration = _yaml_to_configuration(yaml_content)
    return configuration


def _read_repositories_file(configuration_folder,configuration):

    global REPOSITORIES_FILE

    yaml_content = _read_yaml_file(configuration_folder,REPOSITORIES_FILE,optional=False)
    repositories = _yaml_to_repositories(yaml_content,configuration)
    return repositories


def _read_projects_file(configuration_folder):

    global PROJECTS_FILE

    yaml_content = _read_yaml_file(configuration_folder,PROJECTS_FILE,optional=False)
    projects = _yaml_to_projects(yaml_content)
    return projects


def _check_projects_composed_of_existing_repositories(projects,repositories):

    repo_names = repositories.keys()

    for project in projects.values():
        for repo in project.repositories:
            if repo not in repo_names:
                raise Exception("project "+project.name+" contains an unknown repository: "+repo)



            
    
def read_configuration_files():

    all_projects = {}
    all_repositories = {}

    _,configuration_folders = _find_root()

    if configuration_folders is None:
        raise TreepConfigFolderNotFound()
    
    all_projects = {}
    all_repositories = {}

    # reading all configuration folders, one by one
    for configuration_folder in configuration_folders :
        
        configuration = _read_configuration_file(configuration_folder)
        repositories = _read_repositories_file(configuration_folder,configuration)
        projects = _read_projects_file(configuration_folder)
        
        repositories = {r.name : r for r in repositories}
        projects = {p.name : p for p in projects}

        all_repositories[configuration_folder]=repositories
        all_projects[configuration_folder]=projects

    def _conflicts(config_folder_dict):
        keys_folder = {}
        for folder,dict_ in config_folder_dict.iteritems():
            for key in dict_.keys():
                try :
                    keys_folder[key].append(folder)
                except:
                    keys_folder[key]=[folder]
        r = {key:value for key,value in keys_folder.iteritems() if len(value)>1}
        return r
        
    # where some repositories/projects defined in more than one configuration folder ?
    # nothing solved, but keeping the trace of this
    conflicts_repositories = _conflicts(all_repositories)
    conflicts_projects = _conflicts(all_projects)

    def _merge(config_folder_dict):

        def _merge_dicts(d1,d2):
            for k,v in d2.iteritems():
                d1[k]=v
            return d1

        r = {}

        for d in config_folder_dict.values():
            r = _merge_dicts(r,d)

        return r

    # merging all configurations into one. If conflicts, only
    # one version of the repositories/projects is arbitrary kept
    all_repositories = _merge(all_repositories)
    all_projects = _merge(all_projects)

    # sanity check on projects: no unknown repository used in projects ?
    _check_projects_composed_of_existing_repositories(all_projects,all_repositories)
    
    workspace_path = _get_workspace_path()
    
    projects_ = Projects(all_projects,
                         all_repositories,
                         workspace_path,
                         conflicts_repositories,
                         conflicts_projects)
    
    return projects_
        


def generate_yaml_configuration_files(path,statuses,
                                      project_name="PROJECT",
                                      commit=False):


    def get_relative_path(abs_path):
        index_workspace = abs_path.index("workspace")
        return abs_path[index_workspace+10:]
    
    # annoyed I need to write the yaml file "manually", but
    # pyyaml throws a "NoneType" exception

    file_repos = path+os.sep+'treep_repositories.generated'
    
    with open(file_repos, 'w+') as f:

        for status in statuses:

            f.write(status.repo_name+":\n")
            f.write("    path: "+get_relative_path(status.path)+"\n")
            f.write("    origin: "+str(status.origin)+"\n")
            f.write("    branch: "+status.branch+"\n")

            if commit:
                f.write("    commit: "+status.commit+"\n")

            if commit:
                values['commit'] = status.commit

                content_repositories[status.repo_name] = values

    file_projects = path+os.sep+'treep_projects.generated'
        
    with open(file_projects, 'w+') as f:

        f.write(project_name+":\n")
        f.write("    repos: "+repr([status.repo_name for status in statuses]))

    
    return file_repos,file_projects
