# VAR(1) Model

We fit a Vector Autoregressive model of order $p$ to the daily log-returns of the 15-stock universe. A VAR($p$) models the system as $X_t = A_1 X_{t-1} + \ldots + A_p X_{t-p} + e_t$, where $e_t$ is an innovation term. The only hyperparameter is the lag order $p$, which we selected by evaluating AIC and BIC over $p \in \{1,\dots,50\}$.

![AIC_BIC](media/AIC_BIC_plot.png)

Both AIC and BIC were minimized at $p = 1$, so we fit a VAR(1). The estimated model is $X_t = A X_{t-1} + e_t$, where $A$ is a $15 \times 15$ coefficient matrix. Each entry $A_{jk}$ measures the contribution of stock $k$ (yesterday) to stock $j$ (today).

We visualize the VAR(1) coefficient matrix and construct directed Granger adjacency graphs by thresholding $|A|$ at several levels. At moderate thresholds (for example $|A| > 0.05$), we observe clear sectoral structure: large technology names exhibit multiple cross-lag edges, while energy and financial stocks show smaller but interpretable predictive effects. At higher thresholds the graph becomes sparse, showing that strong linear predictability across daily returns is limited.

![VAR_and_adj](media/VAR_and_adj_grid.png)

To assess model fit, we compute the per-stock statistic $R^2 = 1 - \text{Var}(e_j) / \text{Var}(X_j)$, which ranges from approximately $0.5\%$ to $3.5\%$. This is expected for daily equity returns, which are dominated by unpredictable shocks.

![R2](media/VAR_r2_barplot.png)
