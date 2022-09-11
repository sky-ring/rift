from graphlib import TopologicalSorter


def topological(refs):
    graph = {}
    for from_, to_ in refs:
        if from_ not in graph:
            graph[from_] = set()
        graph[from_].add(to_)
    ts = TopologicalSorter(graph)
    return list(ts.static_order())
