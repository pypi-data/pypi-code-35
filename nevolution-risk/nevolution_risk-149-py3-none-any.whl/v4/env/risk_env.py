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
        self.seed = 42
        self.graph = Graph(self.seed, self.player_positions, self.player_count)
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
        self.action_space = spaces.Box(low=0, high=1, shape=[edge_count * 4 + 1, ], dtype=float32)
        self.action_len = len(self.action_space.sample())

        self.dis = np.zeros(4)
        self.atk = np.zeros(4)
        self.shift = np.zeros(4)

    def set_static_agent(self, step_function, id=0):
        self.static_agents[id] = step_function

    def set_start_positions(self, positions):
        """
        sets the starting position of the 4 player on the map
        also replaces the current graph with a new one

        :param positions:   array with tuples containing (troop_count, player_id)
                            each tuple corresponds to a node in the graph (length should be 42)
        :return:
        """
        if len(positions < 42):
            raise EnvironmentError('Positions array doesnt have length 42')
        self.player_positions = positions
        self.graph = Graph(self.player_positions, self.player_count)

    '''
    action format:
        [probabilities]
    '''

    def seed(self, seed=42):
        self.seed = seed

    def close(self):
        del self

    def step(self, action):
        """
            simulates one step of the game that is being played
            the enemy turn is part of one step

            :param action: a list of values, shape is defined in he action_space
            :return: 4 results of the current step
                observation - game state after the step, shape defined in observation_space
                reward      - reward for the step
                done        - a boolean, which is true, when the match is over
                info        - a string which can display some information
        """
        if self.done:
            self.reset()

        self.update_legal_actions()
        for i in range(0, len(action)):
            action[i] *= self.legal_actions[i]

        source_id = self.valid_actions[np.argmax(action)][0]
        target_id = self.valid_actions[np.argmax(action)][1]
        troops = self.valid_actions[np.argmax(action)][2]

        if self.game_state == 0:
            self.dis[self.graph.current_player.id] += 1
        elif self.game_state == 1:
            self.atk[self.graph.current_player.id] += 1
        elif self.game_state == 2:
            self.shift[self.graph.current_player.id] += 1

        if self.execute_action((source_id, target_id, troops)):
            self.game_state = self.game_state + 1

        if self.game_state > 2:
            self.game_state = 0
            self.graph.next_player()

            while self.graph.current_player.id != 0:
                """
                ----------------------------------------------------------------------------------
                code for opponent AI goes here
                """
                observation = self.encode_graph()

                static_agent_action = self.static_agents[self.graph.current_player.id - 1](observation)

                self.update_legal_actions()
                for i in range(0, len(static_agent_action)):
                    static_agent_action[i] *= self.legal_actions[i]

                source_id = self.valid_actions[np.argmax(static_agent_action)][0]
                target_id = self.valid_actions[np.argmax(static_agent_action)][1]
                troops = self.valid_actions[np.argmax(static_agent_action)][2]

                if self.execute_action((source_id, target_id, troops)):
                    self.game_state = self.game_state + 1
                """
                ----------------------------------------------------------------------------------
                """

                if self.game_state == 0:
                    self.dis[self.graph.current_player.id] += 1
                elif self.game_state == 1:
                    self.atk[self.graph.current_player.id] += 1
                elif self.game_state == 2:
                    self.shift[self.graph.current_player.id] += 1

                if self.game_state > 2:
                    self.game_state = 0
                    self.graph.next_player()

        observation = self.encode_graph()
        self.done = self.graph.is_conquered()

        reward = self.graph.players[0].reward
        for player in self.graph.players:
            player.reward = 0

        return observation, reward, self.done, ()

    def execute_action(self, action):
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
        return self.action_space.sample()

    def reset(self):
        """
        replaces the current game state with a fresh one

        :return: observation of the new game state
        """
        self.graph = Graph(42, self.player_positions, self.player_count)
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

        :param mode:
        :param control: decides whether additional gui elements are displayed for human/machine control
        :return:
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
        checks if the current player owns the starting node

        :param action: a tuple containing start and end node on the graph
        :return: true if the player owns the starting node
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
        iterates over the valid_actions array if all players and updates its values

        an action is valid, when the graph connects start and end node
        an action is legal, when none of the game rules are broken

        :return:
        """

        self.legal_actions = np.zeros(self.action_len, float32)

        for i, action in enumerate(self.valid_actions):
            if self.is_action_valid(action):
                self.legal_actions[i] = 1

    def encode_graph(self):
        """
        encodes the current game state via one hot encoding
        an integer encoded to one hot results in a array that is filled with zeros and only contains a 1 at the index
        of the integer

        example:
        space = 0-4
        integer = 3

        encode: [0,0,0,1,0]

        :param reverse: boolean, that if true, flips the players before encoding
        :return: an array that contains 0s and 1s to represent the current game state
        """
        observation = np.zeros(0, int32)
        zero_array = np.zeros(1, int32)

        graph = self.get_game_state()
        offset = self.player_count - self.graph.current_player.id

        for node in graph:
            troops = self.encode_number(node[0])
            player_id = (node[1] + offset) % self.player_count
            player = to_one_hot(player_id, self.player_count - 1)

            observation = np.append(observation, troops)
            observation = np.append(observation, player)

        if self.graph.current_player.troops > 0:
            zero_array[0] = 1

        observation = np.append(observation, zero_array)

        return observation

    def get_game_state(self):
        game_state = []

        for node in self.graph.nodes:
            state = (node.troops, node.player.id)
            game_state.append(state)

        return game_state

    def encode_number(self, number):
        array = np.zeros(len(self.encode), int32)

        for i in range(0, len(self.encode) - 1):
            if self.encode[i] <= number < self.encode[i + 1]:
                array[i] = 1
        if number >= self.encode[-1]:
            array[-1] = 1

        return array

    def get_reward(self, player):
        """
        calculates the reward

        :param player: player object in the graph
        :return: the current reward
        """
        total_troops = 0

        for n in range(0, len(self.graph.nodes)):
            if self.graph.nodes[n].player == player:
                total_troops += self.graph.nodes[n].troops

        reward = total_troops - self.agent_troops_count
        self.agent_troops_count = total_troops
        return reward


def to_one_hot(n, limit):
    array = np.zeros(limit + 1, np.int32)
    array[n] = 1

    return array


if __name__ == '__main__':
    env = RiskEnv()
    env.reset()
    done = False

    n = 0
    # env.render()

    distribute = np.array([0, 0, 0, 0])
    attack = np.array([0, 0, 0, 0])
    shift = np.array([0, 0, 0, 0])

    t1 = time.time()
    for i in range(10):
        observation = env.reset()
        done = False
        while not done:
            observation, reward, done, info = env.step(env.action_space.sample())
            n += 1
        distribute = np.add(distribute, env.dis)
        attack = np.add(attack, env.atk)
        shift = np.add(shift, env.shift)
        # print("step ", n)
        # print("reward: ", reward)
        # env.render()
        # print("winner is ", env.graph.nodes[0].player.name)
    print('Time needed:', time.time() - t1)
    print('Average steps:', n / 10)
    print('Distribute:', np.array(env.dis) / 10)
    print('Attack', np.array(env.atk) / 10)
    print('Shift:', np.array(env.shift) / 10)
