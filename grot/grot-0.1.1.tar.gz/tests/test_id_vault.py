from grot import IdVault


def test_id_vault():
    vault = IdVault()

    # check that when asked first time - calculates unique ids for different call statements
    assert [(k,) + vault("content", {'arg': k}) for k in range(4)] == [
        (0, None, 'n_7'),
        (1, None, 'n_f'),
        (2, None, 'n_d'),
        (3, None, 'n_79'),
    ]
    # check that when asked second time - indicates it's already known hash
    assert [(k,) + vault("content", {'arg': k}) for k in range(6)] == [
        (0, 'n_7', 'n_7'),
        (1, 'n_f', 'n_f'),
        (2, 'n_d', 'n_d'),
        (3, 'n_79', 'n_79'),
        (4, None, 'n_9'),
        (5, None, 'n_90')
    ]

    assert vault._known_ids == {
        'n_7': '7dd1d46df95a4069950b04f0f088f0a0fe787ced',
        'n_79': '79f0cadf37c16c170065d7b9661f24eb33f16e56',
        'n_9': '9c6e1ada077d2eb7f702646456be76b88d78fa96',
        'n_90': '9092f9b2bbf7d9468efe6e57599537dbdefe506f',
        'n_d': 'd418a2bc11706f0bbc4b57a7a5a90ea7f2e6d67a',
        'n_f': 'f9f31b0d213f2fce1e478783a2bb16d59dbc6cb6',
    }


def test_subgraph_names():
    vault = IdVault()

    names = [vault.eval_sub_graph_name({}) for _ in range(4)]
    assert names == ['cluster_0', 'cluster_1', 'cluster_2', 'cluster_3']
    assert vault.eval_sub_graph_name({'name': 'bad_name'}) == "cluster_bad_name"
    assert vault.eval_sub_graph_name({'name': 'bad_name'}) == "cluster_bad_name_0"
    assert vault.eval_sub_graph_name({'name': 'cluster_bad_name'}) == "cluster_bad_name_1"
    assert vault.eval_sub_graph_name({'name': 'cluster_bad_name'}) == "cluster_bad_name_2"
    assert vault.eval_sub_graph_name({'name': 'bad_name'}) == "cluster_bad_name_3"
