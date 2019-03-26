import numpy as np

"""Functions to help with sampling trees."""

def gen_samples(trees, vectors, vector_lookup, node_list):
    """Creates a generator that returns a tree in BFS order with each node
    replaced by its vector embedding, and a child lookup table."""

    node_lookup = {node: _onehot(i, len(node_list)*2) for i, node in enumerate(node_list)}

    for i, tree in enumerate(trees):
        nodes = []
        children = []

        queue = [(tree, -1)]
        while queue:
            node, parent_ind = queue.pop(0)
            node_ind = len(nodes)
            queue.extend([(child, node_ind) for child in node['children']])
            # create a list to store this node's children indices
            children.append([])
            # add this child to its parent's child list
            if parent_ind > -1:
                children[parent_ind].append(node_ind)

            if isinstance(node['node'], list):
                # print('list', node['node'])
                for nod in node['node']:
                    node_vector = np.zeros(2*len(node_list))
                    if nod in vector_lookup:
                        node_vector += np.concatenate([np.zeros(len(node_list)), vectors[vector_lookup[nod]]])
                    else:
                        node_vector += np.concatenate([np.zeros(len(node_list)), vectors[vector_lookup[b'[unknown]']]])
                nodes.append(node_vector)
            else:
                if node['node'] in node_lookup:
                    nodes.append(node_lookup[node['node']])
                else:
                    nodes.append(node_lookup['unknown'])

        yield (nodes, children)

def batch_samples(gen, batch_size):
    """Batch samples from a generator"""
    nodes, children = [], []
    samples = 0
    for n, c in gen:
        nodes.append(n)
        children.append(c)
        samples += 1
        if samples >= batch_size:
            yield _pad_batch(nodes, children)
            nodes, children = [], []
            samples = 0

    if nodes:
        yield _pad_batch(nodes, children)


def _pad_batch(nodes, children):
    if not nodes:
        return [], [], []
    max_nodes = max([len(x) for x in nodes])
    max_children = max([len(x) for x in children])
    feature_len = len(nodes[0][0])
    child_len = max([len(c) for n in children for c in n])

    nodes = [n + [[0] * feature_len] * (max_nodes - len(n)) for n in nodes]
    # pad batches so that every batch has the same number of nodes
    children = [n + ([[]] * (max_children - len(n))) for n in children]
    # pad every child sample so every node has the same number of children
    children = [[c + [0] * (child_len - len(c)) for c in sample] for sample in children]

    return nodes, children


def _onehot(i, total):
    return [1.0 if j == i else 0.0 for j in range(total)]
