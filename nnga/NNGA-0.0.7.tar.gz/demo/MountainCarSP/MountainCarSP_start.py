import gym
from neuralNetworkGA import *

env = gym.make("MountainCarContinuous-v0")
generation = 0
ai = NeuroGA(2,[30],1,10)
while True:
    generation += 1
    print('-------------------------------')
    print('generation: '+ str(generation))
    gen = ai.next_gen_networks()
    for i in range(len(gen)):
        env.reset()
        observation,reward,done,info = env.step([0])
        while not done:
            res = gen[i].put_inputs(observation)
            #env.render()
            observation,reward,done,info = env.step(res)
            if reward > 99:
                savenet(gen[i],1)
        print(str(i) + ' score: ' + str(reward))
        ai.mark_score(reward,gen[i])