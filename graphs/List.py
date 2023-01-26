import typing

from .Tree import Tree

__all__ = [
    'List',
]

_N = typing.TypeVar('_N')


class List(Tree):
    def _add_link(self, origin: _N, target: _N) -> None:
        if self.origins(target):
            raise Exception(f"Cannot add more than 1 origin to a node in a {self.__class__.__name__} structure.")
        
        if self.targets(origin):
            raise Exception(f"Cannot add more than 1 target to a node in a {self.__class__.__name__} structure.")
        
        super()._add_link(origin, target)
