import numpy as np
from neuralNetworkGA import *
from multiprocessing import Process
import multiprocessing
import shelve
import time

geni = loadnet('gen_1')
from ballG import ballgame
game = ballgame()
while True:
    inputs,reward,terminal = game.start(0)
    while not terminal:
        time.sleep(0.005)
        res = geni.put_inputs(inputs)
        a = np.argmax(res)
        inputs,reward,terminal = game.start(a)