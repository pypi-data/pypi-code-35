import gym
from neuralNetworkGA import *

env = gym.make("CartPole-v1")
generation = 0
ai = NeuroGA(4,[30],2,20)
while True:
    generation += 1
    print('-------------------------------')
    print('generation: '+ str(generation))
    gen = ai.next_gen_networks()
    for i in range(len(gen)):
        sum_reward = 0
        env.reset()
        observation,reward,done,info = env.step(0)
        sum_reward += reward
        while not done:
            res = gen[i].put_inputs(observation)
            a = np.argmax(res)
            env.render()
            observation,reward,done,info = env.step(a)
            sum_reward += reward
            if sum_reward > 499:
                savenet(gen[i],1)
        print(str(i) + ' score: ' + str(sum_reward))
        ai.mark_score(reward,gen[i])