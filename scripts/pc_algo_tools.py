import numpy as np
import itertools
import networkx as nx
import matplotlib.pyplot as plt
from scipy.stats import norm

def fisher_z_verbose(X, i, j, cond, alpha=0.05):
    X_sub = X[:, [i, j] + cond]
    corr = np.corrcoef(X_sub, rowvar=False)
    prec = np.linalg.inv(corr)
    rho = -prec[0,1] / np.sqrt(prec[0,0]*prec[1,1])

    n = X_sub.shape[0]
    z = 0.5 * np.log((1+rho)/(1-rho))
    stat = np.sqrt(n - len(cond) - 3) * abs(z)
    crit = norm.ppf(1 - alpha/2)

    independent = stat <= crit

    return independent, {
        "i": i, "j": j, "cond": cond,
        "rho": rho, "z": z, "stat": stat,
        "crit": crit, "independent": independent
    }


def plot_graph(G, ax, title, pos):
    nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color="black", ax=ax)
    ax.set_title(title)


def pc_skeleton_verbose_plot(X, nodes, axarr, alpha=0.05):
    import itertools

    # fixed layout
    base_G = nx.Graph(); base_G.add_nodes_from(nodes)
    fixed_pos = nx.spring_layout(base_G, seed=42)

    p = len(nodes)
    index = {node: k for k, node in enumerate(nodes)}

    # initial graph
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from([(nodes[i], nodes[j]) for i in range(p) for j in range(i+1,p)])

    logs = []
    level = 0
    removed_any = True

    # plot level 0 BEFORE any tests
    plot_graph(G, axarr[0], "Level 0 (Unconditional)", fixed_pos)

    while removed_any:
        removed_any = False
        edges = list(G.edges())

        # test all edges at this level
        for (u, v) in edges:

            nbrs = list(set(G.neighbors(u)) - {v})
            if len(nbrs) < level:
                continue

            # all conditioning sets of size = level
            for cond in itertools.combinations(nbrs, level):
                cond_idx = [index[c] for c in cond]

                indep, details = fisher_z_verbose(X, index[u], index[v], cond_idx, alpha)

                logs.append({
                    "level": level,
                    "edge": f"{u}-{v}",
                    "u": u,
                    "v": v,
                    "cond_set": cond,
                    **details
                })

                if indep:
                    G.remove_edge(u, v)
                    logs[-1]["removed"] = True
                    removed_any = True
                    break
                else:
                    logs[-1]["removed"] = False

        level += 1

        # plot each level if panel exists
        if level < len(axarr):
            plot_graph(G, axarr[level], f"Level {level}", fixed_pos)

    return G, logs

def df_to_image(df, filename="pc_logs.png", max_rows=30):
    df_show = df if len(df) <= max_rows else df.iloc[:max_rows]
    fig, ax = plt.subplots(figsize=(16, min(1 + 0.4 * len(df_show), 20)))
    ax.axis('off')
    table = plt.table(
        cellText=df_show.values,
        colLabels=df_show.columns,
        loc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)
    
    plt.savefig(filename, bbox_inches='tight', dpi=300)
    plt.close()