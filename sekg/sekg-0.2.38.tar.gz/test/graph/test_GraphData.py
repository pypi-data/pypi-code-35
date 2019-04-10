from unittest import TestCase

from sekg.graph.exporter.graph_data import GraphData


class TestGraphData(TestCase):

    def test_get_graph(self):
        graph_data = GraphData()

        graph_data.add_node({"method"}, {"qualified_name": "ArrayList.add"})
        graph_data.add_node({"override method"}, {"qualified_name": "ArrayList.pop"})
        graph_data.add_node({"method"}, {"qualified_name": "ArrayList.remove"})
        graph_data.add_node({"method"}, {"qualified_name": "ArrayList.clear"})

        # print(graph_data.find_nodes_by_property_value_starts_with("qualified_name", "ArrayList"))

        # print(graph_data.get_node_ids())
        # print(graph_data.get_relation_pairs_with_type())

        graph_data.add_relation(1, "related to", 2)
        graph_data.add_relation(1, "related to", 3)
        graph_data.add_relation(1, "related to", 4)
        graph_data.add_relation(2, "related to", 3)
        graph_data.add_relation(3, "related to", 4)

        print(graph_data.get_relations(1, "related to"))
        print("get relation by type")
        print(graph_data.get_relations(relation_type="related to"))

        # print(graph_data.get_node_ids())
        # print(graph_data.get_relation_pairs_with_type())

        # print("#" * 50)
        # graph_data.merge_two_nodes_by_id(1, 2)

        # print(graph_data.get_node_ids())
        # print(graph_data.get_relation_pairs_with_type())

    def test_merge(self):
        graph_data = GraphData()
        graph_data.create_index_on_property("qualified_name", "alias")

        graph_data.add_node({"method"}, {"qualified_name": "ArrayList.add"})
        graph_data.add_node({"override method"}, {"qualified_name": "ArrayList.pop"})
        graph_data.add_node({"method"}, {"qualified_name": "ArrayList.remove"})
        graph_data.add_node({"method"}, {"qualified_name": "ArrayList.clear", "alias": ["clear"]})

        graph_data.merge_node(node_labels=["method", "merge"], node_properties={"qualified_name": "ArrayList.clear",
                                                                                "alias": ["clear", "clear1"]
                                                                                },
                              primary_property_name="qualified_name")
