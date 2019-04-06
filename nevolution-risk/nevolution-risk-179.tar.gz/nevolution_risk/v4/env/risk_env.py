"""
Author: Heinrich Sporys
"""

import time

import gym
import networkx as nx
import numpy as np
import pygame
from gym import spaces
from numpy import int32, float32

from nevolution_risk.v4.logic import Graph
from nevolution_risk.v4.view import Gui


class RiskEnv(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second': 10
    }

    node_count = 42
    player_count = 4
    troop_count = 5
    default_encode = [1, 2, 3, 5, 10]

    def __init__(self, encode=None):
        self.agent_troops_count = 0
        self.player_positions = None
        self.card_seed = 42
        self.graph = Graph(self.card_seed, self.player_positions, self.player_count)
        self.static_agents = []
        self.static_agents.append(self.random_step)
        self.static_agents.append(self.random_step)
        self.static_agents.append(self.random_step)
        self.gui = Gui(self.graph)
        self.done = False
        self.rendering = True
        self.first_render = True
        self.game_state = 0
        if encode is None:
            self.encode = self.default_encode
        else:
            self.encode = encode
        self.encode_index_array = self.generate_encode_index_array()
        self.valid_actions = []
        for n in range(0, len(self.graph.nodes)):
            for adjacent in self.graph.nodes[n].adj_list:
                self.valid_actions.append((self.graph.nodes[n].id, adjacent.id, True))
                self.valid_actions.append((self.graph.nodes[n].id, adjacent.id, False))
        self.valid_actions.append((-1, 0, 0))
        self.legal_actions = []

        edges = []
        for line in nx.generate_edgelist(self.graph.graph):
            edges.append(line)
        edge_count = len(edges)
        self.observation_space = spaces.Box(low=0, high=1,
                                            shape=[self.node_count * (self.player_count + len(self.encode)) + 1, ],
                                            dtype=int32)
        self.observation_len = len(self.observation_space.sample())
        self.action_space = spaces.Box(low=0, high=1, shape=[edge_count * 4 + 1, ], dtype=float32)
        self.action_space_len = len(self.action_space.sample())

        self.dis = np.zeros(4)
        self.atk = np.zeros(4)
        self.shift = np.zeros(4)

    def set_static_agent(self, step_function, id=0):
        """
        sets the behaviour of one of the AI opponents.

        :param  step_function: a function that returns an action, which is shaped according to the action space
                the function takes the observation of the environment as input
        :param id: place in the static self.static_agents array
        :raises EnvironmentError: if the given function returns an action of the wrong length
        :return: nothing
        """
        step_fun_len = len(step_function(self.encode_graph()))
        acs_len = len(self.action_space.sample())
        if acs_len != step_fun_len:
            raise EnvironmentError(
                "tried to set static agent with wrong action length (expected {} got {})".format(acs_len, step_fun_len))
        self.static_agents[id] = step_function

    def set_start_positions(self, positions):
        """
        sets the starting position of the 4 player on the map
        also replaces the current graph with a new one

        :param positions:   array with tuples containing (troop_count, player_id)
                            each tuple corresponds to a node in the graph (length should be 42)
        :return:
        """
        if len(positions) != 42:
            raise EnvironmentError('Positions array doesnt have length 42')
        if not isinstance(positions, list):
            raise EnvironmentError("Positions are not a list")
        for element in positions:
            if element is None:
                raise Exception("Position contains None elements")
            elif not isinstance(element[0], int):
                raise Exception("Positions array contains non int tuples")
            elif not isinstance(element[1], int):
                raise Exception("Positions array contains non int tuples")

            self.player_positions = positions
            self.graph = Graph(42, self.player_positions, self.player_count)

    def seed(self, seed=42):
        """
        sets the seed that is used to generate cards and the seed that is used to calculate random step for the agents

        :param seed: will be used as a seed in the random card and step generation
        :return: nothing
        """
        self.card_seed = seed
        self.action_space.seed(seed)

    def close(self):
        del self

    '''
        action format:
            [probabilities]
    '''

    def find_best_action(self, action):
        """
        finds the best valid and legal action from a given action (in the action space)
        :param action: an array of scores for all actions
        :return: action, best valid action
        """
        index = np.argmax(action)
        action[index] = -2
        action_command = self.valid_actions[index]

        while not self.is_action_valid(action_command):
            index = np.argmax(action)
            action[index] = -2
            action_command = self.valid_actions[index]
        return action_command

    def step_ai(self):
        """
        executes an enemy ai's step
        :return: boolean, True if the game ended, False otherwise
        """
        # code for opponent AI starts  here
        observation = self.encode_graph()

        static_agent_action = self.static_agents[self.graph.current_player.id - 1](observation)

        action_command = self.find_best_action(static_agent_action)

        if self.execute_action(action_command):
            self.game_state = self.game_state + 1

        self.done = self.graph.is_conquered()
        if self.done:
            return True
        # code for opponent AI ends here
        if self.game_state == 0:
            self.dis[self.graph.current_player.id] += 1
        elif self.game_state == 1:
            self.atk[self.graph.current_player.id] += 1
        elif self.game_state == 2:
            self.shift[self.graph.current_player.id] += 1

        if self.game_state > 2:
            self.game_state = 0
            self.graph.next_player()
        return False

    def step(self, action):
        """
            simulates one step of the game that is being played
            the enemy turn is part of one step

            :param action:  a list of values between 0 and 1
                            the values represent probabilities, that are mapped to valid actions
                            the mapping can be taken from self.valid_actions
                            format of an action: (node1, node2, boolean)
                            example: (0, 1, True)
                            the first node is the start, the 2nd node is the end
                            the boolean signifies if after an attack maximum or minimum troops get moved to the
                            conquered node
            :return: 4 results of the current step
                observation - game state after the step, shape defined in observation_space
                reward      - reward for the step
                done        - a boolean, which is true, when the match is over
                info        - a string which can display some information
        """
        action_len = len(action)
        if action_len != self.action_space_len:
            raise EnvironmentError("tried to execute action of wrong length (expected {} got {})"
                                   .format(self.action_space_len, action_len))

        if self.done:
            self.reset()

        if self.game_state == 0:
            self.dis[self.graph.current_player.id] += 1
        elif self.game_state == 1:
            self.atk[self.graph.current_player.id] += 1
        elif self.game_state == 2:
            self.shift[self.graph.current_player.id] += 1

        action_command = self.find_best_action(action)

        if self.execute_action(action_command):
            self.game_state = self.game_state + 1

        self.done = self.graph.is_conquered()

        if self.game_state > 2:
            self.game_state = 0
            self.graph.next_player()

            while self.graph.current_player.id != 0:
                if self.step_ai():
                    break

        observation = self.encode_graph()
        self.done = self.graph.is_conquered()

        reward = self.graph.players[0].reward
        for player in self.graph.players:
            player.reward = 0

        return observation, reward, self.done, ()

    def execute_action(self, action):
        """
        executes the right action depending on the current player and current game state
        in stage 0: a troop gets added to node2
        in stage 1: node1 attacks node2 and conquers is according to the boolean
        in stage 2: 3 troops from node1 are moved to node2
                    if less than 3 troops can be moved, that amount will be taken instead
                    to avoid infinite circles, the start mode in set to true

        :param action:  tuple of (int, int, boolean)
                        the values represent (node1, node2, maximum or minimum of troops moved after conquering a node)
                        the values are interpreted differently, depending on game state
        :return: True when the action ends the current game state and progresses to the next state
        """
        if self.graph.current_player.troops > 0 and self.game_state == 0:
            self.graph.distribute(action[1])
            if self.graph.current_player.troops > 0:
                return False
            else:
                return True

        if action[0] == -1:
            return True

        if self.game_state == 1:
            if self.graph.attack(action[0], action[1], action[2]):
                if not self.graph.current_player.card_received:
                    self.graph.current_player.add_card()
                    self.graph.current_player.card_received = True
            return False

        if self.game_state == 2:
            self.graph.fortify(action[0], action[1])
            return False

        return True

    def random_step(self, observation):
        """
        this functions is used as default step function for the static agents

        :param observation: not used yet
        :return: action that is in accordance with the action space
        """
        return self.action_space.sample()

    def reset(self):
        """
        replaces the current game state with a fresh one

        :return: observation of the new game state
        """
        self.graph = Graph(self.card_seed, self.player_positions, self.player_count)
        self.gui.graph = self.graph
        self.done = False
        self.game_state = 0
        self.dis = np.zeros(4)
        self.atk = np.zeros(4)
        self.shift = np.zeros(4)
        self.rendering = True
        self.agent_troops_count = 0
        return self.encode_graph()

    def render(self, mode='human', control="auto"):
        """
        draws the current games state into the pygame window and sleeps for 1/60 seconds

        :param mode:    defines the format of the visual output
                        currently supported:
                        human: renders the gui in a window, visible to the user
                        rgb-array: outputs tpo a video format
        :param control: decides whether additional gui elements are displayed for human/machine control
                        currently supported:
                        auto:   some gui elements are not displayed and
                                the environment only checks if the window is closed
                        manual: assumes that gui elements are drawn and input is pulled from outside the environment
                                needed to make the game humanly playable

        :return: nothing
        """
        if self.first_render:
            pygame.init()
            self.first_render = False

        if control == "auto":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
        if mode == 'rgb_array':
            return self.gui.render(mode)
        else:
            self.gui.render(mode)

        if control == "auto":
            pygame.display.update()

    def is_action_valid(self, action):
        """
        checks if a certain action is valid, depending on the current game state and player

        :param action:  a tuple containing start node, end node on the graph, a boolean that indicates the amount of
                        roops moved if a node is conquered (True -> move all troops, False -> move minimum troops)
        :return: True if the action is valid
        """

        start = self.graph.nodes[action[0]]
        end = self.graph.nodes[action[1]]

        if self.game_state == 0:
            if action[0] == -1:
                return False
            elif end.player == self.graph.current_player:
                return True
            else:
                return False

        if action[0] == -1:
            return True

        if self.game_state == 1:
            if start.troops < 2:
                return False
            elif start.player != self.graph.current_player:
                return False
            elif end.player == self.graph.current_player:
                return False
            else:
                return True

        if self.game_state == 2:
            if start.troops < 2:
                return False
            elif end.marked:
                return False
            elif start.player != self.graph.current_player:
                return False
            elif end.player != self.graph.current_player:
                return False
            else:
                return True

        return True

    def update_legal_actions(self):
        """
        checks each action in valid actions for validity and puts the result into self.legal_actions
        the result takes into account the current player and game state

        legal_actions is a list that contains 0 and 1
        it will be multiplied to the action array, given to the step function to filer out illegal actions

        an action is valid, when the graph connects start and end node
        an action is legal, when none of the game rules are broken

        :return: nothing
        """

        self.legal_actions = np.zeros(self.action_len, float32)

        for i, action in enumerate(self.valid_actions):
            if self.is_action_valid(action):
                self.legal_actions[i] = 1

    def encode_graph(self):
        """
        encodes the current game state with the encode defined in the constructor and a one-hot encode

        resulting observation structure:
        for all nodes:
            amount of troops encoded with encode_number function
            player index encoded with to_one_hot function
        the last element in the observation is set to either 0 or 1 depending on if the player that corresponds to the
        observation still has troops to distribute or not

        :return:    an array that contains 0s and 1s to represent the current
                    game state from the view of the current player
        """
        observation = np.zeros(self.observation_len, np.int32)

        graph = self.get_game_state()
        offset = self.player_count - self.graph.current_player.id

        index = 0
        troop_len = len(self.encode)
        for node in graph:
            # troop count
            # i would put this in an extra function but this loses ~5% performance
            if node[0] >= self.encode[-1]:
                observation[index + self.encode_index_array[-1]] = 1
            elif node[0] >= self.encode[0]:
                observation[index + self.encode_index_array[node[0] - 1]] = 1
            # do nothing otherwise
            index += troop_len

            # player
            player_id = (node[1] + offset) % self.player_count
            observation[index + player_id] = 1
            index += self.player_count

        if self.graph.current_player.troops > 0:
            observation[-1] = 1
        return observation

    def get_game_state(self):
        """
        pulls the current game state from self.graph

        :return: array containing information about the troops and player on each node in form of a tuple
        """
        game_state = [None] * len(self.graph.nodes)
        i = 0
        for node in self.graph.nodes:
            game_state[i] = (node.troops, node.player.id)
            i += 1

        return game_state

    def generate_encode_index_array(self):
        """
        generates an array of the to encode values for the troop_numbers in the range of 0..(last encode value), to
        allow better performance, the result is stored in the self.encode_index_array indexed by the troop_number
        :return: None
        """
        self.encode_index_array = []

        for i in range(1, self.encode[-1] + 1):
            encode_i = -1
            for index in range(len(self.encode) - 1):
                if self.encode[index] <= i < self.encode[index + 1]:
                    encode_i = index
            if i >= self.encode[-1]:
                encode_i = len(self.encode) - 1
            self.encode_index_array.append(encode_i)

        return self.encode_index_array


def to_one_hot_raw(n, limit):
    """
    encodes a number to one-hot

    examples with limit 5
    0   -> [1,0,0,0,0,0]
    1   -> [0,1,0,0,0,0]
    3   -> [0,0,0,3,0,0]
    5   -> [0,0,0,0,0,1]

    :param n: integer, gets encoded
    :param limit: integer, defines the length
    :return: array containing 0s and a 1 at the index of n
    """
    if n < 0:
        raise IndexError("number must not be negative")

    array = np.zeros(limit + 1, np.int32)
    array[n] = 1
    return array


if __name__ == '__main__':
    print()
    env = RiskEnv()

    env.seed(1)
    env.reset()
    done = False

    n = 0
    # env.render()

    distribute = np.array([0, 0, 0, 0])
    attack = np.array([0, 0, 0, 0])
    shift = np.array([0, 0, 0, 0])

    t1 = time.time()
    for i in range(1):
        observation = env.reset()
        done = False
        while not done:
            observation, reward, done, info = env.step(env.action_space.sample())
            n += 1
            # env.render()

        distribute = np.add(distribute, env.dis)
        attack = np.add(attack, env.atk)
        shift = np.add(shift, env.shift)

        # print("reward: ", reward)
        # env.render()
        # print("winner is ", env.graph.nodes[0].player.name)
    print("step ", n)
    print('Time needed:', time.time() - t1)
    print('Average steps:', n / 10)
    print('Distribute:', np.array(env.dis) / 10)
    print('Attack', np.array(env.atk) / 10)
    print('Shift:', np.array(env.shift) / 10)
