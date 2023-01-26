import dataclasses
import functools
import typing

__all__ = [
    'Ordering',
]

_N = typing.TypeVar('_N')


@dataclasses.dataclass
class Ordering(typing.Generic[_N]):
    graph: typing.Mapping[_N, typing.Iterable[_N]]
    """
    A class for computing an ordering of the nodes in a graph.
    
    If the graph has loops, the nodes in the same SCC should have the same order.

    Attributes:
        graph (dict[_N, typing.Iterable[_N]]): A dictionary representing the graph, where the keys are the nodes and the
        values are iterables of the nodes that each key node has edges to.
    """
    
    @functools.cached_property
    def strongly_connected_components(self) -> set[frozenset[_N]]:
        stack: list[_N] = []
        safe_set = set()
        index: dict[_N, int] = {}
        low_link: dict[_N, int] = {}
        clusters: set[frozenset[_N]] = set()
        
        def visit(origin: _N):
            index[origin] = len(index)
            low_link[origin] = index[origin]
            stack.append(origin)
            safe_set.add(origin)
            
            for target in self.graph[origin]:
                if target not in index:
                    visit(target)
                    low_link[origin] = min(low_link[origin], low_link[target])
                elif target in safe_set:
                    low_link[origin] = min(low_link[origin], index[target])
            
            if low_link[origin] == index[origin]:
                strongly_connected_component: set[_N] = set()
                target: _N | None = None
                while origin != target:
                    target = stack.pop()
                    strongly_connected_component.add(target)
                    safe_set.remove(target)
                clusters.add(frozenset(strongly_connected_component))
        
        for v in self.graph:
            if v not in index:
                visit(v)
        
        return clusters
    
    @functools.cached_property
    def get_scc_order(self) -> typing.Callable[[frozenset[_N]], int]:
        @functools.lru_cache
        def function(scc: frozenset[_N]) -> int:
            """
            A function that returns the order of a strongly connected component of the graph.

            Args:
                scc (frozenset[_N]): A frozenset representing a scc of nodes in the graph.
            Returns:
                The order of the scc of nodes.
            """
            
            return max(
                (
                    self.get_node_order(target)
                    for node in scc
                    for target in self.graph.get(node, [])
                    if target not in scc
                ),
                default=-1
            ) + 1
        
        return function
    
    @functools.cached_property
    def get_node_order(self) -> typing.Callable[[_N], int]:
        @functools.lru_cache
        def function(node: _N) -> int:
            """
            A function that returns the order of a node in the graph.

            Args:
                node (_N): A node in the graph.
            Returns:
                The order of the node in the graph.
            """
            
            return self.get_scc_order(self.get_node_scc(node))
        
        return function
    
    @functools.cached_property
    def get_node_scc(self) -> typing.Callable[[_N], frozenset[_N]]:
        @functools.lru_cache
        def function(node: _N) -> frozenset[_N]:
            """
            A function that returns the strongly connected component that a node belongs to.

            Args:
                node (_N): A node in the graph.
            Returns:
                A frozenset representing the scc that the node belongs to.
            """
            
            for scc in self.strongly_connected_components:
                if node in scc:
                    return scc
            return frozenset({node})
        
        return function
