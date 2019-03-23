import hashlib


class IdVault(object):

    def __init__(self):
        self._known_ids = {}
        self._sub_graphs = set()

    def __call__(self, input_text, statement_arguments):
        long_hash = self._calc_hash(input_text, statement_arguments)
        already_known = self._find_in_known(long_hash)
        short_id = already_known or self._evaluate_shortest_unique_hash(long_hash)
        return already_known, short_id

    @staticmethod
    def _calc_hash(input_text, statement_arguments):
        attr_str = ", ".join([str(input_text)] + ["{}={}".format(k, v) for k, v in sorted(statement_arguments.items())])
        return hashlib.sha1(attr_str.encode("utf-8")).hexdigest()

    def _find_in_known(self, long_hash_string):
        for short, long in self._known_ids.items():
            if long == long_hash_string:
                return short

    def _evaluate_shortest_unique_hash(self, long_hash_string):
        for length in range(1, len(long_hash_string)):
            short_id = "n_" + long_hash_string[:length]
            if short_id not in self._known_ids:
                self._known_ids[short_id] = long_hash_string
                return short_id
            elif self._known_ids[short_id] == long_hash_string:
                return short_id
        raise ValueError("Id value collision: {}.".format(long_hash_string))

    def eval_sub_graph_name(self, dot_attrs):
        name = dot_attrs.pop("name", "cluster")
        if not name.startswith("cluster"):
            name = "cluster_" + name

        if name == "cluster" or name in self._sub_graphs:
            number = 0
            while True:
                new_name = "{}_{}".format(name, number)
                if new_name not in self._sub_graphs:
                    name = new_name
                    break
                number += 1

        self._sub_graphs.add(name)
        return name
