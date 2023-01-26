import unittest

from graphs import *


class TestStructures(unittest.TestCase):
    def test_001(self):
        dg = DirectedGraph()
        dag = DirectedAcyclicGraph()
        tree = Tree()
        list_ = List()
        set_ = Set()


if __name__ == '__main__':
    unittest.main()
