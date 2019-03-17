"""
Taken from openai/baseline with minor edits
See https://github.com/openai/baselines/blob/master/baselines/common/vec_env/subproc_vec_env.py
"""

from abc import ABC, abstractmethod
from multiprocessing import Process, Pipe

import gym
import numpy as np


class CloudpickleWrapper:
    """ Uses cloudpickle to serialize contents (otherwise multiprocessing
    tries to use pickle).
    """

    def __init__(self, env_fn):
        self.env_fn = env_fn

    def __getstate__(self):
        import cloudpickle
        return cloudpickle.dumps(self.env_fn)

    def __setstate__(self, ob):
        import pickle
        self.env_fn = pickle.loads(ob)


class VectorizedEnv(ABC):
    """ An abstract asynchronous, vectorized environment. """

    def __init__(self, num_envs, observation_space, action_space):
        self.num_envs = num_envs
        self.observation_space = observation_space
        self.action_space = action_space

    @abstractmethod
    def reset(self):
        """ Reset all the environments and return an array of observations, or 
        a dict of observation arrays. If step_async is still doing work, that 
        work will be cancelled and step_wait() should not be called until 
        step_async() is invoked again.
        """
        pass

    @abstractmethod
    def step_async(self, actions):
        """ Tell all the environments to start taking a step with the given 
        actions. Call step_wait() to get the results of the step. You should 
        not call this if a step_async run is already pending.
        """
        pass

    @abstractmethod
    def step_wait(self):
        """ Wait for the step taken with step_async().
        Returns (obs, rews, dones, infos):
         - obs: an array of observations, or a dict of
                arrays of observations.
         - rews: an array of rewards
         - dones: an array of "episode done" booleans
         - infos: a sequence of info objects
        """
        pass

    @abstractmethod
    def close(self):
        """ Clean up the environments' resources. """
        pass

    def step(self, actions):
        """ Step the environments synchronously.
        This is available for backwards compatibility.
        """
        self.step_async(actions)
        return self.step_wait()

    def render(self, mode='human'):
        #logger.warn('Render not defined for %s' % self)
        pass

    @property
    def unwrapped(self):
        if isinstance(self, VecEnvWrapper):
            return self.venv.unwrapped
        else:
            return self


class ParallelEnv(VectorizedEnv):
    def __init__(self, env_name, n=4, seed=None, spaces=None):
        """ Initializes a ParallelEnv.
        envs: list of gym environments to run in subprocesses
        adopted from openai baseline
        """
        raise NotImplementedError()

        env_fns = [ gym.make(env_name) for _ in range(n) ]

        if seed is not None:
            for i, e in enumerate(env_fns):
                e.seed(i + seed)

        self.waiting = False
        self.closed = False

        nenvs = len(env_fns)

        # Connection objects representing the end of a bidirectional pipe
        self.remotes, self.work_remotes = zip(*[Pipe() for _ in range(nenvs)])

        self.ps = [Process(target=self.worker, args=(work_remote, remote, CloudpickleWrapper(env_fn)))
            for (work_remote, remote, env_fn) in zip(self.work_remotes, self.remotes, env_fns)]

        for p in self.ps:
            # If the main process crashes, we should not cause things to hang
            p.daemon = True
            p.start()

        for remote in self.work_remotes:
            remote.close()

        self.remotes[0].send(('get_spaces', None))
        observation_space, action_space = self.remotes[0].recv()
        VectorizedEnv.__init__(self, len(env_fns), observation_space, action_space)

    def step_async(self, actions):
        for remote, action in zip(self.remotes, actions):
            remote.send(('step', action))
        self.waiting = True

    def step_wait(self):
        results = [remote.recv() for remote in self.remotes]
        self.waiting = False
        obs, rews, dones, infos = zip(*results)
        return np.stack(obs), np.stack(rews), np.stack(dones), infos

    def reset(self):
        for remote in self.remotes:
            remote.send(('reset', None))
        return np.stack([remote.recv() for remote in self.remotes])

    def reset_task(self):
        for remote in self.remotes:
            remote.send(('reset_task', None))
        return np.stack([remote.recv() for remote in self.remotes])

    def close(self):
        if self.closed:
            return
        if self.waiting:
            for remote in self.remotes:
                remote.recv()
        for remote in self.remotes:
            remote.send(('close', None))
        for p in self.ps:
            p.join()
        self.closed = True

    @staticmethod
    def worker(remote, parent_remote, env_fn_wrapper):
        """ A worker process. """
        parent_remote.close()
        env = env_fn_wrapper.env_fn

        while True:
            command, data = remote.recv()
            if command == 'step':
                ob, reward, done, info = env.step(data)
                if done:
                    ob = env.reset()
                remote.send((ob, reward, done, info))
            elif command == 'reset':
                ob = env.reset()
                remote.send(ob)
            elif command == 'reset_task':
                ob = env.reset_task()
                remote.send(ob)
            elif command == 'close':
                remote.close()
                break
            elif command == 'get_spaces':
                remote.send((env.observation_space, env.action_space))
            else:
                raise NotImplementedError
