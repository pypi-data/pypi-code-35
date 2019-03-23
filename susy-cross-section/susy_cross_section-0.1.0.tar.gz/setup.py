# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['susy_cross_section',
 'susy_cross_section.base',
 'susy_cross_section.interp',
 'susy_cross_section.tests']

package_data = \
{'': ['*'],
 'susy_cross_section': ['data/lhc_susy_xs_wg/*',
                        'data/nllfast/7TeV/*',
                        'data/nllfast/8TeV/*',
                        'data/nnllfast/13TeV/*'],
 'susy_cross_section.tests': ['data/*']}

install_requires = \
['click>=7.0,<8.0',
 'colorama>=0.4,<0.5',
 'coloredlogs>=10.0,<11.0',
 'pandas>=0.24,<0.25',
 'scipy>=1.2,<2.0']

extras_require = \
{':python_version >= "2.7.0" and python_version < "2.8.0"': ['pathlib>=1.0,<2.0',
                                                             'typing>=3.6,<4.0']}

entry_points = \
{'console_scripts': ['susy-xs = susy_cross_section.scripts:main']}

setup_kwargs = {
    'name': 'susy-cross-section',
    'version': '0.1.0',
    'description': 'A Python package for high-energy physics analysis to provide SUSY cross section data',
    'long_description': '[![Build Status](https://api.travis-ci.org/misho104/susy_cross_section.svg?branch=master)](https://travis-ci.org/misho104/susy_cross_section)\n[![Coverage Status](https://coveralls.io/repos/github/misho104/susy_cross_section/badge.svg?branch=master)](https://coveralls.io/github/misho104/susy_cross_section?branch=master)\n[![Doc Status](http://readthedocs.org/projects/susy-cross-section/badge/)](https://susy-cross-section.readthedocs.io/)\n[![PyPI version](https://badge.fury.io/py/susy-cross-section.svg)](https://badge.fury.io/py/susy-cross-section)\n[![License: MIT](https://img.shields.io/badge/License-MIT-ff25d1.svg)](https://github.com/misho104/susy_cross_section/blob/master/LICENSE)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n[susy_cross_section](https://github.com/misho104/susy_cross_section): Table-format cross-section data handler\n=============================================================================================================\n\nA Python package for [cross section tables](https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SUSYCrossSections) and interpolation.\n\nQuick Start\n-----------\n\nThis package supports Python 2.7 and 3.5+.\n\nInstall simply via PyPI and use a script as:\n\n```console\n$ pip install susy-cross-section\n$ susy-xs get 13TeV.n2x1+.wino 500\n(32.9 +2.7 -2.7) fb\n$ susy-xs get 13TeV.n2x1+.wino 513.3\n(29.4 +2.5 -2.5) fb\n```\n\nwhich gives the 13 TeV LHC cross section to wino-like neutralino-chargino pair-production (`p p > n2 x1+`), etc.\nThe values are taken from [LHC SUSY Cross Section Working Group](https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SUSYCrossSections13TeVn2x1wino#Envelope_of_CTEQ6_6_and_MSTW_AN1) with interpolation if needed.\n\nTo see more information, you will use `show` sub-command, which displays the cross-section table with physical attributes.\n\n```console\n$ susy-xs show 13TeV.n2x1+.wino\n\n------------------------------------------------------------------------\nTABLE "xsec" (unit: fb)\n------------------------------------------------------------------------\n               value        unc+        unc-\nm_wino\n100     13895.100000  485.572000  485.572000\n125      6252.210000  222.508000  222.508000\n150      3273.840000  127.175000  127.175000\n...              ...         ...         ...\n475        41.023300    3.288370    3.288370\n500        32.913500    2.734430    2.734430\n525        26.602800    2.299570    2.299570\n...              ...         ...         ...\n1950        0.005096    0.001769    0.001769\n1975        0.004448    0.001679    0.001679\n2000        0.003892    0.001551    0.001551\n\n[77 rows x 3 columns]\n\ncollider: pp-collider, ECM=13TeV\ncalculation order: NLO+NLL\nPDF: Envelope by LHC SUSY Cross Section Working Group\nincluded processes:\n  p p > wino0 wino+\n```\n\nYou may also notice that the above value for 513.3GeV is obtained by interpolating the grid data.\n\nYou can list all the available tables, or search for tables you want, by `list` sub-command:\n\n```console\n$ susy-xs list\n13TeV.n2x1-.wino       lhc_susy_xs_wg/13TeVn2x1wino_envelope_m.csv\n13TeV.n2x1+.wino       lhc_susy_xs_wg/13TeVn2x1wino_envelope_p.csv\n13TeV.n2x1+-.wino      lhc_susy_xs_wg/13TeVn2x1wino_envelope_pm.csv\n13TeV.slepslep.ll      lhc_susy_xs_wg/13TeVslepslep_ll.csv\n13TeV.slepslep.maxmix  lhc_susy_xs_wg/13TeVslepslep_maxmix.csv\n13TeV.slepslep.rr      lhc_susy_xs_wg/13TeVslepslep_rr.csv\n...\n\n$ susy-xs list 7TeV\n7TeV.gg.decoup  nllfast/7TeV/gdcpl_nllnlo_mstw2008.grid\n7TeV.gg.high    nllfast/7TeV/gg_nllnlo_hm_mstw2008.grid\n7TeV.gg         nllfast/7TeV/gg_nllnlo_mstw2008.grid\n...\n7TeV.ss10       nllfast/7TeV/ss_nllnlo_mstw2008.grid\n7TeV.st         nllfast/7TeV/st_nllnlo_mstw2008.grid\n\n$ susy-xs list 8t decoup\n8TeV.gg.decoup    nllfast/8TeV/gdcpl_nllnlo_mstw2008.grid\n8TeV.sb10.decoup  nllfast/8TeV/sdcpl_nllnlo_mstw2008.grid\n```\n\nand run for it:\n\n```console\n$ susy-xs get 8TeV.sb10.decoup 1120\n(0.00122 +0.00019 -0.00019) pb\n```\n\nFor more help, try to run with `--help` option.\n\n```console\n$ susy-xs --help\nUsage: susy-xs [OPTIONS] COMMAND [ARGS]...\n...\n\n$ susy-xs get --help\nUsage: susy-xs get [OPTIONS] TABLE [ARGS]...\n...\n```\n\nYou can uninstall this package as simple as\n\n```console\n$ pip uninstall susy-cross-section\nUninstalling susy-cross-section-x.y.z:\n   ...\nProceed (y/n)?\n```\n\nIntroduction\n------------\n\nProduction cross sections are the most important values for high-energy physics collider experiments.\nMany collaborations publish their cross-section tables, calculated in various tools or schemes, which are available on the WWW.\nFor SUSY scenarios, the values provided by [LHC SUSY Cross Section Working Group](https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SUSYCrossSections) are the most famous source of the "nominal" cross section expectation for the LHC, while [NNLL-fast](https://www.uni-muenster.de/Physik.TP/~akule_01/nnllfast/) collaboration publishes those for colored process at the very high precision.\n\nHowever, these results are provided in various format; for example, some are in HTML with absolute combined symmetric uncertainties, and others are in CSV files with relative asymmetric uncertainties.\n\nThis package `susy_cross_section` is provided to handle those data regardless of their format.\nThis package reads any table-like grid files with help of [pandas](https://pandas.pydata.org/) DataFrame, and interpret any format of uncertainties once an annotation file  (`info` files) written in JSON format is provided, which allows one to interpolate the grid easily, e.g., by using [scipy.interpolate](https://docs.scipy.org/doc/scipy/reference/interpolate.html) package.\n\nFor simpler use-case, a command-line script `susy-xs` is provided, with which one can get the cross section in several simple scenarios.\nFor more customization, you can use this package from your own code with more detailed interpolator options (linear-interpolation, loglog-spline-interpolation, etc.) or with your interpolator.\n\nDocument\n--------\n\nThe document is provided on [readthedocs.io](https://susy-cross-section.readthedocs.io), together with [API references](https://susy-cross-section.readthedocs.io/en/latest/api_reference.html).\nA [PDF file](https://github.com/misho104/susy_cross_section/blob/master/docs/doc.pdf) is also distributed with this package.\n\nLicense and Citation Policy\n---------------------------\n\nThe program codes included in this repository are licensed by [Sho Iwamoto / Misho](https://www.misho-web.com) under [MIT License](https://github.com/misho104/SUSY_cross_section/blob/master/LICENSE).\n\nThe non-program-code documents are licensed by [Sho Iwamoto / Misho](https://www.misho-web.com) under [CC BY-NC 4.0 International](https://creativecommons.org/licenses/by-nc/4.0/) License.\n\nOriginal cross-section data is distributed by other authors, including\n\n* [LHC SUSY Cross Section Working Group](https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SUSYCrossSections).\n* [NNLL-fast](https://www.uni-muenster.de/Physik.TP/~akule_01/nnllfast/)\n\nFull list of references are shown in [citations.pdf](https://github.com/misho104/susy_cross_section/blob/master/contrib/citations.pdf) distributed with this package, where you will find the citation policy for this package.\n',
    'author': 'Sho Iwamoto (Misho)',
    'author_email': 'webmaster@misho-web.com',
    'url': 'https://github.com/misho104/susy_cross_section',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
