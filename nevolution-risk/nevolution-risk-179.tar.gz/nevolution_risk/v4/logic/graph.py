import os

import networkx as nx

from nevolution_risk.constants.colors import green, deepskyblue, darkviolet, orange
from nevolution_risk.v4.logic.card_factory import Card_factory
from nevolution_risk.v4.logic.continent import Continent
from nevolution_risk.v4.logic.continent_loader import ContinentLoader
from nevolution_risk.v4.logic.graphlogic import GraphLoader, RiskGraph
from nevolution_risk.v4.logic.node import Node
from nevolution_risk.v4.logic.player import Player


class Graph(object):
    default_positions = []
    for i in range(0, 42):
        default_positions.append((4, i % 4))

    def __init__(self, seed=42, player_positions=None, player_count=4):
        self.player_count = player_count
        loader = GraphLoader()
        dir_name = os.path.dirname(os.path.realpath(__file__))
        source_graph = loader.load_graph(os.path.join(dir_name, '../../res', 'small.txt'))
        self.graph = RiskGraph(graph=source_graph[0], coord=source_graph[1])
        self.nodes = []
        for n in range(0, self.graph.node_count):
            self.add_node(Node(n, self.graph.get_attributes(n)))

        for n in range(0, self.graph.node_count):
            for m in self.graph.get_adjlist()[n]:
                self.nodes[n].add_node_to_list(self.nodes[m])
                self.nodes[m].add_node_to_list(self.nodes[n])

        continents = ContinentLoader().load_continents(os.path.join(dir_name, '../../res', 'continents.txt'))
        self.continents = []
        n = 0
        countries = []
        for continent in continents:
            for country in continent:
                countries.append(self.nodes[country])
            Continent(n, countries)
            self.continents.append(Continent(n, countries))
            countries = []
            n = n + 1

        edges = []
        for line in nx.generate_edgelist(self.graph):
            edges.append(line)
        edge_count = len(edges)
        action_len = edge_count * 4 + 1

        self.seed = seed
        self.card_fac = Card_factory(seed)

        self.card_fac1 = Card_factory(seed)

        self.card_fac2 = Card_factory(seed)

        self.card_fac3 = Card_factory(seed)

        self.players = []
        self.players.append(Player('player_one', 0, green, action_len, self.card_fac))
        self.players.append(Player("player_two", 1, deepskyblue, action_len, self.card_fac1))
        self.players.append(Player("player_three", 2, darkviolet, action_len, self.card_fac2))
        self.players.append(Player("player_four", 3, orange, action_len, self.card_fac3))

        self.current_player = self.players[0]

        for i in range(0, len(self.players) - 1):
            self.players[i].next_player = self.players[i + 1]

        self.players[-1].next_player = self.players[0]

        i = 0

        if player_positions is None:
            initial_state = self.default_positions
        else:
            initial_state = player_positions

        for node in self.nodes:
            if i < len(initial_state):
                node.troops = initial_state[i][0]
                node.player = self.players[initial_state[i][1]]
            i = i + 1

    def add_node(self, node):
        self.nodes.append(node)

    def next_player(self):
        """
        Sets current player to next player. If there is no next player, an error massage appears.
        If the next player lost, the next player of him would be taken and so on.
        If there is no next player of him, an error massage appears
        and if all players lost (???) an error massage appears.

        :return: None
        """
        next_player = self.current_player

        i = 0
        if next_player.next_player is None:
            print("in next_player: next player would be None")
        else:
            next_player = next_player.next_player

        while next_player.lost:
            if next_player.next_player is None:
                print("in next_player: next player would be None")
                break
            elif i > len(self.players):
                print("in next_player: all players lost???")
            else:
                next_player = next_player.next_player
            i = i + 1

        self.current_player = next_player
        self.current_player.card_received = False
        self.reset_marks()
        self.add_troops()

    def add_troops(self):
        """
        Adding troop units to current players reserve from round_reward and continents

        :return: None
        """
        self.current_player.troops = self.current_player.troops + self.round_reward()

        for continent in self.continents:
            var = 0
            for node in continent.nodes:
                if node.player == self.current_player:
                    var = var + 1
            if var == len(continent.nodes):
                self.current_player.troops = self.current_player.troops + continent.reward()

        self.current_player.combine_cards()

        if self.current_player.lost:
            self.current_player.troops = 0

    def round_reward(self):
        """
        Counting all territories from the current player and divide it through 3 to get reward.
        The reward can't get less than 3.

        :return: integer, number of troop units
        """
        territories = 0
        for node in self.nodes:
            if node.player == self.current_player:
                territories = territories + 1

        troops = territories / 3
        troops = int(troops)
        if troops < 3:
            troops = 3

        return troops

    def is_conquered(self):
        """
        Marks a player who get conquered

        :return:    if one player is left it returns True, else it returns False
                    also returns true when player-one has lost
        """
        for player in self.players:
            i = 0
            for node in self.nodes:
                if player == node.player:
                    i = i + 1
                    break

            if i == 0:
                player.lost = True

        i = 0
        for player in self.players:
            if not player.lost:
                i = i + 1

        if self.players[0].lost:
            return True

        return i < 2

    def distribute(self, node):
        """
        Sets one troop unit from current players reserve to an owned node

        :param node: integer, target node
        :return: None
        """

        if self.current_player.troops > 0:
            self.nodes[node].troops = self.nodes[node].troops + 1
            self.current_player.troops = self.current_player.troops - 1

    def fortify(self, start_node_index, finish_node_index):
        """
        Moves three troop units (if possible) from an owned node to another owned node. Sets the start node to True,
        so no other fortify move on this Node is possible

        :param start_node_index: integer, start node
        :param finish_node_index: integer, finish node
        :return: None
        """

        start = self.nodes[start_node_index]
        finish = self.nodes[finish_node_index]

        if start.troops >= 2 and start.player == finish.player and not finish.marked:
            moved = min(start.troops - 1, 3)
            start.troops -= moved
            finish.troops += moved
            start.marked = True

    def reset_marks(self):
        """
        Resets all marked Nodes to False

        :return: None
        """
        for node in self.nodes:
            node.marked = False

    def attack(self, node1, node2, all_troops):
        """
        Attacks in a fight simulation the finish node from the start node.

        :param node1: integer, start node
        :param node2: integer, finish node
        :param all_troops: integer, number of troops
        :return: True if the attack was successful and False if it was a failure
        """

        start = self.nodes[node1]
        finish = self.nodes[node2]

        attack_size = start.troops - 1
        if attack_size <= 0:
            return False
        if attack_size > 3:
            attack_size = 3

        attack_casualties, def_casualties = self.fight_simulation(attack_size, finish.troops)
        start.troops = start.troops - attack_casualties
        finish.troops = finish.troops - def_casualties
        if finish.troops >= 1:
            return False
        start.player.reward += 1
        finish.player.reward -= 1
        finish.player = start.player
        if all_troops:
            finish.troops = start.troops - 1
            start.troops = 1
        else:
            finish.troops = 1
            start.troops = start.troops - 1
        return True

    @staticmethod
    def fight_simulation(attack_size, def_troop):
        # hard coded in version 4
        # rng goes here in version 5
        """
        Simulate an attack with its troops loss.

        :param attack_size: integer, number of attacking troops
        :param def_troop: integer, number of defending troops
        :return: integer, integer; lost attacking troops, lost defending troops
        """
        attack_casualties = 0
        def_casualties = 0

        if def_troop < 0 or attack_size < 0:
            raise ValueError("number attackers and defenders must not be negative")
        if def_troop == 0:
            attack_casualties = 0
            def_casualties = 0
        elif def_troop == 1:
            if attack_size >= 3:
                attack_casualties = 0
                def_casualties = 1
            if attack_size == 2:
                attack_casualties = 1
                def_casualties = 1
            if attack_size == 1:
                attack_casualties = 1
                def_casualties = 0
        else:
            if attack_size >= 3:
                attack_casualties = 1
                def_casualties = 2
            if attack_size == 2:
                attack_casualties = 2
                def_casualties = 1
            if attack_size == 1:
                attack_casualties = 1
                def_casualties = 0
        return attack_casualties, def_casualties


if __name__ == '__main__':
    graph = Graph()
    for node in graph.nodes:
        print(node.x, node.y)

    elem = (1, 1)
    print(isinstance(elem[0], int))
