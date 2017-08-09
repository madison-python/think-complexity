import warnings
warnings.filterwarnings('ignore')

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from numpy import random


def all_pairs(nodes):
    for i, u in enumerate(nodes):
        for j, v in enumerate(nodes):
            if i < j:
                yield u, v

def make_complete_graph(n):
    G = nx.Graph()
    nodes = range(n)
    G.add_nodes_from(nodes)
    G.add_edges_from(all_pairs(nodes))
    return G

def random_pairs(nodes, p):
    for i, u in enumerate(nodes):
        for j, v in enumerate(nodes):
            if i<j and flip(p):
                yield u, v

def make_random_graph(n, p):
    G = nx.Graph()
    nodes = range(n)
    G.add_nodes_from(nodes)
    G.add_edges_from(random_pairs(nodes, p))
    return G

def flip(p):
    return random.random() < p

def adjacent_edges(nodes, halfk):
    """Yields edges between each node and `halfk` neighbors.

    halfk: number of edges from each node
    """
    n = len(nodes)
    for i, u in enumerate(nodes):
        for j in range(i+1, i+halfk+1):
            v = nodes[j % n]
            yield u, v

def make_ring_lattice(n, k):
    """Makes a ring lattice with `n` nodes and degree `k`.

    Note: this only works correctly if k is even.

    n: number of nodes
    k: degree of each node
    """
    G = nx.Graph()
    nodes = range(n)
    G.add_nodes_from(nodes)
    G.add_edges_from(adjacent_edges(nodes, k//2))
    return G


def make_ws_graph(n, k, p):
    """Makes a Watts-Strogatz graph.

    n: number of nodes
    k: degree of each node
    p: probability of rewiring an edge
    """
    ws = make_ring_lattice(n, k)
    rewire(ws, p)
    return ws

def rewire(G, p):
    """Rewires each edge with probability `p`.

    G: Graph
    p: float
    """
    nodes = set(G.nodes())
    for edge in G.edges():
        if flip(p):
            u, v = edge
            choices = nodes - {u} - set(G[u])
            new_v = random.choice(tuple(choices))
            G.remove_edge(u, v)
            G.add_edge(u, new_v)

def clustering_coefficient(G):
    """Average of the local clustering coefficients.

    G: Graph

    returns: float
    """
    cc = np.mean([node_clustering(G, node) for node in G])
    return cc

def node_clustering(G, u):
    """Computes local clustering coefficient for `u`.

    G: Graph
    u: node

    returns: float
    """
    neighbors = G[u]
    k = len(neighbors)
    if k < 2:
        return 0

    total = k * (k-1) / 2
    exist = 0
    for v, w in all_pairs(neighbors):
        if G.has_edge(v, w):
            exist +=1
    return exist / total


def path_lengths(G):
    length_map = nx.shortest_path_length(G)
    lengths = [length_map[u][v] for u, v in all_pairs(G)]
    return lengths

def characteristic_path_length(G):
    return np.mean(path_lengths(G))


def run_experiment(ps, n=1000, k=10, iters=20):
    """Computes stats for WS graphs with a range of `p`.

    ps: sequence of `p` to try
    n: number of nodes
    k: degree of each node
    iters: number of times to run for each `p`

    returns: sequence of (mpl, cc) pairs
    """
    res = {}
    for p in ps:
        res[p] = []
        for _ in range(iters):
            res[p].append(run_one_graph(n, k, p))
    return res

def run_one_graph(n, k, p):
    """Makes a WS graph and computes its stats.

    n: number of nodes
    k: degree of each node
    p: probability of rewiring

    returns: tuple of (mean path length, clustering coefficient)
    """
    ws = make_ws_graph(n, k, p)
    mpl = characteristic_path_length(ws)
    cc = clustering_coefficient(ws)
    return mpl, cc
