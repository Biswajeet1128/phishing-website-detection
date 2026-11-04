# Machine Learning Models Directory

This directory stores the trained model artifacts, serialized parameters, and training metadata for both experimental tracks.

---

## 🏛️ Two-Model Strategy Overview

| Property | Track A (Full Benchmark) | Track B (Deployed Real-Time) |
|---|---|---|
| **Purpose** | Academic benchmark on complete multi-domain dataset | Lightweight on-device inference inside Chrome Extension |
| **Input Features** | All 30 UCI features (Lexical, DOM, SSL, DNS, WHOIS) | 8 Address-Bar URL features only |
| **Deployed Model** | Random Forest (`models/model_a/random_forest.joblib`) | Decision Tree (`models/model_b/model.json`) |
| **Accuracy** | **97.60%** | **73.13%** |
| **Phishing Recall** | **96.53%** | **76.63%** |
| **ROC-AUC** | **0.9963** | **0.8120** |
| **Inference Latency** | 0.028 ms / sample | **0.0015 ms / sample** |
| **Execution Environment**| Python (Backend / Offline) | **Pure Browser JavaScript (Zero Latency)** |

---

## 📁 Directory Structure

```
models/
├── model_a/                             # Full 30-feature benchmark models
│   ├── decision_tree.joblib             # Scikit-learn Decision Tree (75 KB)
│   ├── gaussian_nb.joblib               # Gaussian Naive Bayes (2.4 KB)
│   ├── categorical_nb.joblib            # Categorical Naive Bayes (6.7 KB)
│   ├── random_forest.joblib             # Random Forest ensemble (15.5 MB)
│   ├── logistic_regression.joblib       # Logistic Regression (1.8 KB)
│   └── training_metadata.json           # Hyperparameters, CV scores & timestamps
│
├── model_b/                             # 8-feature URL real-time models
│   ├── decision_tree.joblib             # Scikit-learn Decision Tree (6.7 KB)
│   ├── gaussian_nb.joblib               # Gaussian Naive Bayes (1.4 KB)
│   ├── categorical_nb.joblib            # Categorical Naive Bayes (2.4 KB)
│   ├── random_forest.joblib             # Random Forest ensemble (1.57 MB)
│   ├── logistic_regression.joblib       # Logistic Regression (1.3 KB)
│   ├── model.json                       # Serialized Decision Tree for JS (31 KB) [DEPLOYED]
│   ├── random_forest.json               # Serialized Random Forest ensemble (2.85 MB)
│   └── training_metadata.json           # Hyperparameters, CV scores & timestamps
│
└── README.md                            # Model documentation & reproduction guide
```

---

## 🚀 The Deployed Model: Model B Decision Tree

The deployed model in the Chrome Extension is the **Model B Decision Tree**:
- **Why Decision Tree?**
  1. **Sub-millisecond Latency**: Evaluates a URL in under $0.002\text{ ms}$ on client devices.
  2. **Zero Dependencies**: Serialized into a pure JSON tree (`model.json`), requiring zero external Python/Node packages or C++ runtimes.
  3. **High Threat Recall**: Achieves $76.63\%$ recall on the Phishing class, prioritizing the minimization of False Negatives (missed attacks).
  4. **Interpretability**: Enables the extension to clearly explain *why* a URL was flagged (e.g., brand-spoofing hyphens, suspicious subdomains).

### Serialized JSON Node Schema
The exported `model.json` consists of a nested decision tree:
```json
{
  "node_id": 0,
  "is_leaf": false,
  "feature_index": 5,
  "feature_name": "Prefix_Suffix",
  "threshold": 0.0,
  "left": { ... },
  "right": { ... },
  "probabilities": [0.557, 0.443]
}
```

---

## 🔄 How to Retrain and Re-Export Models

To retrain all models from scratch with 5-fold cross-validation:
```bash
python src/train_models.py
```

To re-evaluate metrics and generate visualizations:
```bash
python src/evaluate_models.py
```

To export the trained Scikit-learn models into `model.json` and `extension/model_data.js`:
```bash
python src/model_export.py
```

---

## 💾 Version Control Note

Large binary `.joblib` files (such as `model_a/random_forest.joblib`, 15.5 MB) are excluded from Git commits via `.gitignore` to maintain a lightweight repository. Running `python src/train_models.py` regenerates all binary `.joblib` artifacts deterministically in under 30 seconds.
