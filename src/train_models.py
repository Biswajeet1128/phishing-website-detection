"""
Model Training Module
AI-Based Phishing Website Detection System

Trains and tunes 5 Machine Learning algorithms for:
- Model A: 30-feature full dataset benchmark
- Model B: 8-feature URL-only real-time detection
Saves serialized models and training metadata.
"""

import os
import time
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB, CategoricalNB
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV

import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.data_preprocessing import load_dataset, get_preprocessed_data, URL_FEATURES, ALL_FEATURES
from src.models_common import ShiftedCategoricalNB

MODELS_A_DIR = os.path.join(BASE_DIR, 'models', 'model_a')
MODELS_B_DIR = os.path.join(BASE_DIR, 'models', 'model_b')


def train_and_tune_models(track: str = 'b', random_state: int = 42):
    """Train and tune all 5 ML models for specified track ('a' or 'b')."""
    print(f"\n==========================================")
    print(f" Starting Training for Track {track.upper()}")
    print(f"==========================================")
    
    df = load_dataset()
    data = get_preprocessed_data(df, random_state=random_state)
    
    if track.lower() == 'a':
        X_train = data['X_train_a']
        X_test = data['X_test_a']
        feature_names = ALL_FEATURES
        save_dir = MODELS_A_DIR
    else:
        X_train = data['X_train_b']
        X_test = data['X_test_b']
        feature_names = URL_FEATURES
        save_dir = MODELS_B_DIR
        
    y_train = data['y_train']
    y_test = data['y_test']
    
    os.makedirs(save_dir, exist_ok=True)
    
    trained_models = {}
    training_times = {}
    
    # ----------------------------------------------------
    # 1. Decision Tree Classifier
    # ----------------------------------------------------
    print(f"\n[1/5] Tuning & Training Decision Tree (Track {track.upper()})...")
    dt_params = {
        'max_depth': [4, 6, 8, 10, 12, None],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'criterion': ['gini', 'entropy']
    }
    t0 = time.time()
    dt_grid = GridSearchCV(
        DecisionTreeClassifier(random_state=random_state),
        dt_params,
        cv=5,
        scoring='f1',
        n_jobs=-1
    )
    dt_grid.fit(X_train, y_train)
    t_dt = time.time() - t0
    best_dt = dt_grid.best_estimator_
    trained_models['Decision_Tree'] = best_dt
    training_times['Decision_Tree'] = t_dt
    print(f"   Best DT params: {dt_grid.best_params_} (CV F1: {dt_grid.best_score_:.4f}) in {t_dt:.2f}s")
    
    # ----------------------------------------------------
    # 2. Gaussian Naive Bayes
    # ----------------------------------------------------
    print(f"\n[2/5] Training Gaussian Naive Bayes (Track {track.upper()})...")
    t0 = time.time()
    gnb = GaussianNB()
    gnb.fit(X_train, y_train)
    t_gnb = time.time() - t0
    trained_models['Gaussian_NB'] = gnb
    training_times['Gaussian_NB'] = t_gnb
    print(f"   Gaussian NB trained in {t_gnb:.2f}s")
    
    # ----------------------------------------------------
    # 3. Categorical Naive Bayes
    # ----------------------------------------------------
    print(f"\n[3/5] Training Categorical Naive Bayes (Track {track.upper()})...")
    t0 = time.time()
    cnb = ShiftedCategoricalNB(min_categories=3)
    cnb.fit(X_train, y_train)
    t_cnb = time.time() - t0
    trained_models['Categorical_NB'] = cnb
    training_times['Categorical_NB'] = t_cnb
    print(f"   Categorical NB trained in {t_cnb:.2f}s")
    
    # ----------------------------------------------------
    # 4. Random Forest Classifier
    # ----------------------------------------------------
    print(f"\n[4/5] Tuning & Training Random Forest (Track {track.upper()})...")
    rf_params = {
        'n_estimators': [50, 100, 150],
        'max_depth': [6, 8, 12, None] if track.lower() == 'b' else [10, 15, None],
        'min_samples_split': [2, 5],
        'min_samples_leaf': [1, 2]
    }
    t0 = time.time()
    rf_grid = GridSearchCV(
        RandomForestClassifier(random_state=random_state),
        rf_params,
        cv=5,
        scoring='f1',
        n_jobs=-1
    )
    rf_grid.fit(X_train, y_train)
    t_rf = time.time() - t0
    best_rf = rf_grid.best_estimator_
    trained_models['Random_Forest'] = best_rf
    training_times['Random_Forest'] = t_rf
    print(f"   Best RF params: {rf_grid.best_params_} (CV F1: {rf_grid.best_score_:.4f}) in {t_rf:.2f}s")
    
    # ----------------------------------------------------
    # 5. Logistic Regression (Baseline Comparison)
    # ----------------------------------------------------
    print(f"\n[5/5] Training Logistic Regression (Track {track.upper()})...")
    t0 = time.time()
    lr = LogisticRegression(max_iter=1000, random_state=random_state)
    lr.fit(X_train, y_train)
    t_lr = time.time() - t0
    trained_models['Logistic_Regression'] = lr
    training_times['Logistic_Regression'] = t_lr
    print(f"   Logistic Regression trained in {t_lr:.2f}s")
    
    # Save all models to disk
    print(f"\nSaving trained models to {save_dir}...")
    for name, model in trained_models.items():
        model_path = os.path.join(save_dir, f"{name.lower()}.joblib")
        joblib.dump(model, model_path)
        print(f"   Saved {name} -> {model_path}")
        
    # Save training metadata
    metadata = {
        'track': track.upper(),
        'feature_names': feature_names,
        'num_features': len(feature_names),
        'num_train_samples': len(X_train),
        'num_test_samples': len(X_test),
        'random_state': random_state,
        'training_times': training_times,
        'best_dt_params': dt_grid.best_params_,
        'best_rf_params': rf_grid.best_params_
    }
    metadata_path = os.path.join(save_dir, 'training_metadata.json')
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=4)
    print(f"   Saved metadata -> {metadata_path}")
    
    return trained_models, training_times


def main():
    print("Initiating full training pipeline for Model A and Model B...")
    # Train Track A (All 30 features)
    train_and_tune_models(track='a')
    # Train Track B (8 URL features)
    train_and_tune_models(track='b')
    print("\nAll models for both tracks successfully trained and saved!")


if __name__ == '__main__':
    main()
