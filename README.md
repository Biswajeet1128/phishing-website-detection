# AI-Based Phishing Website Detection System with Chrome Browser Extension

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3%2B-F7931E?logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6%2B-F7DF1E?logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Chrome Extension](https://img.shields.io/badge/Chrome%20Extension-Manifest%20V3-4285F4?logo=googlechrome&logoColor=white)](https://developer.chrome.com/docs/extensions/mv3/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Unit & Parity Tests](https://img.shields.io/badge/Tests-17%20Passed%20(100%25)-brightgreen.svg)]()
[![Inference](https://img.shields.io/badge/Inference-0ms%20Local%20Client-blueviolet.svg)]()

<p align="center">
  <strong>A real-time Machine Learning security system that inspects website URL characteristics to detect phishing attacks directly inside the browser using client-side JavaScript inference.</strong>
</p>

</div>

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Two-Model Strategy](#-two-model-strategy)
- [Dataset Details](#-dataset-details)
- [Machine Learning Algorithms](#-machine-learning-algorithms)
- [Model Performance & Comparison](#-model-performance--comparison)
- [Visualizations & Screenshots](#-visualizations--screenshots)
- [Installation & Setup](#-installation--setup)
- [How to Load the Chrome Extension](#-how-to-load-the-chrome-extension)
- [CLI Inference](#-cli-inference)
- [Repository Structure](#-repository-structure)
- [Testing & Quality Assurance](#-testing--quality-assurance)
- [Limitations](#-limitations)
- [Future Scope](#-future-scope)
- [Author & License](#-author--license)

---

## 🎯 Overview

Phishing attacks remain the leading threat vector for credential harvesting, financial fraud, and identity theft. Traditional defense relies on static blacklists (such as Google Safe Browsing or PhishTank). However, modern attack campaigns utilize algorithmically generated, short-lived domains that remain active for only **4 to 8 hours**—bypassing static blacklists before human analysts can flag them.

**PhishShield AI** addresses this zero-day window by analyzing URL lexical and structural patterns directly on the client side:
1. **Pre-Render Protection**: Evaluates URLs before the browser renders the remote webpage, protecting users from drive-by downloads or malicious scripts.
2. **Zero-Latency Inference**: Serializes trained Scikit-learn tree models into JSON for execution in pure browser JavaScript ($<0.002\text{ ms}$ latency).
3. **100% Privacy-Preserving**: Runs completely offline inside the browser extension. User browsing history is never transmitted to an external server or cloud API.

---

## ✨ Key Features

- **Machine Learning Classification**: Trained and benchmarked on 5 classification algorithms across 11,055 ground-truth records.
- **8 Deterministic Address-Bar Features**: Extracts lexical indicators matching the official UCI dataset specification without network calls.
- **Chrome Browser Extension (Manifest V3)**: Event-driven service worker and cybersecurity dashboard popup with real-time risk gauges.
- **Three Clear UI Security States**:
  - 🟢 **LEGITIMATE**: Low threat score, clean URL indicator chips, safe browsing guidance.
  - 🔴 **PHISHING**: Critical threat warning, highlighted risk indicators (spoofing hyphens, subdomains), instructions to avoid credential entry.
  - ⚙️ **INTERNAL / UNKNOWN**: Graceful handling of browser system pages (`chrome://`, `about:blank`, `file://`).
- **On-Demand Manual URL Scanner**: Test custom URLs in real-time from the extension popup.
- **Verified Python & JavaScript Parity**: Automated test suite guaranteeing that Python training feature extraction and JavaScript browser runtime produce identical vectors and predictions.

---

## 🏛️ System Architecture

### End-to-End Pipeline

```mermaid
flowchart TD
    subgraph Data Pipeline
        A["UCI Phishing Dataset (11,055 records)"] --> B["Data Preprocessing (src/preprocessing.py)"]
        B --> C["Stratified Train-Test Split (80% / 20%)"]
    end

    subgraph Two-Model Strategy
        C --> D["Track A: 30 Features (Full Benchmark)"]
        C --> E["Track B: 8 Address-Bar Features (Real-Time)"]
        D --> F["Benchmark Models: RF (97.6%), DT (97.0%), CNB (93.3%)"]
        E --> G["Deployable Models: DT (73.1%), RF (73.1%), CNB (72.9%)"]
    end

    subgraph Serialization & Deployment
        G --> H["Model Selection: Decision Tree (Recall: 76.63%, F1: 71.66%)"]
        H --> I["Model Serializer (src/model_export.py)"]
        I --> J["extension/model.json & model_data.js (31 KB)"]
    end

    subgraph Browser Extension Manifest V3
        K["User Navigates Tab"] --> L["Query Active Tab URL (popup.js)"]
        L --> M["JS Feature Extractor (feature_extractor.js)"]
        M --> N["8-Element Discrete Vector"]
        J --> O["Pure JS Inference Engine (model.js)"]
        N --> O
        O --> P["Cybersecurity Dashboard UI"]
    end
```

### Real-Time Detection Sequence in Chrome

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant Browser as Chrome Browser (Active Tab)
    participant Popup as Extension Popup (popup.js)
    participant Extractor as JS Feature Extractor (feature_extractor.js)
    participant Engine as Inference Engine (model.js)
    participant UI as Popup Dashboard (popup.html)

    User->>Browser: Navigates to target website
    User->>Popup: Clicks extension icon
    Popup->>Browser: Queries active tab URL
    Browser-->>Popup: Returns URL string

    alt URL is Internal Scheme (chrome://, about:, file://)
        Popup->>UI: Renders UNKNOWN / INTERNAL state (exempt from scan)
    else URL is Web Scheme (http://, https://)
        Popup->>Extractor: extractFeatures(url)
        Extractor-->>Popup: Returns 8-element feature vector & findings
        Popup->>Engine: predictVector(vector)
        Engine-->>Popup: Returns { label, risk_level, confidence, risk_score }
        Popup->>UI: Renders LEGITIMATE (Green) or PHISHING (Red) with guidance
    end
```

<div align="center">
  <img src="assets/architecture/pipeline_architecture.svg" alt="System Architecture Diagram" width="850">
</div>

---

## ⚖️ Two-Model Strategy

The original UCI dataset contains 30 features. However, not all features can be extracted from a URL string alone without querying remote DNS servers or scraping web page HTML. We implement two distinct experimental tracks:

| Dimension | Model A (Full Academic Benchmark) | Model B (Real-Time URL Detection) |
|---|---|---|
| **Features** | **30 Features** (Lexical, DOM elements, SSL certificate, DNS, WHOIS) | **8 Address-Bar Features** (Pure URL string only) |
| **Execution** | Offline / Server-side analysis | **Client-side inside Chrome Extension** |
| **External Dependencies** | Requires HTML DOM parsing, port scanning, WHOIS | **Zero external requests, zero server dependencies** |
| **Selected Algorithm** | Random Forest (`models/model_a/random_forest.joblib`) | **Decision Tree (`models/model_b/model.json`)** |
| **Accuracy** | **97.60%** | **73.13%** |
| **Phishing Recall** | **96.53%** | **76.63%** |
| **ROC-AUC** | **0.9963** | **0.8120** |
| **Inference Latency** | 0.028 ms / sample | **0.0015 ms / sample** |

---

## 🔍 The 8 URL Address-Bar Features

Model B extracts the following 8 deterministic features matching the exact encoding of the original UCI dataset specification:

| # | Feature Name | Description & Heuristic Rule | Encoding |
|---|---|---|---|
| 1 | `having_IP_Address` | Checks if hostname is an IPv4, hex IPv4, or IPv6 address. | `-1`: IP used (Phishing)<br>`+1`: Domain name (Legit) |
| 2 | `URL_Length` | Length $L$ of URL string ($L < 54 \to 1$, $54 \le L \le 75 \to 0$, $L > 75 \to -1$). | `+1`: Legit<br>`0`: Suspicious<br>`-1`: Phishing |
| 3 | `Shortining_Service` | Domain matches known URL shorteners (`bit.ly`, `tinyurl.com`, `t.co`, etc.). | `-1`: Shortener (Phishing)<br>`+1`: Standard (Legit) |
| 4 | `having_At_Symbol` | Checks for `@` symbol trick in URL (RFC 3986 userinfo credential masking). | `-1`: `@` present (Phishing)<br>`+1`: Clean (Legit) |
| 5 | `double_slash_redirecting` | Position of last `//` occurring after index 7 ($\text{lastIndexOf} > 7$). | `-1`: Redirect trick (Phishing)<br>`+1`: Protocol only (Legit) |
| 6 | `Prefix_Suffix` | Domain label contains a hyphen `-` (used for brand spoofing). | `-1`: Hyphen present (Phishing)<br>`+1`: Clean domain (Legit) |
| 7 | `having_Sub_Domain` | Number of dots $d$ after stripping `www.` and multi-part ccTLDs (`.co.uk`, `.edu.in`). | `+1`: $d \le 1$ (Legit)<br>`0`: $d = 2$ (Suspicious)<br>`-1`: $d > 2$ (Phishing) |
| 8 | `HTTPS_token` | Deceptive inclusion of `http` or `https` tokens inside domain label. | `-1`: Token in domain (Phishing)<br>`+1`: Clean domain (Legit) |

---

## 📂 Dataset Details

- **Dataset:** [UCI Phishing Websites Dataset (ID: 327)](https://archive.ics.uci.edu/dataset/327/phishing+websites)
- **Creators:** Rami M. Mohammad, Fadi Thabtah, and Lee McCluskey (University of Huddersfield, UK)
- **Total Records:** 11,055 instances
- **Missing Values:** 0 (dense, fully populated)
- **Original Class Distribution:**
  - `Legitimate (+1)`: 6,157 instances (55.69%)
  - `Phishing (-1)`: 4,898 instances (44.31%)
- **Binary Target Mapping**: `Phishing (-1) -> 1` (Positive threat), `Legitimate (+1) -> 0` (Negative safe).

To download the dataset automatically:
```bash
python dataset/download_dataset.py
```

---

## 🤖 Machine Learning Algorithms

Five classification algorithms were trained and cross-validated:

1. **Decision Tree Classifier (Deployed)**:
   Recursive binary partitioning using Information Gain (Entropy). Tuned with `criterion='entropy'`, `max_depth=6`, `min_samples_split=2`. Selected for deployment due to high phishing recall (76.63%), sub-millisecond execution, and transparent interpretability.
2. **Random Forest Classifier**:
   Ensemble of 100 decorrelated decision trees using bagging and feature subsampling. Achieved 97.60% accuracy on Model A and 73.13% on Model B.
3. **Categorical Naive Bayes**:
   Computes exact category frequency tables with Laplace smoothing. Shifted discrete features $\{-1, 0, 1\} \to \{0, 1, 2\}$. Attained 93.31% accuracy on Model A and 72.91% on Model B.
4. **Gaussian Naive Bayes**:
   Baseline probabilistic classifier assuming normal feature distributions. Illustrates the failure of Gaussian assumptions on discrete multi-class data (58.57% accuracy on Model B).
5. **Logistic Regression**:
   Linear classification baseline applying the standard sigmoid activation function.

---

## 📈 Model Performance & Comparison

Evaluated on 2,211 held-out test samples (stratified 20% test split):

### Comprehensive Results Table

| Track | Algorithm | Accuracy | Precision | Recall (Phishing) | F1-Score | ROC-AUC | False Negatives (FN) | Train Time | Pred Latency |
|---|---|---|---|---|---|---|---|---|---|
| **Model A (30 Features)** | **Random Forest** | **97.60%** | **98.03%** | **96.53%** | **97.28%** | **0.9963** | **34** | 20.02s | 0.0284 ms |
| **Model A (30 Features)** | Decision Tree | 97.01% | 97.31% | 95.92% | 96.61% | 0.9778 | 40 | 6.91s | 0.0012 ms |
| **Model A (30 Features)** | Categorical NB | 93.31% | 93.79% | 90.92% | 92.33% | 0.9814 | 89 | 0.02s | 0.0008 ms |
| **Model A (30 Features)** | Logistic Regression | 92.76% | 93.43% | 90.00% | 91.68% | 0.9784 | 98 | 0.06s | 0.0006 ms |
| **Model A (30 Features)** | Gaussian NB | 61.60% | 53.59% | 99.90% | 69.75% | 0.9677 | 1 | 0.01s | 0.0016 ms |
| **Model B (8 URL Features)** | **Decision Tree (Deployed)** | **73.13%** | **67.29%** | **76.63%** | **71.66%** | **0.8120** | **229** | **1.85s** | **0.0015 ms** |
| **Model B (8 URL Features)** | Random Forest | 73.13% | 67.51% | 75.92% | 71.47% | 0.8260 | 236 | 12.55s | 0.0113 ms |
| **Model B (8 URL Features)** | Categorical NB | 72.91% | 66.19% | 79.49% | 72.23% | 0.7972 | 201 | 0.003s | 0.0003 ms |
| **Model B (8 URL Features)** | Logistic Regression | 71.01% | 68.21% | 64.80% | 66.46% | 0.7830 | 345 | 0.02s | 0.0007 ms |
| **Model B (8 URL Features)** | Gaussian NB | 58.57% | 51.69% | 100.0% | 68.15% | 0.7616 | 0 | 0.002s | 0.0012 ms |

> **Selection Rationale:** In cybersecurity, **False Negatives (missed threats)** are substantially more dangerous than False Positives (user warnings). The Model B Decision Tree was chosen for deployment because it minimizes missed attacks ($76.63\%$ phishing recall), operates in $0.0015\text{ ms}$, serializes into a compact $31\text{ KB}$ JSON file, and provides interpretable feature-by-feature explanations.

---

## 🖼️ Visualizations & Screenshots

### Chrome Extension Interface States
<div align="center">
  <img src="assets/screenshots/extension_preview.svg" alt="Chrome Extension UI States" width="850">
</div>

---

### Model Performance & ROC Curves
<div align="center">
  <table>
    <tr>
      <td width="50%"><img src="assets/plots/model_performance_comparison.png" alt="Model Performance Comparison"></td>
      <td width="50%"><img src="assets/plots/roc_curves_comparison.png" alt="ROC Curves Comparison"></td>
    </tr>
    <tr>
      <td align="center"><b>Algorithm Metric Comparison (Model A vs Model B)</b></td>
      <td align="center"><b>Receiver Operating Characteristic (ROC) Curves</b></td>
    </tr>
  </table>
</div>

---

### Confusion Matrices & Feature Importances
<div align="center">
  <table>
    <tr>
      <td width="50%"><img src="assets/plots/confusion_matrices_track_b.png" alt="Confusion Matrices Track B"></td>
      <td width="50%"><img src="assets/plots/feature_importance_rf_model_b.png" alt="Feature Importance Track B"></td>
    </tr>
    <tr>
      <td align="center"><b>Confusion Matrices (Track B URL Models)</b></td>
      <td align="center"><b>Model B Gini Feature Importances</b></td>
    </tr>
  </table>
</div>

---

## 💻 Installation & Setup

### Prerequisites
- Python 3.10, 3.11, 3.12, or 3.13
- Node.js (v18+, optional for parity test suite execution)
- Google Chrome, Brave, or any Chromium-based browser

### 1. Clone the Repository
```bash
git clone https://github.com/Biswajeet1128/phishing-website-detection.git
cd phishing-website-detection
```

### 2. Set Up Python Virtual Environment
```bash
# On Linux / macOS:
python3 -m venv venv
source venv/bin/activate

# On Windows:
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. (Optional) Re-download Dataset or Retrain Models
```bash
# Download dataset if not present
python dataset/download_dataset.py

# Retrain all models with 5-fold cross-validation
python src/train_models.py

# Re-run evaluation and update plots
python src/evaluate_models.py

# Export model for browser extension
python src/model_export.py
```

### 5. Launch the Jupyter Notebook
```bash
jupyter notebook notebooks/phishing_analysis.ipynb
```

---

## 🌐 How to Load the Chrome Extension

The extension works on **Google Chrome**, **Brave**, **Microsoft Edge**, and other Chromium browsers:

1. Open **Google Chrome** (or **Brave**).
2. In the URL address bar, enter:
   ```text
   chrome://extensions
   ```
   *(For Brave: `brave://extensions`)*
3. In the top-right corner, switch the **Developer mode** toggle to **ON**.
4. In the top-left toolbar, click the **Load unpacked** button.
5. In the file picker, select the `extension/` directory inside this repository:
   ```text
   /path/to/phishing-website-detection/extension
   ```
6. Click **Select Folder**.
7. The **PhishShield AI** extension is now installed!
8. Click the puzzle icon in Chrome's toolbar and **pin** PhishShield AI for easy access.

---

## 🖥️ CLI Inference

Predict the security status of any URL directly from your command line:

```bash
# Predict a legitimate URL
python src/predict.py --url "https://www.google.com"

# Predict a suspicious URL
python src/predict.py --url "http://secure-paypal-login.update-billing.account-security.com//verify"

# Output structured JSON
python src/predict.py --url "https://bit.ly/3xY8a" --json
```

**Example Terminal Output:**
```text
============================================================
 PHISHING DETECTION SECURITY ASSESSMENT
============================================================
 Analyzed URL: http://secure-paypal-login.update-billing.account-security.com//verify
 Result:       [!] PHISHING DETECTED
 Risk Level:   HIGH (97.3% Risk Score)
 Confidence:   97.3%
------------------------------------------------------------
 Extracted Feature Findings:
    [OK]    having_IP_Address          : Domain name used
    [WARN]  URL_Length                 : Moderate length URL (54-75 chars)
    [OK]    Shortining_Service         : Direct domain (no shortening)
    [OK]    having_At_Symbol           : No '@' symbol
    [ALERT] double_slash_redirecting   : Suspicious '//' redirect in path
    [ALERT] Prefix_Suffix              : Hyphen '-' in domain (phishing brand spoofing)
    [ALERT] having_Sub_Domain          : Multiple suspicious subdomains (>2 dots)
    [OK]    HTTPS_token                : Clean domain protocol naming
============================================================
```

---

## 📁 Repository Structure

```
phishing-website-detection/
│
├── assets/                             # Portfolio visual assets
│   ├── architecture/                   # SVG and Mermaid architecture diagrams
│   ├── plots/                          # High-resolution evaluation charts
│   └── screenshots/                    # UI state mockups and screenshot guides
│
├── dataset/                            # Dataset documentation & tools
│   ├── README.md                       # Dataset overview, attributes & citation
│   ├── download_dataset.py             # Automated UCI dataset downloader & converter
│   └── phishing.csv                    # Cleaned 11,055-sample benchmark dataset
│
├── notebooks/                          # Interactive analysis
│   └── phishing_analysis.ipynb         # End-to-end Jupyter Notebook with outputs
│
├── src/                                # Core Python source code
│   ├── __init__.py                     # Package initializer
│   ├── preprocessing.py                # Dataset validation, cleaning & split
│   ├── data_preprocessing.py           # Backward-compatible alias
│   ├── feature_extractor.py            # 8-feature URL extraction engine
│   ├── models_common.py                # ShiftedCategoricalNB custom estimator
│   ├── train_models.py                 # Cross-validation training pipeline
│   ├── evaluate_models.py              # Metrics evaluation & plot generation
│   ├── model_export.py                 # Scikit-learn tree to JSON exporter
│   ├── predict.py                      # CLI & programmatic inference interface
│   └── generate_notebook.py            # Automated notebook generation script
│
├── models/                             # Trained models & metadata
│   ├── model_a/                        # Track A models (30 features, .joblib)
│   ├── model_b/                        # Track B models (.joblib, .json)
│   └── README.md                       # Model documentation & reproduction guide
│
├── extension/                          # Chrome Extension (Manifest V3)
│   ├── manifest.json                   # Extension configuration & minimal permissions
│   ├── popup.html                      # Cybersecurity dashboard popup
│   ├── popup.css                       # Responsive dark-mode styling
│   ├── popup.js                        # Active tab URL scan & UI controller
│   ├── background.js                   # Service worker lifecycle & scan counters
│   ├── feature_extractor.js            # Pure JS URL feature extractor
│   ├── model.js                        # Pure JS decision tree inference engine
│   ├── model_data.js                   # Embedded synchronous model parameters
│   ├── model.json                      # Portable JSON decision tree
│   └── icons/                          # Crisp shield icons (16px, 48px, 128px)
│
├── tests/                              # Automated test suites
│   ├── __init__.py                     # Package initializer
│   ├── test_feature_extractor.py       # 11 unit tests for URL feature rules
│   ├── test_model.py                   # 5 unit tests for models & JSON schemas
│   └── test_prediction_parity.py       # Python vs JS Node.js parity tests
│
├── results/                            # Experimental evaluation outputs
│   ├── model_comparison.csv            # Quantitative metrics across all models
│   ├── confusion_matrices/             # Confusion matrix plots (Track A & B)
│   ├── roc_curves/                     # Comparative ROC curve plots
│   └── visualizations/                 # Full correlation heatmaps, tree plots
│
├── docs/                               # Detailed technical documentation
│   ├── methodology.md                  # Mathematical formulations & ML methodology
│   ├── architecture.md                 # Detailed architectural diagrams & mapping
│   ├── project_report.md               # 21-chapter formal B.Tech laboratory report
│   └── viva_questions.md               # 40 comprehensive viva questions & answers
│
├── .gitignore                          # Python, Jupyter, Node, and OS ignore rules
├── requirements.txt                    # Annotated version-pinned dependencies
├── LICENSE                             # MIT Open Source License
├── CONTRIBUTING.md                     # Open source contribution guidelines
└── README.md                           # Master project documentation
```

---

## 🧪 Testing & Quality Assurance

Run the automated test suite with Python's built-in `unittest` framework:

```bash
python -m unittest discover tests
```

### Test Suite Summary

- `tests/test_feature_extractor.py`: 11 tests verifying URL edge cases (IPs, shortening domains, `@` signs, multi-part ccTLDs, path double slashes, malformed URLs).
- `tests/test_model.py`: 5 tests verifying dataset integrity, model deserialization, tree JSON schema, and threshold logic.
- `tests/test_prediction_parity.py`: Integration test passing a 15-URL battery through both Python and Node.js to confirm **100% vector and prediction parity**.

```text
.................
----------------------------------------------------------------------
Ran 17 tests in 0.506s

OK

==========================================================================================
 PYTHON vs JAVASCRIPT FEATURE AND PREDICTION PARITY REPORT
==========================================================================================
URL                                        | Py Pred    | JS Pred    | Vector Match | Status
------------------------------------------------------------------------------------------
https://www.google.com                     | Legitimate | Legitimate | True         | [OK] MATCH
https://github.com/torvalds/linux          | Legitimate | Legitimate | True         | [OK] MATCH
https://hud.ac.uk/students/portal          | Legitimate | Legitimate | True         | [OK] MATCH
http://192.168.1.1/admin/login.html        | Legitimate | Legitimate | True         | [OK] MATCH
https://bit.ly/3xY8a                       | Legitimate | Legitimate | True         | [OK] MATCH
http://secure-paypal-login.update-billi... | Phishing   | Phishing   | True         | [OK] MATCH
http://appleid-apple-support-recover-ac... | Legitimate | Legitimate | True         | [OK] MATCH
http://bank-of-america-verify-credentia... | Legitimate | Legitimate | True         | [OK] MATCH
http://login:secret@phishing-target.com... | Legitimate | Legitimate | True         | [OK] MATCH
http://https-secure-banking-portal-veri... | Legitimate | Legitimate | True         | [OK] MATCH
https://example.com/long_path_segment/l... | Legitimate | Legitimate | True         | [OK] MATCH
==========================================================================================
 100% PARITY CONFIRMED ACROSS ALL TEST URLS
==========================================================================================
```

---

## ⚠️ Limitations

1. **Lexical Scope**: Model B relies strictly on URL address-bar characteristics. It cannot detect phishing sites hosted on completely clean, newly registered domains that visually clone brands solely through HTML/CSS.
2. **Dynamic Evasion**: Sophisticated evasion techniques, such as Unicode/IDN homoglyph attacks or canvas-rendered login forms, require auxiliary DOM inspection.
3. **Static Training Snapshot**: The UCI dataset reflects established phishing heuristics; emerging zero-day attack patterns require continuous model retraining.
4. **Heuristic Disclaimers**: A model prediction is an automated probabilistic risk score, not a definitive legal or forensic verdict.

---

## 🔮 Future Scope

- [ ] **IDN Homoglyph Detection**: Implement Internationalized Domain Name (IDN) Punycode inspection to flag mixed-script character spoofing (e.g., Cyrillic 'а' replacing Latin 'a').
- [ ] **Shannon Entropy Calculation**: Add domain character entropy checks to flag algorithmically generated domains (DGA).
- [ ] **Hybrid Pre-Filter Pipeline**: Trigger lightweight DOM inspection only for borderline confidence scores (40%–60%).
- [ ] **Cross-Browser Manifest Port**: Expand extension compatibility to Firefox (WebExtensions API) and Safari.

---

## 👤 Author

**Biswajeet**  
- GitHub: [@Biswajeet1128](https://github.com/Biswajeet1128)  
- Focus: Machine Learning, Cybersecurity, Full-Stack Development

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
