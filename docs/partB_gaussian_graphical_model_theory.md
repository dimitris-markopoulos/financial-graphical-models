## Gaussian Graphical Model

### Assumptions
We assume the vector of asset returns follows a multivariate normal distribution: $X \sim \mathcal{N}(0, \Sigma)$.

The **precision matrix** is defined as the inverse covariance: $\Theta = \Sigma^{-1}.$

A fundamental property of multivariate Gaussians: $\Theta_{ij} = 0 \quad\Longleftrightarrow\quad X_i \perp X_j \mid X_{\{1,\dots,p\}\setminus\{i,j\}}$.
This means:
- **Zero entry** $\rightarrow$ conditional independence  
- **Nonzero entry** $\rightarrow$ conditional dependence (an *edge* in the graph)

Thus, the structure of the graphical model (edges / no edges) is read **directly from** the sparsity pattern of $\Theta$.

---

### Motivations
This motivated the question **Why We *Do Not* Use the Sample Inverse Covariance?** or at least this was my first thought.

Although in theory: $\Theta = \Sigma^{-1},$ we almost never estimate $\Theta$ this way in practice: $\hat{\Theta}_{\text{naive}} = \hat{\Sigma}^{-1}$. This is due to problems with the naive inversion.

- **Not invertible when $p > n$**  
In finance and many real datasets, the number of variables is large relative to the number of observations, making $\hat{\Sigma}$ singular.

- **Even when invertible, the result is dense**  
The inverse of the sample covariance contains **almost no zeros**, producing:
    - a **dense graph**,  
    - no sparsity,  
    - no meaningful conditional independence structure.

This defeats the entire purpose of a graphical model.

---

### Graphical Lasso (GLasso)

To obtain a **sparse** and interpretable precision matrix, we solve a **regularized maximum-likelihood** problem:   

$$
\max_{\Theta \succeq 0} \; \log\det(\Theta)
- \mathrm{tr}(\hat{\Sigma}\Theta)
- \lambda \|\Theta\|_{1,\text{off}}.
$$

Where $\log\det(\Theta) - \mathrm{tr}(\hat{\Sigma}\Theta)$ is the Gaussian log-likelihood, and $\lVert\Theta\rVert_{1,\mathrm{off}} = \sum_{i \ne j} \lvert\Theta_{ij}\rvert$ encourages sparsity.

- $\lambda \ge 0$ is a hyperparameter controlling sparsity:

  - $\lambda = 0$ $\rightarrow$ dense graph  
  - $\lambda \uparrow$ $\rightarrow$ sparser graph (more zeros in $\Theta$)

Graphical Lasso produces a **sparse** precision matrix with meaningful conditional dependencies.

---

### Interpreting the Estimated Precision Matrix

The estimated precision matrix $\Theta$ encodes **conditional dependencies** between assets after controlling for all other stocks in the universe. An off-diagonal entry $\Theta_{ij}$ represents the partial correlation between asset $i$ and $j$:

- **Negative $\Theta_{ij}$** $\rightarrow$ the two assets tend to move in the **same direction**, *given all other assets are held fixed*.  
- **Positive $\Theta_{ij}$** $\rightarrow$ the assets tend to move in **opposite directions** (conditionally).  
- **Magnitude** reflects the **strength** of the conditional dependence.  
- Diagonal terms are always positive (inverse variances) and are not interpreted.

---

### Why Not Use Just Correlations?

Pairwise correlations can be misleading because they reflect both **direct** and **indirect** relationships.  

Two variables may appear correlated solely because they are each related to one or more *other* variables.  

A Gaussian graphical model separates these effects by examining **conditional** relationships: an edge between nodes $(i$ and $j$ is present only if their dependence remains after conditioning on all remaining variables.  

Thus, the precision matrix reveals the **direct dependency structure**, whereas correlation alone cannot distinguish direct from indirect associations.

