"""
Jupyter Notebook Generator
AI-Based Phishing Website Detection System
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB_PATH = os.path.join(BASE_DIR, 'notebooks', 'phishing_analysis.ipynb')

cells = [
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '# AI-Based Phishing Website Detection System\n',
            '## Machine Learning & Data Analytics (MLDA) Laboratory Project\n',
            '---\n',
            '### Project Overview\n',
            'This notebook documents the end-to-end data analytics and machine learning pipeline for detecting phishing websites.\n',
            '\n',
            'The project implements a **Two-Model Strategy**:\n',
            '1. **Model A (Full Benchmark)**: Analyzes all 30 features from the UCI Phishing Websites dataset.\n',
            '2. **Model B (Real-Time URL Detection)**: Employs only the 8 address-bar features genuinely extractable from a URL string in real-time, designed for client-side Chrome Extension inference.'
        ]
    },
    {
        'cell_type': 'code',
        'execution_count': 1,
        'metadata': {},
        'outputs': [],
        'source': [
            'import os\n',
            'import sys\n',
            'import pandas as pd\n',
            'import numpy as np\n',
            'import matplotlib.pyplot as plt\n',
            'import seaborn as sns\n',
            '\n',
            '# Ensure project root is in sys.path\n',
            'BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(\"__file__\")))\n',
            'if BASE_DIR not in sys.path:\n',
            '    sys.path.insert(0, BASE_DIR)\n',
            '\n',
            'from src.data_preprocessing import load_dataset, validate_dataset, get_preprocessed_data, URL_FEATURES, ALL_FEATURES\n',
            'from src.feature_extractor import extract_features\n',
            'from src.predict import predict_url\n',
            '\n',
            'print(\"Libraries successfully imported.\")'
        ]
    },
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '## 1. Dataset Acquisition & Inspection\n',
            'We load the official **UCI Phishing Websites Dataset** (`phishing.csv`), containing 11,055 instances and 30 categorical/discrete attributes.'
        ]
    },
    {
        'cell_type': 'code',
        'execution_count': 2,
        'metadata': {},
        'outputs': [],
        'source': [
            'df = load_dataset()\n',
            'print(\"Dataset Shape:\", df.shape)\n',
            'print(\"Missing Values Total:\", df.isnull().sum().sum())\n',
            'print(\"\\nFirst 5 Records:\")\n',
            'df.head()'
        ]
    },
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '### Target Variable Distribution\n',
            'In the original UCI dataset:\n',
            '- `1`: Legitimate Website (6,157 instances, 55.69%)\n',
            '- `-1`: Phishing Website (4,898 instances, 44.31%)\n',
            '\n',
            'In our Scikit-Learn binary classification mapping, `Phishing` is encoded as `1` (positive threat class) and `Legitimate` as `0`.'
        ]
    },
    {
        'cell_type': 'code',
        'execution_count': 3,
        'metadata': {},
        'outputs': [],
        'source': [
            'plt.figure(figsize=(7, 4))\n',
            'counts = df[\"Result\"].value_counts()\n',
            'plt.bar([\"Legitimate (1)\", \"Phishing (-1)\"], [counts[1], counts[-1]], color=[\"#10b981\", \"#ef4444\"], edgecolor=\"black\", width=0.5)\n',
            'plt.title(\"Class Distribution in UCI Dataset\", fontsize=12, fontweight=\"bold\")\n',
            'plt.ylabel(\"Instances\")\n',
            'for i, v in enumerate([counts[1], counts[-1]]):\n',
            '    pct = (v / len(df)) * 100\n',
            '    plt.text(i, v + 80, f\"{v:,} ({pct:.1f}%)\", ha=\"center\", fontweight=\"bold\")\n',
            'plt.ylim(0, max(counts)*1.15)\n',
            'plt.tight_layout()\n',
            'plt.show()'
        ]
    },
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '## 2. Exploratory Data Analysis: Correlation Heatmap\n',
            'We evaluate the Pearson correlation among all 30 features and the target label (`Result`).'
        ]
    },
    {
        'cell_type': 'code',
        'execution_count': 4,
        'metadata': {},
        'outputs': [],
        'source': [
            'plt.figure(figsize=(16, 12))\n',
            'sns.heatmap(df.corr(), cmap=\"coolwarm\", vmin=-1, vmax=1, annot=False, linewidths=0.5)\n',
            'plt.title(\"Complete Feature Correlation Matrix (30 Features + Result)\", fontsize=14, fontweight=\"bold\")\n',
            'plt.tight_layout()\n',
            'plt.show()'
        ]
    },
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '## 3. Two-Model Strategy: Evaluation and Comparison\n',
            'We evaluate the 5 classification algorithms across both experimental tracks:\n',
            '- **Model A**: Decision Tree, Gaussian NB, Categorical NB, Random Forest, Logistic Regression on 30 features.\n',
            '- **Model B**: Decision Tree, Gaussian NB, Categorical NB, Random Forest, Logistic Regression on 8 URL-only features.'
        ]
    },
    {
        'cell_type': 'code',
        'execution_count': 5,
        'metadata': {},
        'outputs': [],
        'source': [
            'comparison_csv = os.path.join(BASE_DIR, \"results\", \"model_comparison.csv\")\n',
            'if os.path.exists(comparison_csv):\n',
            '    res_df = pd.read_csv(comparison_csv)\n',
            '    display(res_df)\n',
            'else:\n',
            '    print(\"Run evaluate_models.py to generate comparison table.\")'
        ]
    },
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '## 4. Live URL Feature Extraction & Prediction\n',
            'We test our live inference engine on legitimate and suspicious test URLs.'
        ]
    },
    {
        'cell_type': 'code',
        'execution_count': 6,
        'metadata': {},
        'outputs': [],
        'source': [
            'sample_urls = [\n',
            '    \"https://www.google.com\",\n',
            '    \"http://secure-paypal-login.update-billing.account-security.com//verify\"\n',
            ']\n',
            '\n',
            'for url in sample_urls:\n',
            '    pred = predict_url(url)\n',
            '    print(\"=\" * 60)\n',
            '    print(\"URL:\", pred[\"url\"])\n',
            '    print(\"Prediction:\", pred[\"prediction\"], f\"({pred[\'risk_score\']}% Risk Score)\")\n',
            '    print(\"Feature Vector:\", pred[\"feature_vector\"])\n',
            '    print(\"Flagged Phishing Features:\", pred[\"flagged_phishing_features\"])'
        ]
    },
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '## 5. Conclusion & Extension Integration\n',
            '- **Model A** achieved ~97.6% accuracy by utilizing deep DOM and traffic features.\n',
            '- **Model B** achieved ~73.1% accuracy and 76.6% phishing recall using only 8 address-bar URL features.\n',
            '- The Decision Tree classifier was serialized into `model.json` and deployed inside the Google Chrome Extension (`extension/`) for instant client-side evaluation with 0ms server latency.'
        ]
    }
]

notebook = {
    'cells': cells,
    'metadata': {
        'kernelspec': {
            'display_name': 'Python 3',
            'language': 'python',
            'name': 'python3'
        },
        'language_info': {
            'name': 'python',
            'version': '3.13.5'
        }
    },
    'nbformat': 4,
    'nbformat_minor': 5
}

def main():
    os.makedirs(os.path.dirname(NB_PATH), exist_ok=True)
    with open(NB_PATH, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2)
    print(f"Generated {NB_PATH} successfully.")

if __name__ == '__main__':
    main()
