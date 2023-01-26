# Terminology

## Node

A node can be anything that can be connected by links within a graph.

### Target

If there is a link in the graph that allow to travel from A to B, then B is a target of A.

### Origin

If there is a link in the graph that allow to travel from A to B, then A is an origin of B.

## Link

A link between two nodes (A <-> B) which is symmetric (`A <-> B == B <-> A`)

## Directed Link (DL)

A kind of link between two nodes that is not symmetric (`A -> B != B -> A`)

### Origin

A DL origin is the starting node of the link. (`origin -> ...`)

### Target

A DL target is the ending node of the link. (`... -> target`)

## Directed Graph (DG)

Is a graph containing a set of nodes and a set of directed links between those nodes.

## Directed Acyclic Graph (DAG)

Is a kind of DG that does not have/allow link loops, in other words, we cannot go from a node A to this
same node A using directed links.

## Strongly Connected Component (SCC)

Is a subset of nodes in a DG such that if we use only the links within this subset we can start from
any of its nodes and reach any other.
