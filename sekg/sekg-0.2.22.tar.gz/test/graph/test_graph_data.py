#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sekg.graph.exporter.graph_data import GraphData

graph_data = GraphData()

graph_data.add_node({"method"}, {"qualified_name": "ArrayList.add"})
graph_data.add_node({"override method"}, {"qualified_name": "ArrayList.pop"})
graph_data.add_node({"method"}, {"qualified_name": "ArrayList.remove"})
graph_data.add_node({"method"}, {"qualified_name": "ArrayList.clear"})

graph_data.print_graph_info()
print(graph_data.id_to_node_map)

graph_data.add_relation(1, "related to", 2)
graph_data.add_relation(1, "related to", 3)
graph_data.add_relation(1, "related to", 4)
graph_data.add_relation(2, "related to", 3)
graph_data.add_relation(3, "related to", 4)

print(graph_data.out_relation_map)
print(graph_data.in_relation_map)
print(graph_data.relation_type_to_relation_json_map)

print("#" * 50)
graph_data.merge_two_nodes_by_id(1, 2)

print(graph_data.id_to_node_map)
print(graph_data.out_relation_map)
print(graph_data.in_relation_map)
print(graph_data.relation_type_to_relation_json_map)
