import matplotlib
matplotlib.use("Agg")  # must be set before importing pyplot
import matplotlib.pyplot as plt
import networkx as nx

def draw_ordered_tree(adj, root, filename="multiway_tree.png",
                      node_size=1100, font_size=10, level_gap=1.2, sib_gap=1.0):
    """
    Draw an ordered multiway tree.

    Parameters
    ----------
    adj : dict[str, list[str]]
        Adjacency list mapping parent -> ordered list of children.
        Children order in the lists is preserved in the drawing.
    root : str
        Root node id.
    filename : str
        Output image file.
    node_size, font_size : drawing parameters.
    level_gap : float
        Vertical distance between levels.
    sib_gap : float
        Horizontal base gap between adjacent leaves (controls overall width).
    """
    # Build a DiGraph and preserve child order by adding edges in given order
    G = nx.DiGraph()
    nodes = set([root])
    for p, kids in adj.items():
        nodes.add(p)
        for c in kids:
            nodes.add(c)
            G.add_edge(p, c)  # order preserved by insertion

    # Simple layout that preserves child order
    pos = ordered_tree_layout(G, root, level_gap=level_gap, leaf_gap=sib_gap)

    plt.figure(figsize=(max(6, 0.8 * len(pos)), 6))
    nx.draw_networkx_edges(G, pos, arrows=False, width=1.2)
    nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color="#C7E9F1", edgecolors="black", linewidths=1.0)
    nx.draw_networkx_labels(G, pos, font_size=font_size)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(filename, dpi=220, bbox_inches="tight")
    print(f"Saved to {filename}")

def ordered_tree_layout(G, root, level_gap=1.2, leaf_gap=1.0):
    """Compute a simple order-preserving layout for a rooted tree."""
    children = {u: list(G.successors(u)) for u in G.nodes()}
    depth = {root: 0}
    q = [root]
    while q:
        u = q.pop(0)
        for v in children.get(u, []):
            depth[v] = depth[u] + 1
            q.append(v)

    xcoord = {}
    next_x = [0.0]

    def dfs(u):
        kids = children.get(u, [])
        if not kids:
            xcoord[u] = next_x[0]
            next_x[0] += leaf_gap
        else:
            for k in kids:
                dfs(k)
            xs = [xcoord[k] for k in kids]
            xcoord[u] = (xs[0] + xs[-1]) / 2.0

    dfs(root)

    min_x = min(xcoord.values())
    xcoord = {k: (v - min_x) for k, v in xcoord.items()}
    return {u: (xcoord[u], -depth.get(u, 0) * level_gap) for u in G.nodes()}

if __name__ == "__main__":
    adj = {
        "A": ["B", "C", "D"],
        "B": ["E", "F"],
        "C": ["G", "H", "I"],
        "D": ["J"],
        "G": ["G1", "G2"],
        "J": ["J1", "J2"],
        "J1": ["J1.1", "J1.2"]
    }
    draw_ordered_tree(adj, root="A", filename="multiway_tree.png")
