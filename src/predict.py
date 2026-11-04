"""
URL Prediction Module (Python CLI and Programmatic Interface)
AI-Based Phishing Website Detection System

Takes a target URL, extracts features, runs inference through
the trained Model B classifier, and outputs security assessment.
"""

import os
import sys
import json
import argparse
import joblib
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.feature_extractor import extract_features, URL_FEATURE_NAMES


def load_inference_model(model_name: str = 'decision_tree'):
    """Load trained Model B joblib model."""
    model_path = os.path.join(BASE_DIR, 'models', 'model_b', f"{model_name}.joblib")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}. Please train models first.")
    return joblib.load(model_path)


def predict_url(url: str, model=None, model_name: str = 'decision_tree') -> dict:
    """Predict security assessment for a given URL.
    
    Returns:
        dict: Complete assessment including prediction, risk level, probabilities,
              extracted features, and human-readable feature findings.
    """
    if model is None:
        model = load_inference_model(model_name)
        
    import pandas as pd
    extracted = extract_features(url)
    vector_df = pd.DataFrame([extracted['vector']], columns=URL_FEATURE_NAMES)
    
    pred_class = int(model.predict(vector_df)[0])
    
    if hasattr(model, 'predict_proba'):
        probs = model.predict_proba(vector_df)[0].tolist()
        phish_prob = float(probs[1])
        legit_prob = float(probs[0])
    else:
        phish_prob = 1.0 if pred_class == 1 else 0.0
        legit_prob = 1.0 - phish_prob
        probs = [legit_prob, phish_prob]
        
    is_phishing = (pred_class == 1)
    
    # Security risk level categorization
    if phish_prob >= 0.70:
        risk_level = 'HIGH'
    elif phish_prob >= 0.45:
        risk_level = 'MODERATE'
    else:
        risk_level = 'LOW'
        
    flagged = [k for k, v in extracted['features'].items() if v == -1]
    suspicious = [k for k, v in extracted['features'].items() if v == 0]
    
    return {
        'url': url,
        'prediction': 'Phishing' if is_phishing else 'Legitimate',
        'is_phishing': is_phishing,
        'phishing_probability': round(phish_prob, 4),
        'confidence_percent': round(max(legit_prob, phish_prob) * 100, 1),
        'risk_level': risk_level,
        'risk_score': round(phish_prob * 100, 1),
        'probabilities': {
            'legitimate': round(legit_prob, 4),
            'phishing': round(phish_prob, 4)
        },
        'feature_vector': extracted['vector'],
        'feature_values': extracted['features'],
        'flagged_phishing_features': flagged,
        'suspicious_features': suspicious,
        'feature_explanations': extracted['explanations']
    }


def main():
    parser = argparse.ArgumentParser(description="AI-Based Phishing Website Detection CLI")
    parser.add_argument('--url', type=str, required=True, help="Target URL to assess")
    parser.add_argument('--model', type=str, default='decision_tree',
                        choices=['decision_tree', 'random_forest', 'categorical_nb', 'gaussian_nb', 'logistic_regression'],
                        help="Model algorithm to use for inference")
    parser.add_argument('--json', action='store_true', help="Output result formatted as JSON")
    args = parser.parse_args()
    
    res = predict_url(args.url, model_name=args.model)
    
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print("\n" + "=" * 60)
        print(" PHISHING DETECTION SECURITY ASSESSMENT")
        print("=" * 60)
        print(f" Analyzed URL: {res['url']}")
        print(f" Result:       {'[!] PHISHING DETECTED' if res['is_phishing'] else '[OK] LEGITIMATE WEBSITE'}")
        print(f" Risk Level:   {res['risk_level']} ({res['risk_score']}% Risk Score)")
        print(f" Confidence:   {res['confidence_percent']}%")
        print("-" * 60)
        print(" Extracted Feature Findings:")
        for feat, expl in res['feature_explanations'].items():
            status = res['feature_values'][feat]
            tag = " [ALERT]" if status == -1 else (" [WARN] " if status == 0 else " [OK]   ")
            print(f"   {tag} {feat.ljust(26)} : {expl}")
        print("=" * 60 + "\n")


if __name__ == '__main__':
    main()
