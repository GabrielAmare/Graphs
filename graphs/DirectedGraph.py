import typing

__all__ = [
    'DirectedGraph'
]

_N = typing.TypeVar('_N')


class DirectedGraph(typing.Generic[_N], typing.Mapping[_N, set[_N]]):
    def __init__(self, __data: typing.Mapping[_N, typing.Iterable[_N]] | None = None):
        self._data: dict[_N, set[_N]] = {}
        
        if __data:
            for origin, targets in __data.items():
                if not self.has_node(origin):
                    self._add_node(origin)
                for target in targets:
                    if not self.has_node(target):
                        self._add_node(target)
                    if not self.has_link(origin, target):
                        self._add_link(origin, target)
    
    def __iter__(self):
        return iter(self._data)
    
    def __len__(self):
        return len(self._data)
    
    def __getitem__(self, node: _N) -> set[_N]:
        return self._data[node]
    
    def __setitem__(self, origin: _N, targets: set[_N]):
        if origin not in self._data:
            self._add_node(origin)
        to_del = self._data[origin].difference(targets)
        to_add = targets.difference(self._data[origin])
        for target in to_del:
            self.del_link(origin, target)
        for target in to_add:
            self._add_link(origin, target)
    
    def __delitem__(self, node: _N) -> None:
        self.del_node(node)
    
    def has_node(self, node: _N) -> bool:
        return node in self._data
    
    def _add_node(self, node: _N) -> None:
        assert node not in self._data
        self._data[node] = set()
    
    def add_node(self, node: _N) -> None:
        if not self.has_node(node):
            self._add_node(node)
    
    def del_node(self, node: _N) -> None:
        assert node in self._data
        del self._data[node]
        for targets in self._data.values():
            if node in targets:
                targets.remove(node)
    
    def has_link(self, origin: _N, target: _N) -> bool:
        return origin in self._data and target in self._data[origin]
    
    def _add_link(self, origin: _N, target: _N) -> None:
        assert origin in self._data
        assert target not in self._data[origin]
        self._data[origin].add(target)
    
    def add_link(self, origin: _N, target: _N) -> None:
        if not self.has_link(origin, target):
            self.add_node(origin)
            self.add_node(target)
            self._add_link(origin, target)
    
    def del_link(self, origin: _N, target: _N) -> None:
        assert origin in self._data
        assert target in self._data[origin]
        self._data[origin].remove(target)
    
    def targets(self, origin: _N) -> set[_N]:
        return self._data.get(origin, set())
    
    def origins(self, target: _N) -> set[_N]:
        return set(
            origin
            for origin, targets in self._data.items()
            if target in targets
        )
    
    def explore_targets(self, initial: _N) -> typing.Iterator[_N]:
        """Yields the nodes that can be reached from `origin`."""
        queue = [initial]
        index = 0
        while index < len(queue):
            node = queue[index]
            index += 1
            
            for target in self.targets(node):
                yield target
                
                if target not in queue:
                    queue.append(target)
    
    def explore_origins(self, initial: _N) -> typing.Iterator[_N]:
        """Yields the nodes that can be reversed reached from `targets`."""
        queue = [initial]
        index = 0
        while index < len(queue):
            node = queue[index]
            index += 1
            
            for origin in self.origins(node):
                yield origin
                
                if origin not in queue:
                    queue.append(origin)
    
    def can_reach(self, origin: _N, target: _N) -> bool:
        """Return True when it exists a path to link `origin` to `target`."""
        
        for node in self.explore_targets(origin):
            if node == target:
                return True
        
        return False
