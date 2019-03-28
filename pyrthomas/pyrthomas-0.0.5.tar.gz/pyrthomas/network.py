import networkx as nx
from networkx.readwrite import json_graph

from .constants import pickle_key, graphml_file_name, dot_file_name, sif_file_name
from .cytoscape import read_sif, write_sif
from . import utils


class NetworkService:
    network: nx.DiGraph

    def __init__(self) -> None:
        try:
            self.network = nx.read_gpickle(pickle_key)
        except FileNotFoundError:
            self.network = nx.DiGraph()
            nx.write_gpickle(self.network, pickle_key)

    def add_node(self, node):
        self.network.add_node(node.id, min=node.min, max=node.max)
        self.persist_network()

    def add_edge(self, edge):
        self.network.add_edge(edge.source, edge.target, weight=edge.weight)
        self.persist_network()

    def get_nodes(self):
        return list(self.network.nodes)

    def clear(self):
        self.network.clear()
        self.persist_network()

    def get_edges(self):
        return list(self.network.edges)

    def import_graphml(self, file):
        self.network = nx.read_graphml(file)
        self.persist_network()
        return json_graph.node_link_data(self.network)

    def import_dot(self, file):
        self.network = nx.drawing.nx_pydot.read_dot(file)
        self.persist_network()
        return json_graph.node_link_data(self.network)

    def import_sif(self, file):
        self.network = read_sif(file)
        self.persist_network()
        return json_graph.node_link_data(self.network)

    def export_graphml(self):
        file = open(graphml_file_name, "wb")
        nx.write_graphml(self.network, file, prettyprint=True)
        file.close()
        return file.name

    def export_dot(self):
        file = open(dot_file_name, "w")
        nx.drawing.nx_pydot.write_dot(self.network, file)
        file.close()
        return file.name

    def export_sif(self):
        file = open(sif_file_name, "w")
        write_sif(self.network, file)
        file.close()
        return file.name

    def persist_network(self):
        utils.persist_network(self.network, pickle_key)
