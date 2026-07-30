# rec24 — Recitation 24 (December 7, 2010)

Covers: Maximum likelihood estimation for a discrete (geometric-type) parametric PMF, partition/normalization function, mean and variance of a shifted geometric, ML estimator as sample mean, CLT-based sample-size choice from a noise-to-signal ratio, 95% confidence intervals, linear regression / least squares as ML with Gaussian noise (first-order and second-order models).

Sources: MIT6_041F10_rec24.pdf (questions/dfd6e16cfb0e3012c829030d51e86ee0_MIT6_041F10_rec24.pdf.md), MIT6_041F10_rec24_sol.pdf (solutions/a7bedaafad0b240c4ade88e559b831b1_MIT6_041F10_rec24_sol.pdf.md)

Header block on every page: Massachusetts Institute of Technology, Department of Electrical Engineering & Computer Science, 6.041/6.431: Probabilistic Systems Analysis (Fall 2010).

---

## Problem 1 — Blackbody photon counting: ML estimation of temperature $\theta$

### Statement

A blackbody at temperature $\theta$ radiates photons of all wavelengths, described by its characteristic spectrum. This problem will have you estimate $\theta$, which is fixed but unknown. The PMF for the number of photons $K$ in a given wavelength range and a fixed very short time interval is given by,

$$p_K(k;\theta) = \frac{1}{Z(\theta)} e^{-k/\theta}, \qquad k = 0, 1, 2, \ldots$$

$Z(\theta)$ is a normalization factor for the probability distribution (the physicists call it the partition function). You are given the task of determining the temperature of the body to two significant digits by photon counting in non-overlapping time intervals of duration one second. The photon emissions in non-overlapping time intervals are statistically independent from each other.

**(a)** Determine the normalization factor $Z(\theta)$.

**(b)** Compute the expected value of the photon number measured in any 1 second time interval, $\mu_K = \mathbf{E}_\theta[K]$, and its variance, $\operatorname{var}_\theta(K) = \sigma_K^2$.

**(c)** You count the number $k_i$ of photons detected in $n$ non-overlapping 1 second time intervals. Find the maximum likelihood estimator, $\hat\theta_n$, for temperature $\theta$. Note, it might be useful to introduce the average photon number $s_n = \frac{1}{n}\sum_{i=1}^{n} k_i$. In order to keep the analysis simple we assume that the body is hot, i.e. $\theta \gg 1$.

You may use the approximation: $\dfrac{1}{e^{1/\theta}-1} \approx \theta$ for $\theta \gg 1$.

In the following questions we wish to estimate the mean of the photon count in a one second time interval using the estimator $\hat K$, which is given by,

$$\hat K = \frac{1}{n}\sum_{i=1}^{n} K_i.$$

**(d)** Find the number of samples $n$ for which the noise to signal ratio for $\hat K$, (i.e., $\dfrac{\sigma_{\hat K}}{\mu_{\hat K}}$), is $0.01$.

**(e)** Find a 95% confidence interval for the mean photon count estimate for the situation in part (d). (You may use the central limit theorem.)

### Official solution

**(a)** Normalization of the distribution requires:

$$1 = \sum_{k=0}^{\infty} p_K(k;\theta) = \sum_{k=0}^{\infty} \frac{e^{-k/\theta}}{Z(\theta)} = \frac{1}{Z(\theta)}\sum_{k=0}^{\infty} e^{-k/\theta} = \frac{1}{Z(\theta)\cdot\left(1 - e^{-1/\theta}\right)},$$

so $Z(\theta) = \dfrac{1}{1 - e^{-1/\theta}}$.

[SOLUTION GAP: the geometric-series evaluation $\sum_{k=0}^\infty e^{-k/\theta} = 1/(1-e^{-1/\theta})$ is used without comment (convergence for $\theta>0$ not discussed).]

**(b)** Rewriting $p_K(k;\theta)$ as:

$$p_K(k;\theta) = \left(e^{-1/\theta}\right)^{k}\left(1 - e^{-1/\theta}\right), \qquad k = 0, 1, \ldots$$

the probability distribution for the photon number is a geometric probability distribution with probability of success $p = 1 - e^{-1/\theta}$, and it is shifted with 1 to the left since it starts with $k = 0$. Therefore the photon number expectation value is

$$\mu_K = \frac{1}{p} - 1 = \frac{1}{1 - e^{-1/\theta}} - 1 = \frac{1}{e^{1/\theta} - 1}$$

and its variance is

$$\sigma_K^2 = \frac{1-p}{p^2} = \frac{e^{-1/\theta}}{\left(1 - e^{-1/\theta}\right)^2} = \mu_K^2 + \mu_K.$$

[SOLUTION GAP: the algebra showing $\frac{1}{1-e^{-1/\theta}} - 1 = \frac{1}{e^{1/\theta}-1}$, and the identity $\frac{e^{-1/\theta}}{(1-e^{-1/\theta})^2} = \mu_K^2 + \mu_K$, are stated without intermediate steps. Also, the standard geometric mean/variance formulas ($1/p$ and $(1-p)/p^2$) are quoted rather than derived.]

**(c)** The joint probability distribution for the $k_i$ is

$$p_K(k_1, \ldots, k_n; \theta) = \frac{1}{Z(\theta)^n}\Pi_{i=1}^{n} e^{-k_i/\theta} = \frac{1}{Z(\theta)^n} e^{-\frac{1}{\theta}\sum_{i=1}^{n} k_i}.$$

The log likelihood is $-n\cdot\log Z(\theta) - 1/\theta\sum_{i=1}^{n} k_i$.

We find the maxima of the log likelihood by setting the derivative with respect to the parameter $\theta$ to zero:

$$\frac{d}{d\theta}\log p_K(k_1, \ldots, k_n; \theta) = -n\cdot\frac{e^{-1/\theta}}{\theta^2\left(1 - e^{-1/\theta}\right)} + \frac{1}{\theta^2}\sum_{i=1}^{n} k_i = 0$$

or

$$\frac{1}{e^{1/\theta} - 1} = \frac{1}{n}\sum_{i=1}^{n} k_i = s_n.$$

For a hot body, $\theta \gg 1$ and $\dfrac{1}{e^{1/\theta}-1} \approx \theta$, we obtain

$$\theta \approx \frac{1}{n}\sum_{i=1}^{n} k_i = s_n.$$

Thus the maximum likelihood estimator $\hat\Theta_n$ for the temperature is given in this limit by the sample mean of the photon number

$$\hat\Theta_n = \frac{1}{n}\sum_{i=1}^{n} K_i.$$

[SOLUTION GAP: the differentiation of $-n\log Z(\theta) = n\log(1-e^{-1/\theta})$ is carried out without showing the chain rule; and the step from the stationarity equation to $\frac{1}{e^{1/\theta}-1} = s_n$ (dividing by $n/\theta^2$ and simplifying $\frac{e^{-1/\theta}}{1-e^{-1/\theta}} = \frac{1}{e^{1/\theta}-1}$) is not shown. No second-order check that this stationary point is a maximum is given.]

**(d)** According to the central limit theorem, the sample mean for large enough $n$ (in the limit) approaches a Gaussian distribution with standard deviation our root mean square error

$$\sigma_{\hat\Theta_n} = \frac{\sigma_K}{\sqrt{n}}.$$

To allow only for 1% relative root mean square error in the temperature, we need $\dfrac{\sigma_K}{\sqrt{n}} < 0.01\mu_K$. With $\sigma_K^2 = \mu_K^2 + \mu_K$ it follows that

$$\sqrt{n} > \frac{\sigma_K}{0.01\mu_K} = 100\frac{\sqrt{\mu_K^2 + \mu_K}}{\mu_K} = 100\sqrt{1 + \frac{1}{\mu_K}}.$$

In general, for large temperatures, i.e. large mean photon numbers $\mu_K \gg 1$, we need about 10,000 samples.

[SOLUTION GAP: the final numerical step is compressed — for $\mu_K \gg 1$ the factor $\sqrt{1 + 1/\mu_K} \to 1$, so $\sqrt{n} > 100$ and hence $n > 10^4 = 10{,}000$; this arithmetic is not written out. Also the CLT is invoked for the *distribution* of the sample mean, but the identity $\sigma_{\hat K} = \sigma_K/\sqrt{n}$ (which is exact by independence, not a CLT consequence) is not separated from it. Note the problem asks for equality (ratio $=0.01$) whereas the solution works with the inequality $<0.01$.]

[SOURCE TYPO?: parts (d) and (e) of the solution are written in terms of the *temperature* estimator $\hat\Theta_n$ and $\sigma_{\hat\Theta_n}$, whereas the problem statement poses (d)/(e) for the *photon-count* estimator $\hat K$ and $\sigma_{\hat K}/\mu_{\hat K}$. In the hot-body limit of part (c) the two coincide, $\hat\Theta_n = \hat K = \frac{1}{n}\sum_{i=1}^n K_i$, which is why the solution switches back to $\hat K$ inside the confidence interval of part (e).]

**(e)** The 95% confidence interval for the temperature estimate for the situation in part (d), i.e.

$$\sigma_{\hat\Theta_n} = \frac{\sigma_K}{\sqrt{n}} = 0.01\mu_K,$$

is

$$[\hat K - 1.96\sigma_{\hat K},\ \hat K + 1.96\sigma_{\hat K}] = [\hat K - 0.0196\mu_K,\ \hat K + 0.0196\mu_K].$$

[SOLUTION GAP: the value 1.96 as the 97.5th percentile of the standard normal is used without justification, and $\sigma_{\hat K} = 0.01\mu_K$ is substituted directly.]

---

## Problem 2 — Linear vs. quadratic regression on five data pairs (ML estimation)

### Statement

Given the five data pairs $(x_i, y_i)$ in the table below,

| x | 0.8 | 2.5 | 5 | 7.3 | 9.1 |
|---|-----|-----|---|-----|-----|
| y | -2.3 | 20.9 | 103.5 | 215.8 | 334 |

we want to construct a model relating $x$ and $y$. We consider a linear model

$$Y_i = \theta_0 + \theta_1 x_i + W_i, \qquad i = 1, \ldots, 5,$$

and a quadratic model

$$Y_i = \beta_0 + \beta_1 x_i^2 + V_i, \qquad i = 1, \ldots, 5.$$

where $W_i$ and $V_i$ represent additive noise terms, modeled by independent normal random variables with mean zero and variance $\sigma_1^2$ and $\sigma_2^2$, respectively.

**(a)** Find the ML estimates of the linear model parameters.

**(b)** Find the ML estimates of the quadratic model parameters.

Note: You may use the regression formulas and the connection with ML described in pages 478-479 of the text. However, the regression material is outside the scope of the final.

The figure below shows the data points $(x_i, y_i)$, $i = 1, \ldots, 5$, the estimated linear model

$$y = 40.53x - 65.86,$$

and the estimated quadratic model

$$y = 4.09x^2 - 3.07.$$

Figure 1: Regression Plot

[FIGURE: Scatter-plus-curves regression plot. Horizontal axis labelled "X" with ticks at 0, 2, 4, 6, 8, 10, 12; vertical axis labelled "Y" with ticks at -100, 0, 100, 200, 300, 400, 500; light blue dashed grid. Five green open-circle "Sample data points" at approximately (0.8, -2.3), (2.5, 20.9), (5, 103.5), (7.3, 215.8), (9.1, 334). A red dashed straight line — the "Estimated first-order model" $y = 40.53x - 65.86$ — rising from about (0.4, -55) to about (11, 375), crossing zero near $x\approx1.6$. A solid purple upward-curving parabola — the "Estimated second-order model" $y = 4.09x^2 - 3.07$ — starting near (0.4, -2) and rising to about (11, 485); it lies *above* the dashed line for $x \lesssim 2$, crosses below it near $x\approx 2$, stays below through mid-range $x$, and crosses back above near $x\approx 8$, passing very close to all five data points. Both curves are drawn slightly beyond the plotted data range (from $x\approx0.4$ to $x\approx11$). Three text callouts with grey right-angled leader lines each ending in a small grey dot: "Sample data points" (label text at upper centre near $y\approx400$, dot at about (6.5, 383), leader running down then right to the circle at (9.1, 334)); "Estimated first-order model" (label near $y\approx280$ at left-of-centre, dot at about (3.4, 233), leader running down then right to the dashed red line at about (5.2, 150)); "Estimated second-order model" (label text at lower centre near $y\approx 60$, dot at about (7.35, 60), leader running up then left to the purple curve at about (6.1, 150)). Plot enclosed in a black rectangular frame; axis box drawn in dark blue. Credit line at bottom right, outside the frame: "Image by MIT OpenCourseWare." | raster/rec24_p02.png]

### Official solution

**(a)** Using the regression formulas of Section 9.2, we have

$$\hat\theta_1 = \frac{\sum_{i=1}^{5}(x_i - \bar x)(y_i - \bar y)}{\sum_{i=1}^{5}(x_i - \bar x)^2}, \qquad \hat\theta_0 = \bar y - \hat\theta_1 \bar x,$$

where

$$\bar x = \frac{1}{5}\sum_{i=1}^{5} x_i = 4.94, \qquad \bar y = \frac{1}{5}\sum_{i=1}^{5} y_i = 134.38.$$

The resulting ML estimates are

$$\hat\theta_1 = 40.53, \qquad \hat\theta_0 = -65.86.$$

[SOLUTION GAP: the numerical evaluation of $\sum (x_i-\bar x)(y_i-\bar y)$ and $\sum (x_i-\bar x)^2$ is not shown — only the final numbers are given. Also, the equivalence of ML estimation under i.i.d. zero-mean Gaussian noise with least-squares regression is cited (text pp. 478-479 / Section 9.2) rather than derived.]

**(b)** Using the same procedure as in part (a), we obtain

$$\hat\theta_1 = \frac{\sum_{i=1}^{5}(x_i^2 - \bar x)(y_i - \bar y)}{\sum_{i=1}^{5}(x_i^2 - \bar x)^2}, \qquad \hat\theta_0 = \bar y - \hat\theta_1\bar x,$$

where

$$\bar x = \frac{1}{5}\sum_{i=1}^{5} x_i^2 = 33.60, \qquad \bar y = \frac{1}{5}\sum_{i=1}^{5} y_i = 134.38.$$

which for the given data yields

$$\hat\theta_1 = 4.09, \qquad \hat\theta_0 = -3.07.$$

[SOURCE TYPO?: in part (b) the solution keeps the symbols $\hat\theta_1,\hat\theta_0$ although the problem statement names the quadratic-model parameters $\beta_0,\beta_1$; so $\hat\theta_1$ here means $\hat\beta_1$ and $\hat\theta_0$ means $\hat\beta_0$.]

[SOURCE TYPO?: in part (b) the symbol $\bar x$ is reused for the mean of the *squares*, $\frac{1}{5}\sum x_i^2 = 33.60$ — i.e. it really denotes $\overline{x^2}$. The formula $\hat\theta_0 = \bar y - \hat\theta_1\bar x$ is consistent only if $\bar x$ is read as this $33.60$ value (indeed $134.38 - 4.09\times 33.60 \approx -3.04 \approx -3.07$).]

[SOLUTION GAP: again the numerator/denominator sums for the quadratic fit are not evaluated explicitly.]

Figure 1 shows the data points $(x_i, y_i)$, $i = 1, \ldots, 5$, the estimated linear model

$$y = 40.53x - 65.86,$$

and the estimated quadratic model

$$y = 4.09x^2 - 3.07.$$

[SOURCE TYPO?: on the solution sheet (page 3 of 3) the sentence ends at "and the estimated quadratic model" and the displayed equation $y = 4.09x^2 - 3.07$ is **not** printed — the figure float displaced it. The equation is supplied here from the identical passage on page 2 of the question sheet and from the part-(b) results $\hat\theta_1 = 4.09$, $\hat\theta_0 = -3.07$.]

[FIGURE: Same regression plot as in the question sheet — "Figure 1: Regression Plot". X axis 0 to 12 (ticks 0, 2, 4, 6, 8, 10, 12), Y axis -100 to 500 (ticks -100, 0, 100, 200, 300, 400, 500), dashed light-blue grid. Five green open circles for the sample data at $(0.8,-2.3)$, $(2.5,20.9)$, $(5,103.5)$, $(7.3,215.8)$, $(9.1,334)$; red dashed straight line for the estimated first-order model $y=40.53x-65.86$; solid purple parabola for the estimated second-order model $y=4.09x^2-3.07$, which fits the points closely, lies above the line for $x\lesssim2$, below it through mid-range $x$, and crosses back above near $x\approx8$. Labelled callouts with right-angled grey leader lines: "Sample data points" (to the circle at $(9.1,334)$), "Estimated first-order model" (to the red dashed line near $x\approx5$), "Estimated second-order model" (to the purple curve near $x\approx6$). Credit outside the frame at bottom right: "Image by MIT OpenCourseWare." | raster/rec24_sol_p03.png]

Footnote at the bottom-left of the last solution page (page 3 of 3), on the same rule as "Page 3 of 3": $^\dagger$Required for 6.431; optional for 6.041

[SOURCE TYPO?: the dagger footnote is printed on solution page 3, but no $^\dagger$ marker appears anywhere in the body text of either the question sheet or the solution sheet for rec24 — it is a leftover from the recitation template. No problem in this recitation is therefore explicitly flagged as 6.431-only.]

---

Both PDFs close with an MIT OpenCourseWare page: "MIT OpenCourseWare, http://ocw.mit.edu, 6.041 / 6.431 Probabilistic Systems Analysis and Applied Probability, Fall 2010. For information about citing these materials or our Terms of Use, visit: http://ocw.mit.edu/terms." (question PDF page 3, solution PDF page 4).
