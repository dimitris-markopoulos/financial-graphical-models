import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from scipy.stats import norm
from pgmpy.estimators import PC

def fisherz(df, i, j, cond, col_index):
    i = col_index[i]
    j = col_index[j]
    cond = [col_index[c] for c in cond]
    cols = [i, j] + cond
    X = df.iloc[:, cols].to_numpy()
    C = np.corrcoef(X, rowvar=False)
    try: P = np.linalg.inv(C)
    except: return False
    rho = -P[0,1]/np.sqrt(P[0,0]*P[1,1])
    n = X.shape[0]
    z = 0.5*np.log((1+rho)/(1-rho))
    stat = np.sqrt(max(n-len(cond)-3,1))*abs(z)
    return stat <= norm.ppf(0.975)

def run_pc(df):
    pc = PC(df)
    col_index = {col:i for i,col in enumerate(df.columns)}
    def ci(x, y, z, **k):
        return fisherz(df, x, y, z, col_index)
    return pc.estimate(significance_level=0.05, ci_test=ci,
                       n_jobs=1, show_progress=False)

def plot_graph(G, title, path=None):
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(10,10))
    nx.draw(G, pos, with_labels=True, arrows=True, arrowstyle='-|>', arrowsize=15,
            node_color="lightblue", node_size=900)
    if path is not None: plt.savefig(path)
    plt.title(title); plt.axis("off"); plt.show()
