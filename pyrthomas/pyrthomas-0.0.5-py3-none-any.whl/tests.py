from operator import eq
from unittest import TestCase

import networkx as nx

from .cytoscape import read_sif, write_sif
from .models import Node, Edge
from .network import NetworkService
from .network_analyser import NetworkAnalyser


class NetworkTestCase(TestCase):
    def setUp(self):
        self.network_service = NetworkService()
        x = Node('x', 0, 2)
        y = Node('y', 0, 1)
        edge1 = Edge(x.id, y.id, 1)
        edge2 = Edge(y.id, x.id, -1)
        edge3 = Edge(x.id, x.id, 2)
        self.network_service.add_node(x)
        self.network_service.add_node(y)
        self.network_service.add_edge(edge1)
        self.network_service.add_edge(edge2)
        self.network_service.add_edge(edge3)

    def test_predecessor_combinations(self):
        predecessor_combinations = NetworkAnalyser.get_predecessors(self.network_service.network)
        expected_x = ((), ('y',), ('x',), ('y', 'x'))
        self.assertTupleEqual(predecessor_combinations['x'], expected_x)

    def test_state_space(self):
        nodes = self.network_service.network.nodes
        result = list(NetworkAnalyser.generate_state_space(self.network_service.network))
        expected = [{'x': 0, 'y': 0}, {'x': 0, 'y': 1}, {'x': 1, 'y': 0}, {'x': 1, 'y': 1}, {'x': 2, 'y': 0},
                    {'x': 2, 'y': 1}]
        self.assertListEqual(result, expected)

    def test_state_graph(self):
        parameters = {
            "x": [
                ([], 0,), (['x'], 2), (['y'], 2), (['x', 'y'], 2)
            ],
            "y": [
                ([], 0,), (['x'], 1)
            ]
        }
        graph = NetworkAnalyser.get_state_graph(self.network_service.network, parameters)
        result = list(graph.nodes)
        expected = ['0,0', '0,1', '1,0', '1,1', '2,0', '2,1']
        self.assertListEqual(result, expected)

    def test_sif_converter(self):
        write_sif(self.network_service.network, 'test.sif')
        G = read_sif("test.sif")
        em = nx.algorithms.isomorphism.generic_edge_match('weight', 1, lambda x, y: eq(str(x), str(y)))
        result = nx.is_isomorphic(self.network_service.network, G, edge_match=em)
        self.assertTrue(result)

    def test_get_all_possible_params(self):
        graphs = NetworkAnalyser.get_possible_parameters(self.network_service.network)
        print(graphs)
        self.assertTrue(True)

    def tearDown(self):
        self.network_service.clear()
