# System Architecture Documentation
## AI-Based Phishing Website Detection System

This document describes the architectural layout, data pipelines, model deployment, and browser runtime execution flow.

---

## 1. End-to-End System Pipeline

```mermaid
flowchart TD
    subgraph Data Pipeline
        A["UCI ARFF Dataset (11,055 samples)"] --> B["Data Preprocessing (src/preprocessing.py)"]
        B --> C["Stratified Split: 80% Train / 20% Test"]
    end

    subgraph Two-Model Strategy
        C --> D["Track A: 30 Features (Full Benchmark)"]
        C --> E["Track B: 8 Address-Bar Features (Real-Time)"]
        D --> F["5 Models: RF (97.6%), DT (97.0%), CNB (93.3%)"]
        E --> G["5 Models: DT (73.1%), RF (73.1%), CNB (72.9%)"]
    end

    subgraph Model Serialization
        G --> H["Select Model B Decision Tree (F1: 71.7%, Recall: 76.6%)"]
        H --> I["Model Serializer (src/model_export.py)"]
        I --> J["extension/model.json & model_data.js (31 KB)"]
    end

    subgraph Chrome Extension Manifest V3
        K["User Navigates Tab"] --> L["chrome.tabs.query (popup.js)"]
        L --> M["JS Feature Extractor (feature_extractor.js)"]
        M --> N["8-Element Discrete Vector"]
        J --> O["Pure JS Inference Engine (model.js)"]
        N --> O
        O --> P["Cybersecurity Dashboard UI"]
    end
```

---

## 2. Real-Time Browser URL Detection Pipeline

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant Browser as Chrome Browser (Active Tab)
    participant Popup as Extension Popup (popup.js)
    participant Extractor as JS Feature Extractor (feature_extractor.js)
    participant Engine as Inference Engine (model.js)
    participant UI as Popup Dashboard (popup.html)

    User->>Browser: Opens target website
    User->>Popup: Clicks PhishShield AI icon
    Popup->>Browser: Queries activeTab.url
    Browser-->>Popup: Returns URL string (e.g., https://example.com)
    
    alt URL is Internal Scheme (chrome://, about:, file://)
        Popup->>UI: Displays UNKNOWN / INTERNAL state (exempt from scan)
    else URL is Web Scheme (http://, https://)
        Popup->>Extractor: extractFeatures(url)
        Extractor-->>Popup: Returns 8-element vector & feature findings
        Popup->>Engine: predictVector(vector)
        Engine-->>Popup: Returns { label, risk_level, confidence, risk_score }
        Popup->>UI: Renders LEGITIMATE (Green) or PHISHING (Red) with guidance
    end
```

---

## 3. Directory and Component Mapping

| Component | Files | Primary Responsibility |
|---|---|---|
| **Data Engineering** | `src/preprocessing.py`, `dataset/download_dataset.py` | Dataset ingestion, duplicate analysis, stratified splitting |
| **Feature Extraction** | `src/feature_extractor.py`, `extension/feature_extractor.js` | 8-feature URL extraction with 100% parity |
| **Model Training** | `src/train_models.py`, `src/models_common.py` | 5-fold CV hyperparameter tuning across 5 algorithms |
| **Model Evaluation** | `src/evaluate_models.py` | Metrics calculation, confusion matrices, ROC curves |
| **Deployment Engine** | `src/model_export.py`, `extension/model.js` | Tree serialization to JSON & pure JS browser execution |
| **Browser Extension** | `extension/manifest.json`, `popup.html`, `popup.css`, `popup.js`, `background.js` | Manifest V3 cybersecurity dashboard |
| **Quality Assurance** | `tests/test_feature_extractor.py`, `test_model.py`, `test_prediction_parity.py` | Automated testing & Python-JS parity verification |
