import numpy as np
from neuralNetworkGA import *
from multiprocessing import Process
import multiprocessing
import shelve

def run(i,q):
	geni = q.get()
	from ballG import ballgame
	game = ballgame()
	inputs,reward,terminal = game.start(0)
	while not terminal:
		res = geni.put_inputs(inputs)
		a = np.argmax(res)
		inputs,reward,terminal = game.start(a)
	q.put([i,reward])


if __name__=='__main__':
	ai = NeuroGA(3,[30],2,3)
	maxreward = 0
	generation = 0
	while True:
		generation += 1
		gen = ai.next_gen_networks()
		processes = list()
		x = []
		for i in range(len(gen)):
			x.append(multiprocessing.Queue())
			x[i].put(gen[i])
			p = Process(target=run,args=(i,x[i]))
			p.start()
			processes.append(p)
		for p in processes:
			p.join()
		for i in range(len(gen)):
			a = x[i].get()
			maxreward = np.where(maxreward>a[1],maxreward,a[1])
			print(a[1])
			ai.mark_score(a[1],gen[a[0]])
		print(str(generation)+ ' ' +str(maxreward))