import typing

from .List import List

__all__ = [
    'Set',
]

_N = typing.TypeVar('_N')


class Set(List):
    def _add_link(self, origin: _N, target: _N) -> None:
        raise Exception(f"Cannot add links in a {self.__class__.__name__} structure.")
