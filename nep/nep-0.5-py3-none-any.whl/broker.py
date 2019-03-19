# coding = utf-8
#!/usr/bin/env python

# ------------------------------- Broker -----------------------_-----------
# Description: Low-level Broker class
# --------------------------------------------------------------------------
# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.
# Autor: Luis Enrique Coronado Zuniga


import time
import os
import zmq
import sys
import nep


class broker():
    def __init__(self, IP, PORT_XPUB, PORT_XSUB):
        """
        Creates a XPUB/XSUB broker for many2many publish-subcribe communication

        Parameters
        ----------

        IP : int 
            IP value of the broker

        PORT_XPUB : int 
            XPUB port. Which must be different that PORT_XSUB.

        PORT_XSUB : int 
            XSUB port. Which must be different that PORT_XPUB.

        """
        context = zmq.Context()
        frontend = context.socket(zmq.XSUB)
        frontend.bind("tcp://" + IP + ":" + str(PORT_XSUB))
        backend = context.socket(zmq.XPUB)
        backend.bind("tcp://" + IP + ":" + str(PORT_XPUB))
        zmq.proxy(frontend, backend)
        frontend.close()
        backend.close()
        context.term()

if __name__ == "__main__":
    import doctest
    doctest.testmod()