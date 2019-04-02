def exit_application(text = None):
    if(text != None):
        print (text)
    exit(0)

def register_error(error_string, print_error = True):
    if(print_error == True):
        print ("Error Encountered <%s>" % error_string)

def input_version(format = ">> "):
    import sys
    # print (sys.version_info)[0]
    if(sys.version_info[0] == 2):
        return_value = input(format)
    elif(sys.version_info[0] == 3):
        return_value = input(format)
    return return_value

def get_input(format=">> ",text = None, can_exit=True,exit_input="exit",valid_options=[], return_type = str, check=False):





    if(text!=None):
        print (text)

    if(check):
        while True:
            user_input = input_version(format)
            if(valid_options != []):
                if(return_type == int):
                    try:
                        user_input = int(user_input)
                        if(user_input in valid_options):
                            break
                        else:
                            register_error("Not valid Entry")
                            continue
                    except:
                        register_error("Not Valid Entry")
                        continue
                elif(return_type == str):
                    if(user_input in valid_options):
                        break
                    else:
                        register_error("Not Valid Entry")
                        continue
                else:
                    register_error("Not valid return_type")
                    continue
            else:
                break


    else:
        user_input = input_version(format)

        if(user_input == exit_input):
            if (can_exit):
                exit_application()
            else:
                register_error("Can't exit application now")

    return user_input

def clear(n=3):
    print ("\n"*n)

class Credits:
    def __init__(self,authors = [], company_name = "",team_name = "", github_account="", email_address=""):
        self.authors = authors
        self.company_name = company_name
        self.team_name = team_name
        self.github_account = github_account
        self.email_address = email_address


    def print_credits(self):
        clear(100)
        print (">> Credits <<")
        if(self.company_name != ""):
            print ("Company: %s"%self.company_name)
        if(self.team_name != ""):
            print ("Developed by %s"%self.team_name)
        if(len(self.authors)!=0):
            print ("\nAuthors:")
            for author in self.authors:
                print ("\t-%s" % author)
        print
        if(self.email_address != ""):
            print ("Email: %s" % self.email_address)
        if(self.github_account != ""):
            print ("GitHub: %s" % self.github_account)
        input("\nPress Enter to Continue...")

class Menu_Func:
    def __init__(self,title=None,function=None,*args):
        self.function = function
        self.title = title
        self.args = args

    def print_function_info(self):
        print ("Function: %s" % self.function)

        for parameter in self.args:
            print (parameter)

    def get_unassigned_params(self):
        unassigned_parameters_list = []
        for parameter in self.function.func_code.co_varnames:
            if not parameter in (self.args):
                print (parameter)
                unassigned_parameters_list.append(parameter)
        return unassigned_parameters_list

    def get_args(self):
        print (self.args)
        return self.args

    def call_function(self):
        self.function(*self.args)

class Menu:

    def __init__(self,title = None, subtitle = None,text = None,options=[],return_type=int,parent=None,input_each = False,previous_menu=None,back=True):
        self.title = title
        self.subtitle = subtitle
        self.text = text
        self.options = options
        self.return_type = return_type
        self.parent = parent
        self.input_each = input_each
        self.previous_menu = previous_menu
        self.back = back
        self.returned_value = None

    def set_parent(self,parent):
        self.parent = parent

    def set_previous_menu(self,previous_menu):
        self.previous_menu = previous_menu



    def get_selection(self, exit_input="exit"):

        start_index = 1
        if(self.back):
            start_index=0


        # if there exist options it means user have to select one of them
        if((self.options.__len__()!=0) and (not self.input_each)):

            while True:

                selection = get_input()

                if(selection.__str__().isdigit()):
                    if(int(selection) in range(start_index,(self.options.__len__())+1)):
                        if(int(selection) != 0):
                            if (isinstance(self.options[int(selection) - 1], Menu_Func)):
                                function = self.options[int(selection) - 1]
                                function.call_function()
                            elif (isinstance(self.options[int(selection) - 1], Menu)):
                                sub_menu = self.options[int(selection) - 1]
                                sub_menu.set_parent(self)
                                sub_menu.show()
                        else:
                            if(self.parent != None):
                                self.parent.set_previous_menu(self)
                                self.parent.show()
                        break
                    else:
                        register_error("Index not in range")

                else:
                    register_error("Entered must be int.")

        elif(self.input_each):
            selection = []
            for option in self.options:
                parameter_value = get_input(str(option)+" >> ")
                selection.append(parameter_value)

        # if there aren't any option it means user must input a string
        else:
            selection = get_input()

        self.returned_value = selection
        return selection



    def show(self):
        # if(self.previous_menu != None) and (self != self.previous_menu):
        #     del(self.previous_menu)
        clear()
        if(self.title != None):
            print ("/// %s " % self.title)
        if (self.subtitle != None):
            print ("///%s" % self.subtitle)
        print
        if (self.text != None):
            print (self.text)

        # print "Parent:",self.parent


        if(self.options.__len__()!=0 and (not self.input_each)):
            for option_index in range(len(self.options)):
                if isinstance(self.options[option_index], Menu_Func):
                    print ("%s. %s" % (str(option_index + 1), self.options[option_index].title))
                elif isinstance(self.options[option_index],Menu):
                    print ("%s. %s"%(str(option_index+1),self.options[option_index].title))
                else:
                    print ("%s. %s"%(str(option_index+1),self.options[option_index]))
            if (self.back):
                print ("0. Back")

        selected_option = self.get_selection()
        return selected_option

class Directory_Manager:


    class File:
        def __init__(self, path, name, extension, size):
            self.path = path
            self.name = name
            self.extension = extension
            self.size = size
        def print_info(self):
            print ("Name:",self.name)
            print ("Path:",self.path)
            print ("Extension:",self.extension)
            print ("Size:",self.size)
            print

    def __init__(self,directories = []):
        self.directories = directories
        self.files = []
        self.get_files()
    def get_dirs(self):
        dirs_list = []
        for file in self.files:
            dirs_list.append(file.path)
        return dirs_list

    def get_files(self):
        import os
        def create_file(directory,file_name=None):

            file_dir = directory
            if(file_name != None):
                file_dir += "/" + file_name
            else:
                file_name = file_dir.rsplit('/',1)[-1]

            file = self.File(file_dir, file_name, file_name.rsplit('.', 1)[-1], os.path.getsize(file_dir))
            self.files.append(file)

        for directory in self.directories:
            if(os.path.isdir(directory)):
                if(os.path.exists(directory)):
                    for file_name in os.listdir(directory):
                        create_file(directory,file_name)
                else: register_error("Path \"%s\" doesn't exists" % directory)
            elif(os.path.isfile(directory)):
                create_file(directory=directory)
            else:
                register_error("Path \"%s\" not found" % directory)

    def print_info(self):
        for file in self.files:
            file.print_info()

    def filter_format(self,extensions = []):
        new_files = []
        for file in self.files:
            if (file.extension in extensions):
                new_files.append(file)
        self.files = new_files

    def create_directory(self,directory):
        import os
        os.makedirs(directory)

    def open_file(self, path):
        import platform,os,subprocess
        current_os = platform.system()
        print ("current os %s" % current_os)

        if(os.path.isfile(path)):

            if (current_os == 'Linux'):
                subprocess.call(('xdg-open',path))
            elif (current_os == 'Windows'):
                os.startfile("\'%s\'" % path)
            elif (current_os == "Darwin"):
                subprocess.call(('open',path))
            else:
                register_error("OS not supported")

        else:
            register_error("File \"%s\" not found" % path)

