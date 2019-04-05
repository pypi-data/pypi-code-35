# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['zeitig']

package_data = \
{'': ['*'], 'zeitig': ['templates/*']}

install_requires = \
['click',
 'colorama',
 'crayons',
 'dateparser',
 'jinja2',
 'pendulum',
 'qtoml>=0.2.4,<0.3.0']

entry_points = \
{'console_scripts': ['z = zeitig.scripts:run']}

setup_kwargs = {
    'name': 'zeitig',
    'version': '0.4.1',
    'description': 'time tracker and reporter',
    'long_description': 'zeitig\n======\n\n.. container:: bagdes\n\n    .. image:: https://travis-ci.org/diefans/zeitig.svg?branch=master\n           :target: https://travis-ci.org/diefans/zeitig\n\n    .. image:: https://img.shields.io/pypi/pyversions/zeitig.svg\n           :alt: PyPI - Python Version\n\n    .. image:: https://img.shields.io/pypi/v/zeitig.svg\n           :alt: PyPI\n\nA time tracker.\n\nThe basic idea is to store all situation changes as a stream of events and create a\nreport as an aggregation out of these.\n\n\nUsage\n-----\n\n.. code-block::\n\n    Usage: z [OPTIONS] [GROUP] COMMAND [ARGS]...\n\n    Options:\n      --help  Show this message and exit.\n\n    Commands:\n      add     Apply tags and notes.\n      break   Change to or start the `break` situation.\n      remove  Remove tags and flush notes.\n      report  Create a report of your events.\n      work    Change to or start the `work` situation.\n\n\nExample session\n---------------\n\nYou may add a timestamp, as in the example, which is parsed for your timezone.\nYou may abbreviate the commands, so the shortes way to track your time of a\nrunning project is just ``z w`` and ``z b``.\n\n.. code-block::\n\n    > export ZEITIG_STORE=/tmp/zeitig; mkdir $ZEITIG_STORE\n\n    > z foobar work -t foo "2018-04-01 08:00:00"\n\n    > z break "2018-04-01 12:00:00"\n\n    > z w "2018-04-01 13:00:00"\n\n    > z b "2018-04-01 17:30:00"\n\n    > z\n    Actual time: 2018-05-04 23:09:01\n\n    Actual group: foobar of foobar\n    Last situation in foobar: Break started at 2018-04-01 17:30:00 since 797.65 hours\n\n    Store used: /tmp/zeitig/olli\n    Last event: groups/foobar/source/2018-04-01T15:30:00+00:00\n\n    > z report\n    Working times for foobar until Friday 04 May 2018\n\n    Week: 13\n            2018-04-01 08:00:00 - 12:00:00 - 4.00 - foo\n            2018-04-01 13:00:00 - 17:30:00 - 4.50\n\n    Total hours: 8.50\n\n\nInternals\n---------\n\nYou may create a ``.zeitig`` directory somewhere in your current working\ndirectory path to use it as the store. Other defaults are ``~/.config/zeitig``\nand ``~/.local/share/zeitig``.\n\nFor every user is a separate directory created, which containes the groups and\nthe events sources:\n\n.. code-block::\n\n    .zeitig/\n        |\n        +- <user>\n            |\n            +- last ---+\n            |          |\n            +- groups  |\n            |   |      v\n            |   +- <group>\n            |       |     \n            |       +- source\n            |       |   |    \n            |       |   +- <event UTC timestamp>\n            |       |\n            |       +- templates\n            |       |   |\n            |       |   +- <jinja template>\n            |       |\n            |       +- template_defaults.toml\n            |       |\n            |       +- template_syntax.toml\n            |\n            +- templates\n            |   |\n            |   +- <jinja template>\n            |\n            +- template_defaults.toml\n            |\n            +- template_syntax.toml\n\nThe events are stored as simple ``toml`` files.\n\nReports\n_______\n\nEvents are fully exposed to the reporting template. You can pipeline certain\nfilters and aggregators to modifiy the event stream.\n\nTemplates are rendered by `jinja2`. You can modify the start and end tags by a\nspecial ``template_syntax.toml`` file.\n\nAn example latex template may look like this:\n\n.. code-block:: latex\n\n    \\documentclass{article}\n\n    \\usepackage[a4paper, total={6in, 8in}]{geometry}\n\n    \\usepackage{longtable,array,titling,booktabs}\n    \\setlength{\\parindent}{0pt}\n    \\setlength{\\parskip}{\\baselineskip}\n    \\title{\\vspace{-13em}Timesheet\\vspace{0em}}\n    \\author{\\vspace{-10em}}\n    \\date{\\vspace{-5em}}\n\n    % sans serif font\n    \\renewcommand{\\familydefault}{\\sfdefault}\n\n    \\begin{document}\n    \\maketitle\n    \\thispagestyle{empty} % no page footer\n    \\vspace{-5em}\n    \\begin{longtable}{\n        >{\\raggedleft\\arraybackslash}r\n        >{\\raggedright\\arraybackslash}l}\n        \\textbf{Client}: & We do something special\\\\\n        \\textbf{Contractor}: & Oliver Berger\\\\\n        \\textbf{Project number}: & 12-345-6789-0\\\\\n    \\end{longtable}\n\n    \\begin{longtable}{\n    >{\\raggedright\\arraybackslash}l\n    >{\\raggedright\\arraybackslash}l\n    >{\\raggedleft\\arraybackslash}r\n    >{\\raggedright\\arraybackslash}l}\n        Start & End & Hours & Description\\\\\n    \\BLOCK{for event in events.pipeline(\n        report.source,\n        events.filter_no_breaks,\n        events.Summary.aggregate,\n        events.DatetimeChange.aggregate\n        )-}\n        \\BLOCK{if py.isinstance(event, events.DatetimeChange) and event.is_new_week}\n        \\midrule\n    \\BLOCK{endif-}\n        \\BLOCK{if py.isinstance(event, events.Work)}\n        \\VAR{event.local_start.to_datetime_string()} & \\VAR{event.local_end.to_time_string()} & \\VAR{\'{0:.2f}\'.format(event.period.total_hours())} & \\BLOCK{if event.tags}\\VAR{\', \'.join(event.tags)}\\BLOCK{endif-}\\\\\n    \\BLOCK{endif-}\n\n        \\BLOCK{if py.isinstance(event, events.Summary)}\n        \\midrule\n        \\multicolumn{2}{l}{\\textbf{Total hours}} & \\textbf{\\VAR{\'{0:.2f}\'.format(event.works.total_hours())}} & \\\\\n    \\BLOCK{endif-}\n    \\BLOCK{-endfor-}\n    \\end{longtable}\n    \\vspace{5em}\n    \\begin{longtable}{\n    >{\\centering\\arraybackslash}p{3.5cm}\n    l\n    >{\\centering\\arraybackslash}p{5.5cm}}\n    \\cline{1-1}\n    \\cline{3-3}\n        Date & & Signature of client\\\\\n    \\end{longtable}\n\n    \\end{document}\n\n\nJinja syntax\n____________\n\nGroup jinja template syntax will be merged into user syntax:\n\n.. code-block::\n\n    [jinja_env]\n\n    [jinja_env.latex]\n    # define a latex jinja env\n    block_start_string = "\\\\BLOCK{"\n    block_end_string = "}"\n    variable_start_string = "\\\\VAR{"\n    variable_end_string = "}"\n    comment_start_string = "\\\\#{"\n    comment_end_string = "}"\n    line_statement_prefix = "%%"\n    line_comment_prefix = "%#"\n    trim_blocks = true\n    autoescape = false\n\n    [templates]\n    # map a template name to a jinja env\n    latex_template = "latex"\n\n\nJinja defaults\n______________\n\nYou may define also template defaults for a group, which will be merged into\nthe user template defaults.\n',
    'author': 'Oliver Berger',
    'author_email': 'diefans@gmail.com',
    'url': 'https://github.com/diefans/zeitig',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
