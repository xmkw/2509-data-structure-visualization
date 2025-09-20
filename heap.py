import matplotlib
matplotlib.use("Agg")            # <— add this
import networkx as nx
import matplotlib.pyplot as plt

def draw_heap(heap):
    G = nx.DiGraph()
    for i, value in enumerate(heap):
        G.add_node(i, label=str(value))
        left, right = 2*i+1, 2*i+2
        if left < len(heap):  G.add_edge(i, left)
        if right < len(heap): G.add_edge(i, right)

    pos = hierarchy_pos(G, 0)
    labels = nx.get_node_attributes(G, 'label')

    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, labels=labels,
            node_size=1000, node_color='lightblue',
            font_size=10, arrows=False)
    plt.title("Heap Visualization", fontsize=14)
    plt.savefig("heap.png", bbox_inches="tight", dpi=200)   # <— save instead of show
    print("Saved to heap.png")

def hierarchy_pos(G, root, width=1.0, vert_gap=0.2, vert_loc=0, xcenter=0.5):
    def _hierarchy_pos(node, xcenter, width, pos, level=0):
        pos[node] = (xcenter, vert_loc - level * vert_gap)
        children = list(G.neighbors(node))
        if children:
            dx = width / len(children)
            x = xcenter - width/2 + dx/2
            for c in children:
                pos = _hierarchy_pos(c, x, dx, pos, level+1)
                x += dx
        return pos
    return _hierarchy_pos(root, xcenter, width, {})

heap_array = [3, 5, 10, 11, 8, 20, 14, 15, 18, 9, 12, 25, 30]
draw_heap(heap_array)
