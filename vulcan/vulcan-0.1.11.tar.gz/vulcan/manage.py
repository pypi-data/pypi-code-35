#!/usr/bin/env python
from migrate.versioning.shell import main
import os

if __name__ == '__main__':

    db_path = 'sqlite:///'+os.path.expanduser('~/.vulcan/vulcan.db')

    main(url=db_path,
         debug='False',
         repository='vulcan_db'
         )
