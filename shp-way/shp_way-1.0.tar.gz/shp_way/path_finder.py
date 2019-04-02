import networkx as nx
import enum


class ShortestPathAlgorithm(enum.Enum):
    """
    Enum class to present the different algorithms available
    """
    dijkstra = 1
    a_star = 2
    bellman_ford = 3


def nx_shortest_path(graph, src_entry_nodes, dst_entry_nodes, alg_name=ShortestPathAlgorithm.dijkstra):
    """
    Initialize process to find the shortest path in graph based on algorithm
    :param graph: NetworkX graph
        graph used for path finding
    :param src_entry_nodes: NetworkX node
        source node from graph
    :param dst_entry_nodes: NetworkX node
        destination node from graph
    :param alg_name: enum class ShortestPathAlgorithm attribute
        selected algorithm to determine path
    :return: A path between src and dst
    """
    try:
        if alg_name.value == 1:
            return __nx_dijkstra(graph, src_entry_nodes, dst_entry_nodes)
        elif alg_name.value == 2:
            return __nx_astar(graph, src_entry_nodes, dst_entry_nodes)
        elif alg_name.value == 3:
            return __nx_bellman_ford(graph, src_entry_nodes, dst_entry_nodes)
    except nx.NetworkXNoPath:
        return None


def __nx_dijkstra(graph, src_entry_nodes, dst_entry_nodes):
    """
    Find shortest path between src and dst using Dijkstra's algorithm
    :param graph: NetworkX graph
        graph used for path finding
    :param src_entry_nodes: list of NetworkX nodes
        source nodes from graph
    :param dst_entry_nodes: list of NetworkX nodes
        destination nodes from graph
    :return: list of NetworkX nodes describing the shortest path between src and dst
    """
    path = None
    path_length = None

    for src_entrance in src_entry_nodes:
        for dst_entrance in dst_entry_nodes:
            if path is None and path_length is None:

                path = nx.dijkstra_path(graph, source=src_entrance, target=dst_entrance)
                path_length = nx.dijkstra_path_length(graph, source=src_entrance, target=dst_entrance)
            else:
                temp_length = nx.dijkstra_path_length(graph, source=src_entrance, target=dst_entrance)
                if temp_length < path_length:
                    path = nx.dijkstra_path(graph, source=src_entrance, target=dst_entrance)
                    path_length = temp_length

    return path


def __nx_astar(graph, src_entry_nodes, dst_entry_nodes):
    """
    Find shortest path between src and dst using A star algorithm
    :param graph: NetworkX graph
        graph used for path finding
    :param src_entry_nodes: list of NetworkX nodes
        source nodes from graph
    :param dst_entry_nodes: list of NetworkX nodes
        destination nodes from graph
    :return: list of NetworkX nodes describing the shortest path between src and dst
    """
    path = None
    path_length = None

    for src_entrance in src_entry_nodes:
        for dst_entrance in dst_entry_nodes:
            if path is None and path_length is None:

                path = nx.astar_path(graph, source=src_entrance, target=dst_entrance)
                path_length = nx.astar_path_length(graph, source=src_entrance, target=dst_entrance)
            else:
                temp_length = nx.astar_path_length(graph, source=src_entrance, target=dst_entrance)
                if temp_length < path_length:
                    path = nx.astar_path(graph, source=src_entrance, target=dst_entrance)
                    path_length = temp_length

    return path


def __nx_bellman_ford(graph, src_entry_nodes, dst_entry_nodes):
    """
    Find shortest path between src and dst using Bellman-Ford's algorithm
    :param graph: NetworkX graph
        graph used for path finding
    :param src_entry_nodes: list of NetworkX nodes
        source nodes from graph
    :param dst_entry_nodes: list of NetworkX nodes
        destination nodes from graph
    :return: list of NetworkX nodes describing the shortest path between src and dst
    """
    path = None
    path_length = None

    for src_entrance in src_entry_nodes:
        for dst_entrance in dst_entry_nodes:
            if path is None and path_length is None:

                path = nx.bellman_ford_path(graph, source=src_entrance, target=dst_entrance)
                path_length = nx.bellman_ford_path_length(graph, source=src_entrance, target=dst_entrance)
            else:
                temp_length = nx.bellman_ford_path_length(graph, source=src_entrance, target=dst_entrance)
                if temp_length < path_length:
                    path = nx.bellman_ford_path(graph, source=src_entrance, target=dst_entrance)
                    path_length = temp_length

    return path

