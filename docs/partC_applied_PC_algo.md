# Applied PC Algorithm

### Selecting the PC Algorithm Significance Level ($\alpha^*$)

To tune the Type I error rate α in the PC algorithm, we examined CPDAGs across a grid of values $\alpha \in {0.001, 0.005, 0.01, 0.05}$. 

![pc_algorithm_on_alpha_grid.png](media/pc_algorithm_on_alpha_grid.png)

Using domain knowledge in equities markets, I propose selecting $\alpha^*$ based on **interpretability and agreement with known financial sector structure**.

Among the grid, **$\alpha = 0.001$** provides the most coherent and stable graphical structure:

- **Preserves clear sector clusters**, consistent with economic intuition:  
  - Mega-cap tech: AAPL–MSFT–GOOGL–META–AMZN–NVDA  
  - Banking: JPM–BAC  
  - Energy: XOM–CVX  
  - Consumer staples / healthcare: PG–KO–WMT–JNJ–PFE  

- **Retains informative weaker edges** within the tech and consumer groups that disappear at higher α, helping maintain rich and realistic cluster formation rather than fragmenting nodes into isolated components.

- **Avoids extremes**, i.e., $\alpha \geq 0.05$ is too sparse and drops economically meaningful links finding just sector based relationships.

Thus, $\alpha^* = 0.001$ achieves a desirable balance between sparsity and interpretability, producing a graph that aligns closely with established market structure. We therefore adopt $\alpha^* = 0.001$ for our final PC model and use this value in the subsequent stability (bootstrap) analysis.

### Stability Analysis

To assess robustness of the PC graph at $\alpha^* = 0.001$, I performed $B = 50$ bootstrap resamples of the returns data. For each bootstrap sample, I refit the PC algorithm, extracted the *undirected skeleton* of the CPDAG, and recorded whether an edge between each pair of stocks was present. This yields an edge-selection frequency $\hat{\pi}_{ij} = \frac{\text{number of bootstraps where edge } i\text{--}j \text{ appears}}{B}$.

![pc_stability.png](media/pc_stability.png)

The left panel plots the selection-frequency heatmap $\hat{\pi}\_{ij}$. The subsequent panels show thresholded adjacency matrices for different stability cutoffs (e.g., $\hat{\pi}\_{ij} \ge 0.5, 0.75, 0.9, 0.95, 0.995$). Edges within the tech cluster (AAPL, MSFT, GOOGL, META, AMZN, NVDA), the bank pair (JPM–BAC), the energy pair (XOM–CVX), and the staples/healthcare cluster (PG, KO, WMT, JNJ, PFE) remain present at high thresholds, indicating that these sector-level dependencies are highly stable to resampling, whereas weaker cross-sector links disappear as the stability cutoff increases.
