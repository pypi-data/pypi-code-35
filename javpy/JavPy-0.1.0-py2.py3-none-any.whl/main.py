# encoding: utf-8

import urllib3
from JavPy.app.tgbot.server import run
from JavPy.utils.node import Node
from JavPy.app.webserver import app
import os


# start node.js subprocess
Node.start_node()

# # run telegram bot service
# run()

# run web server
app.app.run('0.0.0.0', 8081)
