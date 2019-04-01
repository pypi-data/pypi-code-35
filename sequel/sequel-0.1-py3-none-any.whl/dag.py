from concurrent.futures import Executor, Future
import inspect
from functools import reduce, wraps
import random


class Pipeline(object):
    def __init__(self, executor_class=None):
        """
        Create work scheduler.

        Args:
            executor_class (:class:`concurrent.futures.Executor`): Optionally
                provide the execution runtime for each independent set of work
                units. By default, independent sets of work will be run in an
                arbitrary and unstable sequence.

                When using the
                :class:`concurrent.futures.ProcessPoolExecutor`, you need to
                make sure all submitted work is :term:`picklable` to avoid
                a `known race condition`_. Also, one can use something else
                such as :mod:`pathos`.

        .. _known race condition: https://bugs.python.org/issue30006
        """
        self._dependencies = {}
        self._jobs = {}
        self._outputs = {}
        self._data = {}
        self._executor_class = executor_class or _SequentialExecutor

    def make_nodes(self, function, outputs=None):
        """
        Add nodes to the dependency graph based on a function signature.

        Each time this method is called, one or more nodes are added to the
        dependency graph.  If `outputs` is provided, the amount of outputs
        designate the amount of nodes created.

        Parameter names of `function` are dependencies to other nodes.  In
        case multiple outputs are specified, all of them will have all these
        dependencies.

        The number of returned values from `function` must also match the
        amount of outputs or else a :class:`sequel.OutputMismatch` will
        be raised by :meth:`sequel.Pipeline.resolve`.

        Here is simple sum of two other nodes

        .. code-block:: python

                def one():
                    return 1

                def two():
                    return 2

                def add(one, two):
                    return one + two

                graph = Pipeline()
                graph.make_nodes(one)
                graph.make_nodes(two)
                graph.make_nodes(three)

        The resulting graph could be reprensented as followed.

        .. digraph:: simple_sum

            add -> one;
            add -> two;

        .. note:: The arrow direction should be interpreted as
            *depends on*.

        The :paramref:`sequel.Pipeline.make_nodes.output` parameters can
        be used to explicitely specify the nodes names and generate more than
        one node for a given callable:

        .. code-block:: python

            def values():
                return 1,2

            def add(one, two):
                return one + two

            graph = Pipeline()
            graph.make_nodes(values, outputs=('one', 'two'))
            graph.make_nodes(three)

        The resulting graph is the same as above

        .. digraph:: simple_sum

            add -> one;
            add -> two;

        Args:
            function (:ref:`callable-types`) Any callable object.
            outputs: Optionally provide the names of outputs of that callable.
        """
        outputs = outputs if outputs is not None else [function.__name__]
        signature = inspect.signature(function)
        self._outputs[function] = outputs

        for node in outputs:
            self._dependencies[node] = set(signature.parameters)
            self._jobs[node] = function

    def resolve(self, node):
        """
        Resolve a given node of the graph.

        This method will run any callable attached to a given node if it is
        required.  Since node are equivalent to callable outputs, it will
        only be run if the output was not previously generated.

        Args:
            node: A node (or node identifier) to be resolved.

        Returns:
            dc
        """
        try:
            result = self._data[node]
            output_names = [node]
        except KeyError:
            function = self._jobs[node]
            arguments = {argument_name: self._data[argument_name]
                         for argument_name in self._dependencies[node]}
            result = function(**arguments)
            output_names = self._outputs[function]

        if not isinstance(result, tuple):
            result = (result,)

        if len(output_names) != len(result):
            # FIXME
            # This should be raised in earlier (in make_nodes)
            # but there is no way to inspect return statements
            # of a function that is not called yet
            raise OutputMismatch()

        result_by_name = dict(zip(output_names, result))

        return result_by_name

    def execute(self, input=None):
        """
        Resolve all the values of nodes of the graph by executing the
        underlying functions.

        The work to do is sequenced with the topological sort provided by
        :func:`sequel.dag.topological_sort`.

        Independent sets are run in pseudo-parallel based on the executor
        provided to :paramref:`sequel.Pipeline.executor_class`.

        Args:
            input (dict): A flat dictionary of initial values.  Keys must
                match nodes (functions, outputs) names.

        Returns:
            The last resolved value.
        """
        self._data.update(input or {})

        last_result = None

        for independent_sets in topological_sort(self._dependencies):
            results = self._run_independent_sets(independent_sets)
            for result_dict in results:
                self._data.update(result_dict)
                last_result = random.choice(list(result_dict.values()))

        return last_result

    def _run_independent_sets(self, independent_sets):
        with self._executor_class() as executor:
            results = executor.map(self.resolve, independent_sets)

        return results

    def job(self, *decargs, **deckwargs):
        def decorator(f):
            @wraps(self.make_nodes)
            def func_wrapper(f, *args, **kwargs):
                return self.make_nodes(f, *args, **kwargs)
            return func_wrapper(f, *decargs, **deckwargs)
        return decorator

    @property
    def data(self):
        return self._data


class OutputMismatch(ValueError):
    pass


class _SequentialExecutor(Executor):
    def submit(self, fn, *args, **kwargs):
        future = Future()

        result = fn(*args, **kwargs)

        future.set_result(result)

        return future


def topological_sort(graph):
    """
    Make a topological sort of a directed acyclic graph using
    `Kahn's algorithm`_.

    Args:
        graph (dict): A :class:`dict` of :class:`set` objects that maps a
            node to the set of its dependencies.

    Yields:
        :class:`set`: Each yielded item is an independent set.  Elements of
            a given yielded set will only have dependencies on elements of
            previous sets.

    In case you require a flat generator as a result, you could wrap this
    function like the following:

    .. code-block:: python

        def flat_topological_sort(graph):
            for independent_set in topological_sort(graph):
                yield from independent_set
                # For a unique solution, sort the set first:
                # yield from sorted(independent_set)

    .. _Kahn's algorithm: https://en.wikipedia.org/wiki/Topological_sorting
    """
    if not graph:
        return []

    graph = _make_normalized_graph(graph)

    while True:
        nodes_without_deps = _find_nodes_without_deps(graph)

        if not nodes_without_deps:
            break

        yield nodes_without_deps

        graph = _make_graph_excluding_nodes(graph, nodes_without_deps)

    if len(graph):
        raise ValueError


def _find_nodes_without_deps(graph):
    return set(node
               for node, deps in graph.items()
               if not deps)


def _make_graph_excluding_nodes(graph, excluded_nodes):
    return {node: set(deps - excluded_nodes)
            for node, deps in graph.items()
            if node not in excluded_nodes}


def _make_normalized_graph(graph):
    graph = graph.copy()

    for element, dependencies in graph.items():
        dependencies.discard(element)

    graph.update({
        node_found_only_in_deps: set()
        for node_found_only_in_deps in reduce(
            set.union, graph.values()) - set(graph.keys())
    })

    return graph
