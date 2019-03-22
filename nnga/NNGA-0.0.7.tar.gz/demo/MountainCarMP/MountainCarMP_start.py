import numpy as np 
from neuralNetworkGA import *
from multiprocessing import Process
import multiprocessing
import shelve
import gym

def run(i,q):
    geni = q.get()
    env = gym.make("MountainCarContinuous-v0")
    env.reset()
    observation,reward,done,info = env.step([0])
    while not done:
        res = geni.put_inputs(observation)
        #a = np.argmax(res)
        observation,reward,done,info = env.step(res)
        env.render()
    q.put([i,reward])
    

if __name__=='__main__':
    ai = NeuroGA(2,[30],1,10)
    maxreward = 0
    generation = 0
    while True:
        generation += 1
        print('-------------------------------')
        print('generation: '+ str(generation))
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
            print(str(i) + ' score: ' + str(a[1]))
            ai.mark_score(a[1],gen[a[0]])