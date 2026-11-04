"""
Unit Tests for Machine Learning Models and Artifacts
AI-Based Phishing Website Detection System
"""

import unittest
import os
import sys
import json
import joblib
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.data_preprocessing import load_dataset, validate_dataset, ALL_FEATURES, URL_FEATURES
from src.predict import predict_url, load_inference_model


class TestModelArtifacts(unittest.TestCase):

    def test_dataset_integrity(self):
        """Validate dataset shape, column names, null counts and class balance."""
        csv_path = os.path.join(BASE_DIR, 'dataset', 'phishing.csv')
        self.assertTrue(os.path.exists(csv_path), "Dataset CSV file is missing.")

        df = pd.read_csv(csv_path)
        self.assertEqual(df.shape, (11055, 31))
        self.assertEqual(df.isnull().sum().sum(), 0, "Dataset contains unexpected null values.")

        val = validate_dataset(df)
        self.assertEqual(len(val['missing_features']), 0, f"Missing features: {val['missing_features']}")
        self.assertEqual(set(val['target_distribution'].keys()), {-1, 1})

    def test_model_files_exist(self):
        """Verify all 5 trained model files exist for both Track A and Track B."""
        algorithms = ['decision_tree', 'gaussian_nb', 'categorical_nb', 'random_forest', 'logistic_regression']
        
        for algo in algorithms:
            path_a = os.path.join(BASE_DIR, 'models', 'model_a', f"{algo}.joblib")
            path_b = os.path.join(BASE_DIR, 'models', 'model_b', f"{algo}.joblib")
            self.assertTrue(os.path.exists(path_a), f"Missing Model A artifact: {path_a}")
            self.assertTrue(os.path.exists(path_b), f"Missing Model B artifact: {path_b}")

    def test_model_loading_and_prediction(self):
        """Test loading Model B and predicting on safe and phishing feature vectors."""
        dt = load_inference_model('decision_tree')
        rf = load_inference_model('random_forest')
        
        # Safe feature vector (all +1)
        safe_vector = pd.DataFrame([[1, 1, 1, 1, 1, 1, 1, 1]], columns=URL_FEATURES)
        pred_dt = dt.predict(safe_vector)[0]
        pred_rf = rf.predict(safe_vector)[0]
        self.assertEqual(pred_dt, 0, "Safe vector should be predicted as Legitimate (0).")
        self.assertEqual(pred_rf, 0, "Safe vector should be predicted as Legitimate (0).")

        # Phishing feature vector (multiple suspicious flags)
        phish_vector = pd.DataFrame([[-1, -1, -1, -1, -1, -1, -1, -1]], columns=URL_FEATURES)
        pred_dt_phish = dt.predict(phish_vector)[0]
        pred_rf_phish = rf.predict(phish_vector)[0]
        self.assertEqual(pred_dt_phish, 1, "Extreme malicious vector should be predicted as Phishing (1).")
        self.assertEqual(pred_rf_phish, 1, "Extreme malicious vector should be predicted as Phishing (1).")

    def test_json_export_structure(self):
        """Verify the exported JSON model conforms to required schema for JS inference."""
        json_path = os.path.join(BASE_DIR, 'models', 'model_b', 'model.json')
        ext_json_path = os.path.join(BASE_DIR, 'extension', 'model.json')
        
        self.assertTrue(os.path.exists(json_path), "Model B model.json missing.")
        self.assertTrue(os.path.exists(ext_json_path), "Extension model.json missing.")

        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.assertEqual(data.get('model_type'), 'DecisionTreeClassifier')
        self.assertEqual(data.get('num_features'), 8)
        self.assertEqual(data.get('feature_names'), URL_FEATURES)
        self.assertIn('tree', data)

        # Validate root node schema
        root = data['tree']
        self.assertIn('node_id', root)
        self.assertIn('is_leaf', root)
        self.assertIn('probabilities', root)
        if not root['is_leaf']:
            self.assertIn('left', root)
            self.assertIn('right', root)
            self.assertIn('feature_index', root)
            self.assertIn('threshold', root)

    def test_predict_url_helper(self):
        """Test high-level predict_url wrapper function."""
        res_safe = predict_url("https://www.google.com")
        self.assertEqual(res_safe['prediction'], 'Legitimate')
        self.assertFalse(res_safe['is_phishing'])
        self.assertEqual(res_safe['risk_level'], 'LOW')

        res_phish = predict_url("http://secure-paypal-login.update-billing.account-security.com//verify")
        self.assertEqual(res_phish['prediction'], 'Phishing')
        self.assertTrue(res_phish['is_phishing'])


if __name__ == '__main__':
    unittest.main()
