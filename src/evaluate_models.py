"""
Model Evaluation and Visualization Module
AI-Based Phishing Website Detection System

Evaluates all models for Track A and Track B on the test sets.
Generates metrics, comparison tables, and academic visualization plots.
"""

import os
import sys
import time
import json
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, confusion_matrix, precision_recall_curve
)
from sklearn.tree import plot_tree

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.data_preprocessing import load_dataset, get_preprocessed_data, URL_FEATURES, ALL_FEATURES
from src.models_common import ShiftedCategoricalNB

# Set plotting style for professional academic presentation
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8


def evaluate_single_model(model, X_test, y_test):
    """Compute all evaluation metrics and latency for a trained model."""
    t0 = time.time()
    preds = model.predict(X_test)
    pred_time = time.time() - t0
    
    # Check probability predictions for ROC-AUC
    if hasattr(model, 'predict_proba'):
        probs = model.predict_proba(X_test)[:, 1]
    elif hasattr(model, 'decision_function'):
        probs = model.decision_function(X_test)
    else:
        probs = preds
        
    acc = accuracy_score(y_test, preds)
    prec = precision_score(y_test, preds, zero_division=0)
    rec = recall_score(y_test, preds, zero_division=0)
    f1 = f1_score(y_test, preds, zero_division=0)
    
    try:
        auc = roc_auc_score(y_test, probs)
    except Exception:
        auc = 0.5
        
    cm = confusion_matrix(y_test, preds)
    # y=1 is Phishing, y=0 is Legitimate
    # cm: [[TN, FP], [FN, TP]]
    tn, fp, fn, tp = cm.ravel()
    
    return {
        'accuracy': acc,
        'precision': prec,
        'recall': rec,
        'f1_score': f1,
        'roc_auc': auc,
        'pred_time_total': pred_time,
        'pred_latency_ms': (pred_time / len(X_test)) * 1000.0,
        'tn': int(tn),
        'fp': int(fp),
        'fn': int(fn),
        'tp': int(tp),
        'confusion_matrix': cm,
        'probs': probs,
        'preds': preds
    }


def run_full_evaluation():
    print("=" * 65)
    print(" Executing Comprehensive Model Evaluation Pipeline")
    print("=" * 65)
    
    df = load_dataset()
    data = get_preprocessed_data(df)
    
    X_test_a = data['X_test_a']
    X_test_b = data['X_test_b']
    y_test = data['y_test']
    
    results_dir = os.path.join(BASE_DIR, 'results')
    cm_dir = os.path.join(results_dir, 'confusion_matrices')
    roc_dir = os.path.join(results_dir, 'roc_curves')
    viz_dir = os.path.join(results_dir, 'visualizations')
    
    os.makedirs(cm_dir, exist_ok=True)
    os.makedirs(roc_dir, exist_ok=True)
    os.makedirs(viz_dir, exist_ok=True)
    
    model_names = ['Decision_Tree', 'Gaussian_NB', 'Categorical_NB', 'Random_Forest', 'Logistic_Regression']
    
    # -----------------------------------------------------------------
    # Generate EDA Visualizations first
    # -----------------------------------------------------------------
    print("\n[Step 1/4] Generating Dataset & EDA Visualizations...")
    
    # 1. Target Class Distribution
    fig, ax = plt.subplots(figsize=(7, 5))
    counts = df['Result'].value_counts()
    labels = ['Legitimate (1)', 'Phishing (-1)']
    bar_colors = ['#2ecc71', '#e74c3c']
    bars = ax.bar(labels, [counts.get(1, 0), counts.get(-1, 0)], color=bar_colors, edgecolor='black', width=0.55)
    for bar in bars:
        h = bar.get_height()
        pct = (h / len(df)) * 100
        ax.annotate(f'{h:,} ({pct:.1f}%)',
                    xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 4), textcoords="offset points",
                    ha='center', va='bottom', fontsize=11, fontweight='bold')
    ax.set_title("UCI Phishing Websites Dataset: Target Class Distribution", fontsize=13, fontweight='bold', pad=12)
    ax.set_ylabel("Number of Instances", fontsize=11)
    ax.set_ylim(0, max(counts) * 1.15)
    plt.tight_layout()
    plt.savefig(os.path.join(viz_dir, 'class_distribution.png'), dpi=300)
    plt.close()
    
    # 2. Correlation Heatmap (Full 30 features + Target)
    fig, ax = plt.subplots(figsize=(18, 15))
    corr = df.corr()
    sns.heatmap(corr, cmap='vlag', vmin=-1, vmax=1, annot=False, linewidths=0.5, ax=ax, cbar_kws={'shrink': 0.8})
    ax.set_title("Complete Feature Correlation Matrix (30 Features + Result)", fontsize=15, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(viz_dir, 'feature_correlation_heatmap.png'), dpi=300)
    plt.close()
    
    # 3. Model B URL Features Correlation Heatmap
    url_df = df[URL_FEATURES + ['Result']].copy()
    fig, ax = plt.subplots(figsize=(9, 7))
    sns.heatmap(url_df.corr(), annot=True, fmt='.2f', cmap='coolwarm', vmin=-1, vmax=1, linewidths=0.5, ax=ax)
    ax.set_title("Model B: URL Features Correlation Heatmap", fontsize=12, fontweight='bold', pad=10)
    plt.tight_layout()
    plt.savefig(os.path.join(viz_dir, 'url_feature_correlation_heatmap.png'), dpi=300)
    plt.close()
    
    # -----------------------------------------------------------------
    # Load and evaluate Track A and Track B models
    # -----------------------------------------------------------------
    print("\n[Step 2/4] Evaluating Track A and Track B Models...")
    
    # Load training metadata for times
    with open(os.path.join(BASE_DIR, 'models', 'model_a', 'training_metadata.json'), 'r') as f:
        meta_a = json.load(f)
    with open(os.path.join(BASE_DIR, 'models', 'model_b', 'training_metadata.json'), 'r') as f:
        meta_b = json.load(f)
        
    metrics_records = []
    eval_cache_a = {}
    eval_cache_b = {}
    
    # Evaluate Track A
    for name in model_names:
        model_path = os.path.join(BASE_DIR, 'models', 'model_a', f"{name.lower()}.joblib")
        model = joblib.load(model_path)
        res = evaluate_single_model(model, X_test_a, y_test)
        eval_cache_a[name] = res
        train_t = meta_a['training_times'].get(name, 0.0)
        
        metrics_records.append({
            'Track': 'Model A (30 Features)',
            'Algorithm': name.replace('_', ' '),
            'Accuracy': round(res['accuracy'], 4),
            'Precision': round(res['precision'], 4),
            'Recall (Phishing)': round(res['recall'], 4),
            'F1-Score': round(res['f1_score'], 4),
            'ROC-AUC': round(res['roc_auc'], 4),
            'False Negatives (FN)': res['fn'],
            'False Positives (FP)': res['fp'],
            'Training Time (s)': round(train_t, 3),
            'Pred Latency (ms/sample)': round(res['pred_latency_ms'], 4)
        })
        
    # Evaluate Track B
    for name in model_names:
        model_path = os.path.join(BASE_DIR, 'models', 'model_b', f"{name.lower()}.joblib")
        model = joblib.load(model_path)
        res = evaluate_single_model(model, X_test_b, y_test)
        eval_cache_b[name] = res
        train_t = meta_b['training_times'].get(name, 0.0)
        
        metrics_records.append({
            'Track': 'Model B (8 URL Features)',
            'Algorithm': name.replace('_', ' '),
            'Accuracy': round(res['accuracy'], 4),
            'Precision': round(res['precision'], 4),
            'Recall (Phishing)': round(res['recall'], 4),
            'F1-Score': round(res['f1_score'], 4),
            'ROC-AUC': round(res['roc_auc'], 4),
            'False Negatives (FN)': res['fn'],
            'False Positives (FP)': res['fp'],
            'Training Time (s)': round(train_t, 3),
            'Pred Latency (ms/sample)': round(res['pred_latency_ms'], 4)
        })
        
    results_df = pd.DataFrame(metrics_records)
    csv_out = os.path.join(results_dir, 'model_comparison.csv')
    results_df.to_csv(csv_out, index=False)
    print(f"Saved comprehensive model comparison to {csv_out}")
    
    # -----------------------------------------------------------------
    # Visualizations: Confusion Matrices and ROC Curves
    # -----------------------------------------------------------------
    print("\n[Step 3/4] Generating Confusion Matrices and ROC Curves...")
    
    # Plot Confusion Matrices for both tracks
    for track_name, cache in [('Track_A', eval_cache_a), ('Track_B', eval_cache_b)]:
        fig, axes = plt.subplots(1, 5, figsize=(22, 4.2))
        for idx, name in enumerate(model_names):
            cm = cache[name]['confusion_matrix']
            ax = axes[idx]
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False, ax=ax,
                        xticklabels=['Legit (0)', 'Phish (1)'],
                        yticklabels=['Legit (0)', 'Phish (1)'])
            ax.set_title(f"{name.replace('_', ' ')}\nAcc: {cache[name]['accuracy']:.3f} | Rec: {cache[name]['recall']:.3f}", fontsize=10, fontweight='bold')
            ax.set_xlabel('Predicted Label', fontsize=9)
            ax.set_ylabel('True Label', fontsize=9)
        plt.suptitle(f"Confusion Matrices: {track_name.replace('_', ' ')}", fontsize=14, fontweight='bold', y=1.05)
        plt.tight_layout()
        plt.savefig(os.path.join(cm_dir, f"confusion_matrices_{track_name.lower()}.png"), dpi=300, bbox_inches='tight')
        plt.close()
        
    # Plot ROC Curves Comparison
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    for idx, name in enumerate(model_names):
        probs_a = eval_cache_a[name]['probs']
        fpr_a, tpr_a, _ = roc_curve(y_test, probs_a)
        auc_a = eval_cache_a[name]['roc_auc']
        ax1.plot(fpr_a, tpr_a, color=colors[idx], lw=2, label=f"{name.replace('_', ' ')} (AUC = {auc_a:.3f})")
        
        probs_b = eval_cache_b[name]['probs']
        fpr_b, tpr_b, _ = roc_curve(y_test, probs_b)
        auc_b = eval_cache_b[name]['roc_auc']
        ax2.plot(fpr_b, tpr_b, color=colors[idx], lw=2, label=f"{name.replace('_', ' ')} (AUC = {auc_b:.3f})")
        
    for ax, title in [(ax1, "Model A: 30 Features ROC Curve"), (ax2, "Model B: 8 URL Features ROC Curve")]:
        ax.plot([0, 1], [0, 1], 'k--', lw=1.2, alpha=0.7)
        ax.set_xlim([0.0, 1.0])
        ax.set_ylim([0.0, 1.05])
        ax.set_xlabel('False Positive Rate (1 - Specificity)', fontsize=11)
        ax.set_ylabel('True Positive Rate (Phishing Recall)', fontsize=11)
        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.legend(loc='lower right', frameon=True)
        ax.grid(True, linestyle='--', alpha=0.5)
        
    plt.tight_layout()
    plt.savefig(os.path.join(roc_dir, 'roc_curves_comparison.png'), dpi=300)
    plt.close()
    
    # -----------------------------------------------------------------
    # Feature Importances & Decision Tree Visualization
    # -----------------------------------------------------------------
    print("\n[Step 4/4] Generating Feature Importance & Tree Visualizations...")
    
    # Feature Importance for Random Forest Model B
    rf_b = joblib.load(os.path.join(BASE_DIR, 'models', 'model_b', 'random_forest.joblib'))
    fig, ax = plt.subplots(figsize=(9, 5))
    importances_b = pd.Series(rf_b.feature_importances_, index=URL_FEATURES).sort_values(ascending=True)
    importances_b.plot(kind='barh', color='#3498db', edgecolor='black', ax=ax)
    ax.set_title("Model B: Feature Importances (Random Forest)", fontsize=13, fontweight='bold')
    ax.set_xlabel("Gini Importance Score", fontsize=11)
    for i, v in enumerate(importances_b):
        ax.text(v + 0.005, i, f"{v:.3f}", va='center', fontsize=10, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(viz_dir, 'feature_importance_rf_model_b.png'), dpi=300)
    plt.close()
    
    # Feature Importance for Random Forest Model A (Top 10)
    rf_a = joblib.load(os.path.join(BASE_DIR, 'models', 'model_a', 'random_forest.joblib'))
    fig, ax = plt.subplots(figsize=(10, 6))
    importances_a = pd.Series(rf_a.feature_importances_, index=ALL_FEATURES).sort_values(ascending=False).head(12).sort_values(ascending=True)
    importances_a.plot(kind='barh', color='#2ecc71', edgecolor='black', ax=ax)
    ax.set_title("Model A: Top 12 Feature Importances (Random Forest)", fontsize=13, fontweight='bold')
    ax.set_xlabel("Gini Importance Score", fontsize=11)
    for i, v in enumerate(importances_a):
        ax.text(v + 0.003, i, f"{v:.3f}", va='center', fontsize=10, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(viz_dir, 'feature_importance_rf_model_a.png'), dpi=300)
    plt.close()
    
    # Decision Tree Visualization (Model B)
    dt_b = joblib.load(os.path.join(BASE_DIR, 'models', 'model_b', 'decision_tree.joblib'))
    fig, ax = plt.subplots(figsize=(24, 10))
    plot_tree(
        dt_b,
        max_depth=3,
        feature_names=URL_FEATURES,
        class_names=['Legitimate', 'Phishing'],
        filled=True,
        rounded=True,
        fontsize=9,
        ax=ax
    )
    ax.set_title("Decision Tree Visualization (Model B, First 3 Levels)", fontsize=15, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(viz_dir, 'decision_tree_visualization.png'), dpi=300)
    plt.close()
    
    # Performance comparison bar chart
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 5.5))
    df_a = results_df[results_df['Track'] == 'Model A (30 Features)']
    df_b = results_df[results_df['Track'] == 'Model B (8 URL Features)']
    
    df_a.plot(x='Algorithm', y=['Accuracy', 'Recall (Phishing)', 'F1-Score'], kind='bar', ax=ax1, colormap='viridis', width=0.7)
    ax1.set_title("Model A Performance Across Algorithms", fontsize=12, fontweight='bold')
    ax1.set_ylabel("Score", fontsize=11)
    ax1.set_ylim(0.5, 1.02)
    ax1.tick_params(axis='x', rotation=30)
    ax1.legend(loc='lower right')
    
    df_b.plot(x='Algorithm', y=['Accuracy', 'Recall (Phishing)', 'F1-Score'], kind='bar', ax=ax2, colormap='viridis', width=0.7)
    ax2.set_title("Model B Performance Across Algorithms", fontsize=12, fontweight='bold')
    ax2.set_ylabel("Score", fontsize=11)
    ax2.set_ylim(0.5, 1.02)
    ax2.tick_params(axis='x', rotation=30)
    ax2.legend(loc='lower right')
    
    plt.tight_layout()
    plt.savefig(os.path.join(viz_dir, 'model_performance_comparison.png'), dpi=300)
    plt.close()
    
    print("\n" + "=" * 65)
    print(" SUMMARY COMPARISON TABLE")
    print("=" * 65)
    print(results_df[['Track', 'Algorithm', 'Accuracy', 'Recall (Phishing)', 'F1-Score', 'ROC-AUC', 'False Negatives (FN)']].to_string(index=False))
    print("=" * 65)
    
    # -----------------------------------------------------------------
    # Model Selection Analysis for Deployment (Model B)
    # -----------------------------------------------------------------
    # We prioritize Phishing Recall (minimizing False Negatives) and F1-Score
    b_df = results_df[results_df['Track'] == 'Model B (8 URL Features)'].copy()
    b_df_sorted = b_df.sort_values(by=['Recall (Phishing)', 'F1-Score', 'False Negatives (FN)'], ascending=[False, False, True])
    selected_algo = b_df_sorted.iloc[0]['Algorithm']
    print(f"\n>> Selected Deployed Model for Extension: {selected_algo}")
    print(f"   Reason: Highest Phishing Recall ({b_df_sorted.iloc[0]['Recall (Phishing)']:.4f}) and minimum False Negatives ({b_df_sorted.iloc[0]['False Negatives (FN)']}).")
    
    return results_df, selected_algo


if __name__ == '__main__':
    run_full_evaluation()
