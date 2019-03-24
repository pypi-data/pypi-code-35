#!/usr/bin/env python                                             
#               _
# z2labelmap ds app
#
# (c) 2019 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#

import  os
from    os                  import  listdir, sep
from    os.path             import  abspath, basename, isdir
from    distutils.dir_util  import  copy_tree
import  numpy               as      np
import  pandas              as      pd
import  csv
import  shutil
import  pudb
import  sys
import  time
import  random
import  copy

# import the Chris app superclass
from chrisapp.base import ChrisApp

Gstr_synopsis = """

    NAME

        z2labelmap.py

    SYNOPSIS

        python z2labelmap.py                                            \\
            [-v <level>] [--verbosity <level>]                          \\
            [--random]                                                  \\
            [-p <f_posRange>] [--posRange <f_posRange>]                 \\
            [-n <f_negRange>] [--negRange <f_negRange>]                 \\
            [-P <'RGB'>] [--posColor <'RGB'>]                           \\
            [-N  <'RGB'> [--negColor <'RGB'>]                           \\
            [-s <f_scaleRange>] [--scaleRange <f_scaleRange>]           \\
            [-l <f_lowerFilter>] [--lowerFilter <f_lowerFilter>]        \\
            [-u <f_upperFilter>] [--upperFilter <f_upperFilter>]        \\
            [-z <zFile>] [--zFile <zFile>]                              \\
            [--version]                                                 \\
            [--man]                                                     \\
            [--meta]                                                    \\
            <inputDir>                                                  \\
            <outputDir> 

    BRIEF EXAMPLE

        * To create a sample/random z-score file and analyze this 
          created file:

            mkdir in out
            python z2labelmap.py    --random                            \\
                                    --posRange 3.0 --negRange -3.0      \\
                                    in out

          In this example, z-scores range between 0.0 and (+/-) 3.0.

        * To analyze a file already located at 'in/zfile.csv', apply a 
          scaleRange and also filter out the lower 80\% of z-scores:

            python z2labelmap.py    --scaleRange 2.0 --lowerFilter 0.8  \\
                                    --negColor B --posColor R           \\
                                    in out

    DESCRIPTION

        `zlabelmap.py' generates FreeSurfer labelmaps from z-score vector
        files. Essentially the script consumes an input text vector file
        of 

            <str_structureName> <float_lh_zScore> <float_rh_zScore>

        and creates a FreeSurfer labelmap where <str_structureName> colors 
        correspond to the z-score (normalized between 0 and 255).

        Currently, only the 'aparc.a2009s' FreeSurfer segmentation is fully
        supported, however future parcellation support is planned.

        Negative z-scores and positive z-scores are treated in the same manner
        but have sign-specific color specifications.

        Positive and negative z-Scores can be assigned some combination of the
        chars 'RGB' to indicate which color dimension will reflect the z-Score.
        For example, a 
            
                --posColor R --negColor RG

        will assign positive z-scores shades of 'red' and negative z-scores 
        shades of 'yellow' (Red + Green = Yellow).

    ARGS

        <inputDir>
        Required argument.
        Input directory for plugin.

        <outputDir>
        Required argument.
        Output directory for plugin.

        [-v <level>] [--verbosity <level>]
        Verbosity level for app. Not used currently.

        [--random]
        If specified, generate a z-score file based on <posRange> and 
        <negRange>.

        [-p <f_posRange>] [--posRange <f_posRange>]
        Positive range for random max deviation generation.

        [-n <f_negRange>] [--negRange <f_negRange>]
        Negative range for random max deviation generation.

        [-P <'RGB'>] [--posColor <'RGB'>]
        Some combination of 'R', 'G', B' for positive heat.

        [-N  <'RGB'> [--negColor <'RGB'>]
        Some combination of 'R', 'G', B' for negative heat.

        [-s <f_scaleRange>] [--scaleRange <f_scaleRange>]
        Scale range for normalization. This has the effect of controlling 
        the brightness of the map. For example, if this 1.5 the effect
        is increase the apparent range by 50% which darkens all colors 
        values.

        [-l <f_lowerFilter>] [--lowerFilter <f_lowerFilter>]
        Filter all z-scores below (normalized) <lowerFilter> to 0.0.

        [-u <f_upperFilter>] [--upperFilter <f_upperFilter>]
        Filter all z-scores above (normalized) <upperFilter> to 0.0.

        [-z <zFile>] [--zFile <zFile>]
        z-score file to read (relative to input directory). Defaults to 
        'zfile.csv'.

        [--version]
        If specified, print version number. 
        
        [--man]
        If specified, print (this) man page.

        [--meta]
        If specified, print plugin meta data.

    EXAMPLE

        * Assuming a file called 'zfile.csv' in the <inputDirectory>
          that ranges in z-score between 0.0 and 3.0, use the --scaleRange
          to reduce the apparent brightness of the map by 50 percent and 
          also remove the lower 80 percent of zscores (this has the effect 
          of only showing the brightest 20 percent of zscores). 

        python z2labelmap.py    --scaleRange 2.0 --lowerFilter 0.8  \\
                                --negColor B --posColor R           \\
                                in out


"""

class Z2labelmap(ChrisApp):
    """
    Convert a file of per-structure z-scores to a FreeSurfer labelmap..
    """
    AUTHORS                 = 'FNNDSC (dev@babyMRI.org)'
    SELFPATH                = os.path.dirname(os.path.abspath(__file__))
    SELFEXEC                = os.path.basename(__file__)
    EXECSHELL               = 'python3'
    TITLE                   = 'z-score to FreeSurfer label map'
    CATEGORY                = 'FreeSurfer'
    TYPE                    = 'ds'
    DESCRIPTION             = 'Convert a file of per-structure z-scores to a FreeSurfer labelmap.'
    DOCUMENTATION           = 'http://wiki'
    VERSION                 = '1.1.6'
    ICON                    = '' # url of an icon image
    LICENSE                 = 'Opensource (MIT)'
    MAX_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MIN_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MAX_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MIN_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MAX_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_GPU_LIMIT           = 0  # Override with the minimum number of GPUs, as an integer, for your plugin
    MAX_GPU_LIMIT           = 0  # Override with the maximum number of GPUs, as an integer, for your plugin

    # Fill out this with key-value output descriptive info (such as an output file path
    # relative to the output dir) that you want to save to the output meta file when
    # called with the --saveoutputmeta flag
    OUTPUT_META_DICT = {}
 
    def a2009sStructList_define(self):
        """
        The list of structures in the a2009s cortical parcellation
        """

        self.l_a2009s = [
            'G_and_S_frontomargin',
            'G_and_S_occipital_inf',
            'G_and_S_paracentral',
            'G_and_S_subcentral',
            'G_and_S_transv_frontopol',
            'G_and_S_cingul-Ant',
            'G_and_S_cingul-Mid-Ant',
            'G_and_S_cingul-Mid-Post',
            'G_cingul-Post-dorsal',
            'G_cingul-Post-ventral',
            'G_cuneus',
            'G_front_inf-Opercular',
            'G_front_inf-Orbital',
            'G_front_inf-Triangul',
            'G_front_middle',
            'G_front_sup',
            'G_Ins_lg_and_S_cent_ins',
            'G_insular_short',
            'G_occipital_middle',
            'G_occipital_sup',
            'G_oc-temp_lat-fusifor',
            'G_oc-temp_med-Lingual',
            'G_oc-temp_med-Parahip',
            'G_orbital',
            'G_pariet_inf-Angular',
            'G_pariet_inf-Supramar',
            'G_parietal_sup',
            'G_postcentral',
            'G_precentral',
            'G_precuneus',
            'G_rectus',
            'G_subcallosal',
            'G_temp_sup-G_T_transv',
            'G_temp_sup-Lateral',
            'G_temp_sup-Plan_polar',
            'G_temp_sup-Plan_tempo',
            'G_temporal_inf',
            'G_temporal_middle',
            'Lat_Fis-ant-Horizont',
            'Lat_Fis-ant-Vertical',
            'Lat_Fis-post',
            'Pole_occipital',
            'Pole_temporal',
            'S_calcarine',
            'S_central',
            'S_cingul-Marginalis',
            'S_circular_insula_ant',
            'S_circular_insula_inf',
            'S_circular_insula_sup',
            'S_collat_transv_ant',
            'S_collat_transv_post',
            'S_front_inf',
            'S_front_middle',
            'S_front_sup',
            'S_interm_prim-Jensen',
            'S_intrapariet_and_P_trans',
            'S_oc_middle_and_Lunatus',
            'S_oc_sup_and_transversal',
            'S_occipital_ant',
            'S_oc-temp_lat',
            'S_oc-temp_med_and_Lingual',
            'S_orbital_lateral',
            'S_orbital_med-olfact',
            'S_orbital-H_Shaped',
            'S_parieto_occipital',
            'S_pericallosal',
            'S_postcentral',
            'S_precentral-inf-part',
            'S_precentral-sup-part',
            'S_suborbital',
            'S_subparietal',
            'S_temporal_inf',
            'S_temporal_sup',
            'S_temporal_transverse'
        ]
        maxlen          = len(max(self.l_a2009s, key = len))
        # Right pad the structure names with spaces to set all names to same length.
        self.l_a2009s   = [x + (' ' * (maxlen - len(x))) for x in self.l_a2009s]
        return self.l_a2009s

    def zScoreFile_read(self, astr_parcellation):
        """
        Read the z-score file in the input directory.
        """
        b_status    = False

        # pudb.set_trace()
        dframe      = pd.read_csv(
                        '%s/%s' % (self.options.inputdir, self.options.zFile),
                        header = None
                    )

        self.d_parcellation[astr_parcellation]['lh']['zScore'] = dframe.ix[:,1].tolist()
        self.d_parcellation[astr_parcellation]['rh']['zScore'] = dframe.ix[:,2].tolist()

        b_status    = True
        return {
            'status':   b_status
        }

    def zScore_processStats(self, astr_parcellation):
        """
        Process some quick stats on the z-score for the <astr_parcellation>:
        basically just tag/flag the min/max in the z-score vector for downstream
        processing.
        """
        b_status    = False

        if astr_parcellation in self.d_parcellation.keys():
            for str_hemi in ['lh', 'rh']:
                for str_stat in ['min', 'max']:
                    obj         = np.array(self.d_parcellation[astr_parcellation][str_hemi]['zScore'])
                    func        = getattr(obj, str_stat)
                    self.d_parcellation[astr_parcellation][str_hemi]['stats'][str_stat] = \
                        func()
                    b_status    = True

        return {
            'status':b_status
        }

    def zScore_filterPosNeg(self, astr_parcellation):
        """
        Filter the original z-score vector into a strictly positive
        and negative vectors and normalize (either to natural range or
        specified range).

        The filtered vectors are positive.
        """
        b_status = False

        if astr_parcellation in self.d_parcellation.keys():
            for str_hemi in ['lh', 'rh']:
                for str_sign in ['posNorm', 'negNorm']:
                    self.d_parcellation[astr_parcellation][str_hemi][str_sign] = \
                        self.d_parcellation[astr_parcellation][str_hemi]['zScore'].copy()
                    # Find the range
                    f_range = self.d_parcellation[astr_parcellation][str_hemi]['stats']['max'] \
                        if str_sign == 'posNorm' else \
                                -self.d_parcellation[astr_parcellation][str_hemi]['stats']['min']
                    # Optional scale
                    if self.options.f_scaleRange != 0.0:
                        f_range = self.options.f_scaleRange * f_range
                    if str_sign == 'posNorm':    
                        self.d_parcellation[astr_parcellation][str_hemi][str_sign] = \
                            [x/f_range if x > 0 else 0 for x in self.d_parcellation[astr_parcellation][str_hemi][str_sign]]
                    else:
                        self.d_parcellation[astr_parcellation][str_hemi][str_sign] = \
                            [-x/f_range if x < 0 else 0 for x in self.d_parcellation[astr_parcellation][str_hemi][str_sign]]
                    # Make sure that anything above 1.0 is set to 1.0
                    self.d_parcellation[astr_parcellation][str_hemi][str_sign] = \
                        [x if x <= 1.0 else 1.0 for x in self.d_parcellation[astr_parcellation][str_hemi][str_sign]]
                    b_status    = True
        return {
            'status':b_status
        }

    def zScore_bandwidthFilter(self, astr_parcellation):
        """
        Bandwidth filter the z-score vector.

        Modify the 'daM_color' attribute of the corresponding dictionary core.
        """
        b_status = False

        if astr_parcellation in self.d_parcellation.keys():
            N           = len(self.d_parcellation[astr_parcellation]['structureNames'])
            for str_hemi in ['lh', 'rh']:
                for str_sign in ['pos', 'neg']:
                    av_zscore               = np.array(self.d_parcellation[astr_parcellation][str_hemi]['%sNorm' % str_sign])
                    av_zscore.shape         = (N, 1)
                    if self.options.f_lowerFilter != -1.0:
                        f_filter            = np.amax(av_zscore) * self.options.f_lowerFilter
                        av_zscore           = np.where(av_zscore > f_filter, av_zscore, 0.0)
                    if self.options.f_upperFilter != -1.0:
                        f_filter            = np.amax(av_zscore) * self.options.f_upperFilter
                        av_zscore           = np.where(av_zscore < f_filter, av_zscore, 0.0)
                    b_status                = True
                    self.d_parcellation[astr_parcellation][str_hemi]['%sNorm' % str_sign] =  av_zscore

        return {
            'status':   b_status
        }

    def zScore_labelFileRGBcalc(self, astr_parcellation):
        """
        Calculate the RGB table for the lh/rh based on the normalized z-score pos and
        negative vectors.

        Modify the 'daM_color' attribute of the corresponding dictionary core.
        """
        b_status = False

        if astr_parcellation in self.d_parcellation.keys():
            N           = len(self.d_parcellation[astr_parcellation]['structureNames'])
            daM_color   = {}
            for str_hemi in ['lh', 'rh']:
                dav_color    = {}
                for str_sign in ['pos', 'neg']:
                    # av_zscore               = np.array(self.d_parcellation[astr_parcellation][str_hemi]['%sNorm' % str_sign])
                    # av_zscore.shape         = (N, 1)
                    av_zscore               = self.d_parcellation[astr_parcellation][str_hemi]['%sNorm' % str_sign]
                    dav_color[str_sign]     = np.array([0, 0, 0])
                    b_status                = True
                    # First create the color "vector"
                    if 'R' in getattr(self.options, '%sColor' % str_sign): dav_color[str_sign][0]   = 255
                    if 'G' in getattr(self.options, '%sColor' % str_sign): dav_color[str_sign][1]   = 255
                    if 'B' in getattr(self.options, '%sColor' % str_sign): dav_color[str_sign][2]   = 255
                    # Now replicate this into a numpy *array* that is matrix-like
                    daM_color[str_sign] = np.tile(dav_color[str_sign], (N, 1))
                    # and scale each row with the corresponding z-score
                    daM_color[str_sign] = daM_color[str_sign] * av_zscore
                daM_color[str_hemi] = daM_color['pos'] + daM_color['neg']
            self.d_parcellation[astr_parcellation]['daM_color'] = daM_color   

        return {
            'status':b_status
        }

    def zScore_labelFileRGBmake(self, astr_parcellation):
        """
        Make the RGB table
        """
        b_status = False

        if astr_parcellation in self.d_parcellation.keys():
            b_status        = True
            N               = len(self.d_parcellation[astr_parcellation]['structureNames'])
            daM_color       = self.d_parcellation[astr_parcellation]['daM_color']   
            aM_fullbrain    = np.concatenate((daM_color['lh'], daM_color['rh'])).astype(int)
            l_lhStruct      = ['lh-%s' % x for x in self.d_parcellation[astr_parcellation]['structureNames']]
            l_rhStruct      = ['rh-%s' % x for x in self.d_parcellation[astr_parcellation]['structureNames']]
            a_lhOffset      = np.zeros((N,1)) + 11100
            a_rhOffset      = np.zeros((N,1)) + 12100 
            l_allStructs    = l_lhStruct + l_rhStruct
            a_lhCount       = np.arange(1, N+1) + a_lhOffset.transpose()
            a_rhCount       = np.arange(1, N+1) + a_rhOffset.transpose()
            a_count         = np.concatenate((a_lhCount.transpose().astype(int), a_rhCount.transpose().astype(int)))
            a_alpha         = np.zeros((2*N,1)).astype(int)
            astr_allStructs = np.array((l_allStructs))
            astr_allStructs.shape = (len(astr_allStructs), 1)

            a_allData       = np.concatenate((a_count, astr_allStructs, aM_fullbrain, a_alpha), axis = 1)

            with open(  self.d_parcellation[astr_parcellation]['labelMapFile'],
                        mode = 'w') as csv_file:
                writer = csv.writer(csv_file, delimiter = '\t')
                writer.writerow(['0       Unknown                         0       0       0       0'])
                writer.writerows(a_allData)

        return {
            'status':b_status
        }


    def randomZscoreFile_generate(self, astr_parcellation):
        """
        Generate a "random" z-score file, based on the range given in the
        --random  --posRange and --negRange  command line flags. 
        
        This file has three columns,

            <structName> <leftHemisphere-z-score> <rightHemisphere-z-score>

        Save file to both input and output directories.

        """

        def file_write(f):
            writer  = csv.writer(f)
            for row in self.rows_zscore:
                writer.writerow(row) 

        l_parc  = self.d_parcellation[astr_parcellation]['structureNames']

        self.d_parcellation[astr_parcellation]['lh']['zScore'] =   np.random.uniform(  
                                            low     = self.options.f_negRange, 
                                            high    = self.options.f_posRange, 
                                            size    = (len(l_parc,))
                                ).tolist()
        self.d_parcellation[astr_parcellation]['rh']['zScore'] =   np.random.uniform(  
                                            low     = self.options.f_negRange, 
                                            high    = self.options.f_posRange, 
                                            size    = (len(l_parc,))
                                ).tolist()

        self.rows_zscore = zip( 
                        self.d_parcellation[astr_parcellation]['structureNames'], 
                        self.d_parcellation[astr_parcellation]['lh']['zScore'],
                        self.d_parcellation[astr_parcellation]['rh']['zScore']
                        )
        with open('%s/%s' % (self.options.inputdir, self.options.zFile), 
                    "w", newline = '') as f:
            file_write(f)
        shutil.copyfile(
            '%s/%s' % (self.options.inputdir,   self.options.zFile),
            '%s/%s' % (self.options.outputdir,  self.options.zFile)
        )

        return {
            'status':   True
        }

    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        """

        self.add_argument("-v", "--verbosity",
                            help        = "verbosity level for app",
                            type        = str,
                            dest        = 'verbosity',
                            optional    = True,
                            default     = "0")
        self.add_argument("-p", "--posRange",
                            help        = "positive range for random max deviation generation",
                            type        = float,
                            dest        = 'f_posRange',
                            optional    = True,
                            default     = 1.0)
        self.add_argument("-P", "--posColor",
                            help        = "Some combination of 'R', 'G', B' for positive heat",
                            type        = str,
                            dest        = 'posColor',
                            optional    = True,
                            default     = 'R')
        self.add_argument("-n", "--negRange",
                            help        = "negative range for random max deviation generation",
                            type        = float,
                            dest        = 'f_negRange',
                            optional    = True,
                            default     = -1.0)
        self.add_argument("-N", "--negColor",
                            help        = "Some combination of 'R', 'G', B' for negative heat",
                            type        = str,
                            dest        = 'negColor',
                            optional    = True,
                            default     = 'B')
        self.add_argument("-s", "--scaleRange",
                            help        = "scale range for normalization",
                            type        = float,
                            dest        = 'f_scaleRange',
                            optional    = True,
                            default     = 0.0)
        self.add_argument("-l", "--lowerFilter",
                            help        = "filter all z-scores below (normalized) <lowerFilter> to 0.0",
                            type        = float,
                            dest        = 'f_lowerFilter',
                            optional    = True,
                            default     = -1.0)
        self.add_argument("-u", "--upperFilter",
                            help        = "filter all z-scores above (normalized) <upperFilter> to 0.0",
                            type        = float,
                            dest        = 'f_upperFilter',
                            optional    = True,
                            default     = -1.0)
        self.add_argument("-z", "--zFile",
                            help        = "z-score file to read (relative to input directory)",
                            type        = str,
                            dest        = 'zFile',
                            optional    = True,
                            default     = 'zfile.csv')
        self.add_argument('--random',
                            help        = 'if specified, generate a z-score file',
                            type        = bool,
                            dest        = 'b_random',
                            action      = 'store_true',
                            optional    = True,
                            default     = False)
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

        self.options        = options
        self.d_hemiStats    = {
            'zScore':       [],
            'stats':        {'min': 0.0, 'max': 0.0},
            'posNorm':      [],
            'negNorm':      []
        }
        self.d_core         = {
            'structureNames':   [],
            'lh':               copy.deepcopy(self.d_hemiStats),
            'rh':               copy.deepcopy(self.d_hemiStats),
            'f_scaleRange':       self.options.f_scaleRange,
            'zScoreFile':       "",
            'labelMapFile':     "",
            'daM_color':        None
        }
        self.d_parcellation = {
            'a2009s':   copy.deepcopy(self.d_core),
            'DKatlas':  copy.deepcopy(self.d_core),
            'default':  copy.deepcopy(self.d_core)
        }

        if options.b_man:
            self.manPage_show()
            sys.exit(0)

        if options.b_meta:
            self.metaData_show()
            sys.exit(0)

        # pudb.set_trace()
        if options.b_version:
            print('Plugin Version: %s' % Z2labelmap.VERSION)
            sys.exit(0)

        copy_tree(self.options.inputdir, self.options.outputdir)

        self.d_parcellation['a2009s']['structureNames']     = \
                 self.a2009sStructList_define()
        self.d_parcellation['a2009s']['zScoreFile']         = '%s/%s' % \
                (self.options.inputdir, self.options.zFile)
        self.d_parcellation['a2009s']['labelMapFile']       = '%s/%s' % \
                (self.options.outputdir, 'aparc.annot.a2009s.ctab')

        b_zFileProcessed        = False

        if options.b_random:
            self.randomZscoreFile_generate('a2009s')
            b_zFileProcessed    = True
        else:
            if os.path.isfile('%s/%s' % 
                    (self.options.inputdir, self.options.zFile)):
                b_zFileProcessed = self.zScoreFile_read('a2009s')['status']
        
        if b_zFileProcessed:
            self.zScore_processStats('a2009s')
            self.zScore_filterPosNeg('a2009s')
            self.zScore_bandwidthFilter('a2009s')
            self.zScore_labelFileRGBcalc('a2009s')
            self.zScore_labelFileRGBmake('a2009s')


# ENTRYPOINT
if __name__ == "__main__":
    app = Z2labelmap()
    app.launch()
