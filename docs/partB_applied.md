# Part B — Applied Analysis (Graphical Lasso + Stability Selection)

### Initial Graphical Lasso Fit Across an $\alpha$-Grid

Before selecting any hyperparameter, we begin by fitting Graphical Lasso across a grid of penalty values $\alpha \in \{0.001, 0.01, 0.1, 0.5\}$ to visualize how regularization shapes the structure of the estimated precision matrix.

Smaller $\alpha$ values produce **dense graphs** with many conditional dependencies, while larger $\alpha$ values encourage **sparser**, more interpretable structure.  
Inspecting this grid helps us see:

- which edges disappear first as regularization increases,  
- which relationships remain persistent across a wide range of $\alpha$,  
- how the overall graph topology transitions from dense (low $\alpha$) to sparse (high $\alpha$).

This exploratory step provides intuition before applying cross-validation or stability selection.

![Precision + Adjacency Across Alpha](media/graphicalLASSO_precision_across_alpha.png)


### Cross-Validated Graphical Lasso

We begin by estimating the penalty parameter $\alpha^*$ using **Graphical Lasso with cross-validation**.  
Cross-validation maximizes the Gaussian log-likelihood on held-out data, which is **problematic for graph structure learning** because the Gaussian log-likelihood **always increases** as the model becomes denser. Therefore CV **prefers graphs with many edges** and tends to **under-penalize** (i.e., choose $\alpha$ that is too small), resulting in adjacency matrices that are **overly dense** and difficult to interpret.

This is illustrated in the CV fit below:

![Graphical Lasso CV](media/graphicalLASSO_CV.png)

Even though CV does not promote sparsity, the selected $\alpha^*$ still provides a useful **starting graph**, which we later refine using *stability selection*. With this CV-chosen $\alpha^*$, the corresponding precision matrix captures **direct conditional dependencies** between variables after controlling for all others.

### Bootstrap Stability Selection

Again, CV is known to **favor overly dense graphs** in Gaussian graphical models. To address this limitation, we complement the CV-chosen model with **stability selection**, which identifies only the *most persistent* structure in the data. The idea is to retain edges that appear consistently under random perturbations of the dataset, and treat unstable edges as noise.

Concretely, we perform **10,000 bootstrap resamples**, refit the Graphical Lasso on each resampled dataset, and record whether each edge is present. Aggregating these results yields a **selection frequency matrix**, where entry $(i,j)$ is the proportion of bootstrap fits in which the edge $i$–$j$ appears.

![Graphical Lasso Stability Tuning](media/graphicalLASSO_tuning.png)

Interpretation:

- The heatmap visualizes how often each edge is selected across all 10,000 runs.  
- Thresholding at levels `0.75, 0.90, 0.95, 0.99, 1.0` (plus `1.01` to show the cutoff) reveals progressively stricter definitions of *stability*.  
- Edges with frequency **1.0** are present in *every* bootstrap fit—representing the **most robust, data-supported conditional dependencies**.

Unlike marginal correlation, these stable edges correspond to **direct partial dependencies** that persist even after conditioning on all other variables. Stability selection therefore isolates the most reliable structural relationships in the graphical model.

---
