import typing

from .DirectedGraph import DirectedGraph

__all__ = [
    'DirectedAcyclicGraph',
]

_N = typing.TypeVar('_N')


class DirectedAcyclicGraph(DirectedGraph[_N], typing.Generic[_N]):
    def _add_link(self, origin: _N, target: _N) -> None:
        if origin == target or self.can_reach(target, origin):
            raise Exception(f"No loop allowed in a {self.__class__.__name__} structure.")
        
        super()._add_link(origin, target)
    
    def get_origin_order(self, node: _N) -> int:
        origins = self.origins(node)
        if not origins:
            return 0
        
        return max(map(self.get_origin_order, origins)) + 1
    
    def get_target_order(self, node: _N) -> int:
        targets = self.targets(node)
        if not targets:
            return 0
        
        return max(map(self.get_target_order, targets)) + 1
