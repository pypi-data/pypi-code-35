#!/usr/bin/env python                                             
#                                                            _
# Simple ChRIS DS (Data Syntehsis) app demo
#
# (c) 2016 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#

import  os
import  shutil
import  time
import  sys
import  time
import  json

# import the Chris app superclass
from chrisapp.base import ChrisApp

Gstr_title = """
     _                 _          _                       
    (_)               | |        | |                      
 ___ _ _ __ ___  _ __ | | ___  __| |___  __ _ _ __  _ __  
/ __| | '_ ` _ \| '_ \| |/ _ \/ _` / __|/ _` | '_ \| '_ \ 
\__ \ | | | | | | |_) | |  __/ (_| \__ \ (_| | |_) | |_) |
|___/_|_| |_| |_| .__/|_|\___|\__,_|___/\__,_| .__/| .__/ 
                | |                          | |   | |    
                |_|                          |_|   |_|    

"""

Gstr_synopsis = """

    NAME

        simpledsapp.py

    SYNOPSIS

        simpledsapp.py                                                  \\
            [-v <level>] [--verbosity <level>]                          \\
            [--prefix <filePrefixString>]                               \\
            [--sleepLength <sleepLength>]                               \\
            [--version]                                                 \\
            [--man]                                                     \\
            [--meta]                                                    \\
            [--ignoreInputDir]                                          \\
            <inputDir>                                                  \\
            <outputDir> 

    BRIEF EXAMPLE

        * To copy some input directory to an output directory:

            mkdir out
            python simpledsapp.py   /tmp \\
                                    out

    DESCRIPTION

        `simpledsapp.py` basically does an explicit copy of each file in 
        an input directory to the output directory, prefixing an optional
        string to each filename.

    ARGS

        [--prefix <prefixString>]
        If specified, a prefix string to append to each file copied.

        [--sleepLength <sleepLength>]
        If specified, sleep for <sleepLength> seconds before starting
        script processing. This is to simulate a possibly long running 
        process.

        [-v <level>] [--verbosity <level>]
        Verbosity level for app. Not used currently.

        [--version]
        If specified, print version number. 
        
        [--man]
        If specified, print (this) man page.

        [--meta]
        If specified, print plugin meta data.

        [--ignoreInputDir] 
        If specified, ignore the input directory. Simply write a single json file
        to the output dir that is a timestamp.
"""

class SimpleDSApp(ChrisApp):
    """
    Add prefix given by the --prefix option to the name of each input file.
    """
    AUTHORS                 = 'FNNDSC (dev@babyMRI.org)'
    SELFPATH                = os.path.dirname(os.path.abspath(__file__))
    SELFEXEC                = os.path.basename(__file__)
    EXECSHELL               = 'python3'
    TITLE                   = 'Simple chris ds app'
    CATEGORY                = ''
    TYPE                    = 'ds'
    DESCRIPTION             = 'A simple chris ds app demo'
    DOCUMENTATION           = 'https://github.com/FNNDSC/pl-simpledsapp'
    LICENSE                 = 'Opensource (MIT)'
    VERSION                 = '1.0.0'
    MAX_NUMBER_OF_WORKERS   = 1     # Override with integer value
    MIN_NUMBER_OF_WORKERS   = 1     # Override with integer value
    MAX_CPU_LIMIT           = ''    # Override with millicore value as string, e.g. '2000m'
    MIN_CPU_LIMIT           = ''    # Override with millicore value as string, e.g. '2000m'
    MAX_MEMORY_LIMIT        = ''    # Override with string, e.g. '1Gi', '2000Mi'
    MIN_MEMORY_LIMIT        = ''    # Override with string, e.g. '1Gi', '2000Mi'
    MIN_GPU_LIMIT           = 0     # Override with the minimum number of GPUs, as an integer, for your plugin
    MAX_GPU_LIMIT           = 0     # Override with the maximum number of GPUs, as an integer, for your plugin


    # Fill out this with key-value output descriptive info (such as an output file path
    # relative to the output dir) that you want to save to the output meta file when
    # called with the --saveoutputmeta flag
    OUTPUT_META_DICT = {}

    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        """
        self.add_argument('--prefix', 
                           dest         = 'prefix', 
                           type         = str, 
                           optional     = True,
                           help         = 'prefix for file names',
                           default      = '')
        self.add_argument('--ignoreInputDir',
                           dest         = 'b_ignoreInputDir',
                           type         = bool,
                           optional     = True,
                           help         = 'if set, ignore the input dir completely',
                           action       = 'store_true',
                           default      = False)
        self.add_argument('--sleepLength',
                           dest         = 'sleepLength',
                           type         = str,
                           optional     = True,
                           help         = 'time to sleep before performing plugin action',
                           default      = '0')
        self.add_argument('--dummyInt',
                           dest         = 'dummyInt',
                           type         = int,
                           optional     = True,
                           help         = 'dummy integer parameter',
                           default      = 1)
        self.add_argument('--dummyFloat',
                           dest         = 'dummyFloat',
                           type         = float,
                           optional     = True,
                           help         = 'dummy float parameter',
                           default      = 1.1)
        self.add_argument('--version',
                            help        = 'if specified, print version number',
                            type        = bool,
                            dest        = 'b_version',
                            action      = 'store_true',
                            optional    = True,
                            default     = False)
        self.add_argument('--man',
                            help        = 'if specified, print man page',
                            type        = bool,
                            dest        = 'b_man',
                            action      = 'store_true',
                            optional    = True,
                            default     = False)
        self.add_argument('--meta',
                            help        = 'if specified, print plugin meta data',
                            type        = bool,
                            dest        = 'b_meta',
                            action      = 'store_true',
                            optional    = True,
                            default     = False)

    def manPage_show(self):
        """
        Print some quick help.
        """
        print(Gstr_synopsis)

    def metaData_show(self):
        """
        Print the plugin meta data
        """
        l_metaData  = dir(self)
        l_classVar  = [x for x in l_metaData if x.isupper() ]
        for str_var in l_classVar:
            str_val = getattr(self, str_var)
            print("%20s: %s" % (str_var, str_val))


    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        if options.b_man:
            self.manPage_show()
            sys.exit(0)

        if options.b_meta:
            self.metaData_show()
            sys.exit(0)

        if options.b_version:
            print('Plugin Version: %s' % SimpleDSApp.VERSION)
            sys.exit(0)

        print(Gstr_title)
        print('Version: %s' % SimpleDSApp.VERSION)
        print('Sleeping for %s' % options.sleepLength)
        time.sleep(int(options.sleepLength))
        if options.b_ignoreInputDir:
            # simply create a timestamp in the output dir
            d_timeStamp = {
                'year':     time.strftime('%Y'),
                'month':    time.strftime('%m'),
                'day':      time.strftime('%d'),
                'hour':     time.strftime('%H'),
                'minute':   time.strftime('%M'),
                'second':   time.strftime('%S'),
            }
            print('Saving timestamp object')
            print(json.dumps(d_timeStamp, indent = 4))
            with open('%s/timestamp.json' % options.outputdir, 'w') as f:
                json.dump(d_timeStamp, f, indent = 4)
        else:
            for (dirpath, dirnames, filenames) in os.walk(options.inputdir):
                relative_path  = dirpath.replace(options.inputdir, "").strip("/")
                output_path =  os.path.join(options.outputdir, relative_path)
                for dirname in dirnames:
                    print('Creating directory... %s' % os.path.join(output_path, dirname))
                    os.makedirs(os.path.join(output_path, dirname))
                for name in filenames:
                    new_name    = options.prefix + name
                    str_outpath = os.path.join(output_path, new_name)
                    print('Creating new file... %s' % str_outpath)
                    shutil.copy(os.path.join(dirpath, name), str_outpath)

# ENTRYPOINT
if __name__ == "__main__":
    app = SimpleDSApp()
    app.launch()
