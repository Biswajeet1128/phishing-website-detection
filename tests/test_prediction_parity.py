"""
Prediction and Feature Parity Verification Suite
AI-Based Phishing Website Detection System

Verifies 100% parity between Python and JavaScript feature extractors
and prediction engines on a diverse battery of test URLs.
"""

import unittest
import os
import sys
import json
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.feature_extractor import extract_features
from src.predict import predict_url


TEST_URL_SUITE = [
    "https://www.google.com",
    "https://github.com/torvalds/linux",
    "https://hud.ac.uk/students/portal",
    "http://192.168.1.1/admin/login.html",
    "https://bit.ly/3xY8a",
    "http://secure-paypal-login.update-billing.account-security.com//verify",
    "http://appleid-apple-support-recover-account.info//login",
    "http://bank-of-america-verify-credentials.com//security",
    "http://login:secret@phishing-target.com/banking",
    "http://https-secure-banking-portal-verification.com/login",
    "https://example.com/" + "long_path_segment/" * 6
]


def run_js_eval(urls):
    """Execute JavaScript feature extraction and model inference via Node.js."""
    js_script = """
    const fe = require('./extension/feature_extractor.js');
    const { PhishingPredictor } = require('./extension/model.js');
    const modelData = require('./extension/model.json');

    const predictor = new PhishingPredictor(modelData);
    const urls = JSON.parse(process.argv[process.argv.length - 1]);
    const results = [];

    for (const u of urls) {
      const feat = fe.extractFeatures(u);
      const pred = predictor.predictVector(feat.vector);
      results.push({
        url: u,
        vector: feat.vector,
        prediction: pred.label,
        is_phishing: pred.is_phishing,
        risk_score: pred.risk_score_percent
      });
    }

    console.log(JSON.stringify(results));
    """
    cmd = ['node', '-e', js_script, json.dumps(urls)]
    proc = subprocess.run(cmd, cwd=BASE_DIR, capture_output=True, text=True, check=True)
    return json.loads(proc.stdout)


class TestPredictionParity(unittest.TestCase):

    def test_python_javascript_parity(self):
        """Verify exact vector and prediction equality between Python and JS engines."""
        js_results = run_js_eval(TEST_URL_SUITE)
        self.assertEqual(len(js_results), len(TEST_URL_SUITE))

        print("\n" + "=" * 90)
        print(" PYTHON vs JAVASCRIPT FEATURE AND PREDICTION PARITY REPORT")
        print("=" * 90)
        print(f"{'URL':<42} | {'Py Pred':<10} | {'JS Pred':<10} | {'Vector Match':<12} | Status")
        print("-" * 90)

        all_parity_passed = True
        for i, url in enumerate(TEST_URL_SUITE):
            py_feat = extract_features(url)['vector']
            py_pred = predict_url(url)['prediction']

            js_feat = js_results[i]['vector']
            js_pred = js_results[i]['prediction']

            vector_matches = (py_feat == js_feat)
            pred_matches = (py_pred == js_pred)

            display_url = (url[:39] + '...') if len(url) > 42 else url
            status = "[OK] MATCH" if (vector_matches and pred_matches) else "[!] MISMATCH"
            print(f"{display_url:<42} | {py_pred:<10} | {js_pred:<10} | {str(vector_matches):<12} | {status}")

            self.assertEqual(py_feat, js_feat, f"Vector mismatch for URL: {url}\nPy: {py_feat}\nJS: {js_feat}")
            self.assertEqual(py_pred, js_pred, f"Prediction mismatch for URL: {url}\nPy: {py_pred}\nJS: {js_pred}")

        print("=" * 90)
        print(" 100% PARITY CONFIRMED ACROSS ALL TEST URLS")
        print("=" * 90 + "\n")


if __name__ == '__main__':
    unittest.main()
