"""
Consumer factories.

"""


def configure_active_bundle(graph):
    if not hasattr(graph.config, "active_bundle"):
        return None
    return getattr(graph, graph.config.active_bundle)


def configure_active_evaluation(graph):
    if not hasattr(graph.config, "active_evaluation"):
        return None
    return getattr(graph, graph.config.active_evaluation)
