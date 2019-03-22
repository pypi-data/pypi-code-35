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


from __future__ import print_function


import os
import treep_git
import status
import coloring
from console_manager import Console_manager


class UnknownProject(Exception):
    pass

class UnknownRepository(Exception):
    pass


INFO=-1
ERROR = 0
WARNING = 1
OK = 2


class Projects :


    def __init__( self,
                  projects,
                  repositories,
                  workspace_path,
                  conflicts_projects,
                  conflicts_repositories ):

        self._projects = projects
        self._repositories = repositories
        self._workspace_path = workspace_path
        self._conflicts_projects = conflicts_projects
        self._conflicts_repositories = conflicts_repositories

        project_names = [project.name for project in self._projects.values()]
        for project in self._projects.values():
            for parent in project.parent_projects:
                if parent not in project_names:
                    raise UnknownProject(parent)


    def get_conflicts(self):
        return self._conflicts_repositories,self._conflicts_projects

    def display_conflicts(self):

        if not self.has_conflicts():
            print(coloring.b_green("\n\t\tno conflicts detected\n"))
            return

        if self._conflicts_repositories:
            print(coloring.b_orange("\t\tREPOSITORIES:"))
            for repo,folders in self._conflicts_repositories.iteritems():
                print("\t\t\t"+coloring.cyan(repo)+" defined in "+", ".join(folders))
            print('')
            
        if self._conflicts_projects:
            print(coloring.b_orange("\t\tprojects:"))
            for project,folders in self._conflicts_projects.iteritems():
                print("\t\t\t"+coloring.cyan(project)+" defined in "+", ".join(folders))
            print('')


            
    def has_conflicts(self):
        if len(self._conflicts_repositories) != 0:
            return True
        if len(self._conflicts_projects) != 0:
            return True
        return False

    def get_workspace_path(self):

        return self._workspace_path


    def get_nb_projects(self):

        return len(self._projects)

    
    def get_nb_repos(self):

        return len(self._repositories)
    
    
    def get_project(self,project_name):

        try :
            return self._projects[project_name]
        except :
            raise UnknownProject(project_name)


    def get_repo(self,repo_name):

        try :
            return self._repositories[repo_name]
        except :
            raise UnknownRepository(repo_name)


    def get_projects(self):
        for project in self._projects.values():
            yield project


    def get_projects_names(self):
        return self._projects.keys()

    
    def get_repos_names(self):
        return self._repositories.keys()


    def get_names(self):
        return self.get_projects_names() + self.get_repos_names()
    
    def get_repos(self,project_name):

        if project_name is None:
            return self._repositories.values()
            
        project = self.get_project(project_name)
        repos = set(project.repositories)
        for parent_project in project.parent_projects:
            instance = self.get_project(parent_project)
            repos.update(instance.repositories)
        return repos


    def has_repo(self,project_name,repo_name):

        return repo_name in self.get_repos(project_name)


    def already_cloned(self,repo_name):

        repo = self.get_repo(repo_name)
        abs_path  = self.get_repo_path(repo_name)
        if os.path.isdir(abs_path):
            return True
        return False


    def pretty_print_repo(self,repo_name,nb_tabs=0):

        already_cloned = self.already_cloned(repo_name)
        repo = self.get_repo(repo_name)
        
        print ('\t'*(nb_tabs+2),end='')
        if already_cloned:
            print (coloring.b_green(repo_name),end='\t')
        else :
            print (coloring.dim(repo_name),end='\t')
        print (coloring.cyan(repo.origin),end='\t')
        print (coloring.dim(repo.path),end='\n')

            
    def pretty_print_project(self,project_name,nb_tabs=1,printed_repos=None):
        
        project = self.get_project(project_name)
        printed_repos = set()
        nb_tabs_ = nb_tabs
        for parent_project in project.parent_projects:
            nb_tabs_ = self.pretty_print_project(parent_project,nb_tabs+1,printed_repos=printed_repos)
        nb_tabs_+=1
        print('\t'*nb_tabs_+coloring.b_cyan(project_name))
        for repo in project.repositories:
            if repo not in printed_repos:
                self.pretty_print_repo(repo,nb_tabs_)
                printed_repos.add(repo)
        return nb_tabs_
        
            
    def get_cloned_repos(self):

        r = []
        for repo_name in self._repositories.keys():
            if self.already_cloned(repo_name):
                r.append(repo_name)
        return r

    
    def get_repos_paths(self,repo_names):

        r = {}
        for repo_name in repo_names:
            instance = self.get_repo(repo_name)
            absolute_path = self._workspace_path+instance.path+os.sep+instance.name
            r[repo_name] = absolute_path
        return r


    def get_repo_path(self,repo_name):

        return self.get_repos_paths([repo_name]).values()[0]
        

    def add_and_commit(self,
                       project_or_repo_name,
                       commit_message,
                       console=True,
                       raise_exception=False):

        if console:
            console_manager = Console_manager()
            print(coloring.b_green("\n\tadding and commiting"))
        
        if project_or_repo_name is None:
            repos = self.get_cloned_repos()
        elif project_or_repo_name in self._projects.keys() :
            repos = self.get_repos(project_or_repo_name)
        else :
            if project_or_repo_name not in self._repositories.keys():
                raise UnknownRepository(project_or_repo_name)
            repos = [project_or_repo_name]

        for repo in repos:

            path = self.get_repo_path(repo)

            if console :
                print("\t\t"+coloring.cyan(repo)+" ... ",end='')

            local_modifications = treep_git.local_modifications(path)

            if not local_modifications:
                print (coloring.orange("no local modifications"))

            else :
                
                try :
                    nb_added = treep_git.add_all(path)
                    added = True
                except Exception as e:
                    added = False
                    if console:
                        print (coloring.red("ERROR"))
                        console_manager.add_error(repo,str(e))
                    else :
                        if raise_exception:
                            raise e

                if added :

                    try :
                        treep_git.commit(path,commit_message)
                        if console:
                            if nb_added == 0:
                                print (coloring.dim("no file added"))
                            else :
                                if nb_added == 1:
                                    file_ = "file"
                                else :
                                    file_ = "files"
                                print (coloring.green(str(nb_added)+" "+file_+" added"))

                    except Exception as e:
                        if console:
                            print (coloring.red("ERROR"))
                            console_manager.add_error(repo,str(e))
                        else :
                            if raise_exception:
                                raise e

        if console:
            console_manager.console()

            
    def push(self,
             project_or_repo_name,
             console=True,
             raise_exception=False):

        if console:
            console_manager = Console_manager()
            print(coloring.b_green("\n\tpushing"))
        
        if project_or_repo_name is None:
            repos = self.get_cloned_repos()
        elif project_or_repo_name in self._projects.keys() :
            repos = self.get_repos(project_or_repo_name)
        else :
            if project_or_repo_name not in self._repositories.keys():
                raise UnknownRepository(project_or_repo_name)
            repos = [project_or_repo_name]

        for repo in repos:

            path = self.get_repo_path(repo)
            
            if console :
                print("\t\t"+coloring.cyan(repo)+" ... ",end='')

            try :
                current_branch = treep_git.current_branch(path)
                treep_git.push_to_origin(path,current_branch)
                print (coloring.green("OK"))
            except Exception as e:
                if console:
                    print (coloring.red("ERROR"))
                    console_manager.add_error(repo,str(e))
                else :
                    if raise_exception:
                        raise e
                    
            
        if console:
            console_manager.console()


    def clone( self,
               project_or_repo_name,
               console=True,
               branch=True,
               commit=True,
               tag=True ):

        if not os.path.isdir(self._workspace_path):
            try :
                os.makedirs(self._workspace_path)
            except Exception as e:
                raise Exception("failed to create workspace "+self._workspace_path+": "+str(e))
        
        if console:
            console_manager = Console_manager()
            print(coloring.b_green("\n\tcloning"))
        
        if project_or_repo_name in self._projects.keys() :
            repos = self.get_repos(project_or_repo_name)
        else :
            if project_or_repo_name not in self._repositories.keys():
                raise UnknownRepository(project_or_repo_name)
            repos = [project_or_repo_name]

        for repo in repos:

            instance = self.get_repo(repo)
            absolute_path = self.get_repo_path(repo)

            if self.already_cloned(repo):
                if console:
                    print(coloring.dim("\t\t"+repo+" already cloned, doing nothing"))

            else :
                if console:
                    print("\t\t"+coloring.cyan(repo)+" ... ",end='')
                try :
                    treep_git.clone(instance.origin,absolute_path)
                    clone_ok = True
                    if console:
                        print (coloring.green("OK"))
                except Exception as e :
                    clone_ok = False
                    if console:
                        print (coloring.red("ERROR"))
                        console_manager.add_error(repo,str(e))
                    else :
                        raise e

                if clone_ok:

                    if branch and instance.branch is not None and instance.branch != "master":
                        print (coloring.dim("\t\t\tchecking out "),end='')
                        print (coloring.cyan(instance.branch)+" ... ",end='')
                        try :
                            treep_git.checkout_branch(absolute_path,instance.branch,create=True)
                            print (coloring.green("OK"))
                        except Exception as e:
                            if console:
                                print (coloring.red("ERROR"))
                                console_manager.add_error(instance.name,str(e))
                            else:
                                if raise_exception:
                                    raise e
                                
                    if tag and instance.tag is not None :
                        print (coloring.dim("\t\t\tchecking out "),end='')
                        print (coloring.cyan(instance.tag)+" ... ",end='')
                        try :
                            treep_git.checkout_tag(absolute_path,instance.tag)
                            print (coloring.green("OK"))
                        except Exception as e:
                            if console:
                                print (coloring.red("ERROR"))
                                console_manager.add_error(repo_name,str(e))
                            else:
                                if raise_exception:
                                    raise e

                    elif commit and instance.commit is not None:
                        print (coloring.dim("\t\t\tchecking out "),end='')
                        print (coloring.cyan(instance.tag)+" ... ",end='')
                        try :
                            treep_git.checkout_commit(absolute_path,instance.commit)
                            print (coloring.green("OK"))
                        except Exception as e:
                            if console:
                                print (coloring.red("ERROR"))
                                console_manager.add_error(repo_name,str(e))
                            else:
                                if raise_exception:
                                    raise e


        if console:
            console_manager.console()
                               

    def pull(self,project_or_repo_name,console=True,raise_exception=False):

        if console:
            console_manager = Console_manager()
            print(coloring.b_green("\n\tpulling"))

        if project_or_repo_name is None:
            repos = self.get_cloned_repos()
        elif project_or_repo_name in self._projects.keys() :
            repos = self.get_repos(project_or_repo_name)
        else :
            if project_or_repo_name not in self._repositories.keys():
                raise UnknownRepository(project_or_repo_name)
            repos = [project_or_repo_name]

        for repo in repos:

            if console:
                print("\t\t"+coloring.cyan(repo)+" ... ",end='')
            try :
                instance = self.get_repo(repo)
                absolute_path = self.get_repo_path(repo)
                treep_git.pull(absolute_path)
                if console:
                    print (coloring.green("OK"))
            except Exception as e :
                if console:
                    print (coloring.red("ERROR"))
                    console_manager.add_error(repo,str(e))
                else :
                    if raise_exception:
                        raise e

        if console:
            console_manager.console()


            
    def list_branches(self,repo_name):

        repo_instance = self.get_repo(repo_name)
        absolute_path = self.get_repo_path(repo_name)
        branches = treep_git.list_branches(absolute_path)
        return branches
    

    def list_all_branches( self,
                           return_common_branches=False,
                           fetch_first=True,
                           console=True,
                           raise_exception=False ):

        if fetch_first:
            self.fetch_origin()
        
        cloned_repos =  self.get_cloned_repos()

        repo_branches = {}

        if console:
            console_manager = Console_manager()
            print(coloring.b_green("\n\tlisting branches"))

        
        for repo_name in cloned_repos:

            if console:
                print("\t\t"+coloring.cyan(repo_name)+" ... ",end='')
            
            try :
                branches = self.list_branches(repo_name)
                repo_branches[repo_name] = set(branches)
                if console:
                    print (coloring.green("OK"))
            except Exception as e:
                if console:
                    print (coloring.red("ERROR"))
                    console_manager.add_error(repo_name,str(e))
                else :
                    if raise_exception:
                        raise e

        if console or return_common_branches:
            if len(repo_branches.values())>0 :
                common_branches = repo_branches.values()[0].intersection(*[s for s in repo_branches.values()])
            else :
                commong_branches = set()

        if len(repo_branches.values())>0 :
            all_branches = repo_branches.values()[0].union(*[s for s in repo_branches.values()])
        else :
            all_branches = set()
            
        if console:
            print('')
            for repo,branches in repo_branches.iteritems():
                branches_str = [coloring.green(branch) if branch in common_branches
                                else branch for branch in branches]
                print ("\t\t"+coloring.cyan(repo)+": "+" ".join(branches_str))
            print('')

        if return_common_branches:
            return all_branches,common_branches

        return all_branches
                
            
    def get_all_existing_branches(self):

        workspace_path = self.get_workspace_path()
        if not os.path.isdir(workspace_path):
            return []
        
        return self.list_all_branches( return_common_branches=False,
                                       fetch_first=False,
                                       console=False,
                                       raise_exception=False )
            
    
    def checkout_branch(self,branch_name,
                        project_name=None,create=False,
                        console=True,raise_exception=False):

        if console:
            console_manager = Console_manager()
            print(coloring.b_green("\n\tchecking out branch "+coloring.cyan(branch_name)))

        
        if project_name is None:
            cloned_repos = self.get_cloned_repos()
        else :
            cloned_repos = self.get_repos(project_name)

        repo_paths = self.get_repos_paths(cloned_repos)

        for repo_name,path in repo_paths.iteritems():

            if console:
                print("\t\t"+coloring.cyan(repo_name)+" ... ",end='')
            
            branches = self.list_branches(repo_name)
            if not create:
                if branch_name in branches:
                    repo_instance = self.get_repo(repo_name)
                    absolute_path = self.get_repo_path(repo_instance.name)
                    try :
                        treep_git.checkout_branch(absolute_path,branch_name,create=False)
                        if console:
                            print (coloring.green("OK"))
                    except Exception as e:
                        if console:
                            print (coloring.red("ERROR"))
                            console_manager.add_error(repo_name,str(e))
                        else:
                            if raise_exception:
                                raise e
                else :
                    print (coloring.orange("no such branch"))            
            else :
                repo_instance = self.get_repo(repo_name)
                absolute_path = self.get_repo_path(repo_instance.name)
                try :
                    treep_git.checkout_branch(absolute_path,branch_name,create=True)
                    if console:
                        print (coloring.green("OK"))
                except Exception as e:
                    if console:
                        print (coloring.red("ERROR"))
                        console_manager.add_error(repo_name,str(e))
                    else:
                        if raise_exception:
                            raise e
        if console:
            console_manager.console()
                    

    def get_status(self,repo_name,fetch_first=True,
                   console=True,raise_exception=False):

        if fetch_first:
            self.fetch_origin(repo_name=repo_name,
                              console=console,
                              raise_exception=raise_exception)

        path = self.get_repo_path(repo_name)
        status = treep_git.get_status(path)
        return status
            
                
    def get_statuses(self,fetch_first=True):

        if fetch_first:
            self.fetch_origin()
        
        r = []

        for root,dirs,files in os.walk(self._workspace_path):
            for dir_ in dirs:
                if dir_!='.git':
                    status = treep_git.get_status(root+os.sep+dir_)
                    if status is not None:
                        r.append(status)

        return r


    def pretty_print_workspace(self):
        
        statuses = self.get_statuses()
        status.pretty_print(statuses,self._workspace_path)

    
    def fetch_origin(self,repo_name=None,console=True,raise_exception=False):

        if console:
            console_manager = Console_manager()
            print(coloring.b_green("\n\tfetching"))

        if repo_name is None:
            repo_names = self.get_cloned_repos()
        else :
            repo_names = [repo_name]
            
        for repo_name in repo_names:
            if console:
                print("\t\t"+coloring.cyan(repo_name)+" ... ",end='')
            try :
                instance = self.get_repo(repo_name)
                absolute_path = self._workspace_path+instance.path+os.sep+instance.name
                treep_git.fetch_origin(absolute_path)
                if console:
                    print(coloring.green("OK"))
            except Exception as e:
                if console:
                    print(coloring.red("ERROR"))
                    console_manager.add_error(repo_name,str(e))
                else :
                    if raise_exception:
                        raise e

        if console:
            console_manager.console()
            
                    

    
