import gym
from neuralNetworkGA import *

env = gym.make("CartPole-v0")
done = False
geni = loadnet('gen_1')
while True:
    env.reset()
    observation,reward,done,info = env.step(0)
    while not done:
        res = geni.put_inputs(observation)
        observation,reward,done,info = env.step(np.argmax(res))
        env.render()