# Technical Methodology
## AI-Based Phishing Website Detection System

This document outlines the machine learning methodology, feature engineering formulations, statistical assumptions, and validation strategies implemented in the project.

---

## 1. Problem Formulation

Phishing website detection is formulated as a supervised binary classification task:
Given an input URL string $u$, an extraction function $\phi(u)$ maps the URL into an $8$-dimensional discrete feature vector:

$$\mathbf{x} = \phi(u) = [x_1, x_2, \dots, x_8]^T \in \{-1, 0, 1\}^8$$

The classifier $f: \mathbb{R}^8 \to \{0, 1\}$ assigns a predicted label $\hat{y}$:
- $\hat{y} = 1$: **Phishing** (Positive threat class)
- $\hat{y} = 0$: **Legitimate** (Negative safe class)

---

## 2. Feature Engineering Rules (8 Deterministic Features)

| Feature Name | Formulation & Heuristic | Output Values |
|---|---|---|
| `having_IP_Address` | Checks if hostname matches IPv4 dotted decimal, hexadecimal, or IPv6 patterns. | $-1$: IP detected (Phishing)<br>$+1$: Domain name (Legitimate) |
| `URL_Length` | Length $L = \text{len}(u)$ of the complete URL string. | $+1$: $L < 54$ (Legitimate)<br>$0$: $54 \le L \le 75$ (Suspicious)<br>$-1$: $L > 75$ (Phishing) |
| `Shortining_Service` | Domain matches known URL shorteners (`bit.ly`, `tinyurl.com`, `t.co`, etc.). | $-1$: Shortener used (Phishing)<br>$+1$: Standard domain (Legitimate) |
| `having_At_Symbol` | Presence of `@` symbol in URL string (RFC 3986 credentials trick). | $-1$: `@` present (Phishing)<br>$+1$: No `@` (Legitimate) |
| `double_slash_redirecting` | Last index of `//` in URL string: $\text{lastIndexOf}(\text{"//"}) > 7$. | $-1$: Redirect trick (Phishing)<br>$+1$: Protocol prefix only (Legitimate) |
| `Prefix_Suffix` | Domain label contains a hyphen `-` (brand spoofing). | $-1$: Hyphen present (Phishing)<br>$+1$: Clean domain (Legitimate) |
| `having_Sub_Domain` | Number of dots $d$ after removing `www.` and ccTLD (`.co.uk`, `.edu.in`). | $+1$: $d \le 1$ (Legitimate)<br>$0$: $d = 2$ (Suspicious)<br>$-1$: $d > 2$ (Phishing) |
| `HTTPS_token` | Domain label contains `http` or `https` substring (e.g., `https-paypal.com`). | $-1$: Token in domain (Phishing)<br>$+1$: Clean domain (Legitimate) |

---

## 3. Data Preprocessing & Validation

1. **Target Mapping**:
   The raw UCI dataset encoded `Result` as $\{-1, 1\}$. We mapped $\text{Phishing } (-1) \to 1$ and $\text{Legitimate } (+1) \to 0$.
2. **Stratified Splitting**:
   An $80/20$ train-test split was executed with stratification on target $y$:
   - Training Set: $8,844$ samples ($4,926$ legitimate, $3,918$ phishing)
   - Test Set: $2,211$ samples ($1,231$ legitimate, $980$ phishing)
3. **Data Leakage Prevention**:
   Hyperparameter grid searches and transformations were computed strictly within training folds using 5-fold cross-validation.

---

## 4. Algorithms & Mathematical Foundations

### 4.1 Decision Tree Classifier (Deployed)
Recursively partitions feature space to minimize node impurity.
- **Information Gain (Entropy)**:
  $$H(S) = -\sum_{i \in \{0, 1\}} p_i \log_2(p_i)$$
  $$\text{Gain}(S, A) = H(S) - \sum_{v \in \text{Values}(A)} \frac{|S_v|}{|S|} H(S_v)$$
- Optimal Hyperparameters: `criterion='entropy'`, `max_depth=6`, `min_samples_split=2`, `min_samples_leaf=1`.

### 4.2 Categorical Naive Bayes
Calculates exact categorical likelihoods with Laplace smoothing ($\alpha = 1$):
$$P(x_i = c | y) = \frac{N_{y, i, c} + \alpha}{N_y + \alpha C_i}$$
Features were shifted by $+1$ mapping $\{-1, 0, 1\} \to \{0, 1, 2\}$.

### 4.3 Gaussian Naive Bayes (Benchmark)
Assumes normal distribution:
$$P(x_i | y) = \frac{1}{\sqrt{2\pi\sigma_y^2}} \exp\left(-\frac{(x_i - \mu_y)^2}{2\sigma_y^2}\right)$$
Demonstrates empirical failure on discrete ternary data ($58.57\%$ accuracy).

### 4.4 Random Forest Classifier
Ensemble of 100 decorrelated decision trees using bagging:
$$\hat{P}(Y=1|\mathbf{x}) = \frac{1}{B} \sum_{b=1}^{B} T_b(\mathbf{x})$$
Optimal Hyperparameters: `n_estimators=100`, `max_depth=8`, `min_samples_split=5`.

### 4.5 Logistic Regression (Baseline)
Linear decision boundary through sigmoid activation:
$$\sigma(z) = \frac{1}{1 + e^{-z}}, \quad z = \mathbf{w}^T \mathbf{x} + b$$

---

## 5. Model Evaluation Metrics

In cybersecurity threat classification, **False Negatives (missed phishing attacks)** represent a critical safety hazard. Therefore, models are evaluated across multiple metrics:

$$\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}$$
$$\text{Precision} = \frac{TP}{TP + FP}$$
$$\text{Recall (Phishing)} = \frac{TP}{TP + FN}$$
$$\text{F1-Score} = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$
$$\text{ROC-AUC} = \int_{0}^{1} \text{TPR}(\text{FPR}^{-1}(t)) \, dt$$

The **Decision Tree** was selected for production because it achieved $76.63\%$ Phishing Recall, an F1-score of $71.66\%$, ROC-AUC of $0.8120$, and sub-millisecond on-device execution.
