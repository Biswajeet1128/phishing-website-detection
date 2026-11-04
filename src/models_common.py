"""
Common Model Utilities and Custom Estimators
AI-Based Phishing Website Detection System
"""

import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.naive_bayes import CategoricalNB


class ShiftedCategoricalNB(BaseEstimator, ClassifierMixin):
    """Wrapper around CategoricalNB that shifts {-1, 0, 1} to non-negative {0, 1, 2}.
    
    Inherits from BaseEstimator and ClassifierMixin to support proper Scikit-learn
    protocols, serialization, cloning, and cross-validation.
    """
    def __init__(self, min_categories=3):
        self.min_categories = min_categories
        self.model = CategoricalNB(min_categories=min_categories)
        self.classes_ = None

    def fit(self, X, y):
        X_shifted = np.array(X) + 1
        self.model.fit(X_shifted, y)
        self.classes_ = self.model.classes_
        return self

    def predict(self, X):
        X_shifted = np.array(X) + 1
        return self.model.predict(X_shifted)

    def predict_proba(self, X):
        X_shifted = np.array(X) + 1
        return self.model.predict_proba(X_shifted)
