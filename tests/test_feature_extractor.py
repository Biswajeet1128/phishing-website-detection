"""
Unit Tests for URL Feature Extraction Engine
AI-Based Phishing Website Detection System
"""

import unittest
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.feature_extractor import (
    extract_features,
    check_ip_address,
    check_url_length,
    check_shortening_service,
    check_at_symbol,
    check_double_slash_redirect,
    check_prefix_suffix,
    check_sub_domain,
    check_https_token,
    get_domain,
    URL_FEATURE_NAMES
)


class TestURLFeatureExtractor(unittest.TestCase):

    def test_feature_names_order(self):
        """Ensure feature names and count match exactly 8 features."""
        self.assertEqual(len(URL_FEATURE_NAMES), 8)
        expected = [
            'having_IP_Address', 'URL_Length', 'Shortining_Service',
            'having_At_Symbol', 'double_slash_redirecting', 'Prefix_Suffix',
            'having_Sub_Domain', 'HTTPS_token'
        ]
        self.assertEqual(URL_FEATURE_NAMES, expected)

    def test_clean_legitimate_url(self):
        """A standard legitimate URL should have clean features (all +1)."""
        url = "https://www.google.com"
        res = extract_features(url)
        self.assertEqual(res['vector'], [1, 1, 1, 1, 1, 1, 1, 1])
        for k, v in res['features'].items():
            self.assertEqual(v, 1, f"Feature {k} was unexpectedly flagged for {url}")

    def test_ip_address_detection(self):
        """IP address in host must return -1 for having_IP_Address."""
        ip_urls = [
            "http://192.168.1.1/index.html",
            "http://125.98.3.123/fake.html",
            "http://0x58.0xCC.0xCA.0x62/paypal.ca/index.html",
            "http://2130706433/login"
        ]
        for u in ip_urls:
            domain = get_domain(u)
            self.assertEqual(check_ip_address(domain), -1, f"Failed to detect IP for {u}")

    def test_url_length_bins(self):
        """Test UCI length thresholds: <54 -> 1, 54-75 -> 0, >75 -> -1."""
        short_url = "https://example.com/login"  # length 25
        self.assertEqual(check_url_length(short_url), 1)

        mod_url = "https://example.com/" + "a" * 40  # length 60
        self.assertEqual(check_url_length(mod_url), 0)

        long_url = "https://example.com/" + "a" * 80  # length 100
        self.assertEqual(check_url_length(long_url), -1)

    def test_shortening_services(self):
        """Known URL shortening services should be flagged -1."""
        short_urls = [
            "https://bit.ly/3xY8a",
            "https://tinyurl.com/banklogin",
            "http://goo.gl/xyz12",
            "https://t.co/abc89"
        ]
        for u in short_urls:
            domain = get_domain(u)
            self.assertEqual(check_shortening_service(domain), -1, f"Failed shortening test for {u}")

    def test_at_symbol(self):
        """Presence of @ symbol should return -1."""
        url_with_at = "http://username:secret@paypal.com/login"
        self.assertEqual(check_at_symbol(url_with_at), -1)
        clean_url = "https://paypal.com/login"
        self.assertEqual(check_at_symbol(clean_url), 1)

    def test_double_slash_redirect(self):
        """Double slash occurring after index 7 should return -1."""
        redirect_url = "https://legitimate.com//http://phish.com"
        self.assertEqual(check_double_slash_redirect(redirect_url), -1)
        clean_url = "https://legitimate.com/search?q=test"
        self.assertEqual(check_double_slash_redirect(clean_url), 1)

    def test_prefix_suffix_hyphen(self):
        """Hyphen in domain name should return -1."""
        dash_domain = "https://secure-login-paypal.com"
        domain = get_domain(dash_domain)
        self.assertEqual(check_prefix_suffix(domain), -1)

        clean_domain = "https://paypal.com"
        domain_clean = get_domain(clean_domain)
        self.assertEqual(check_prefix_suffix(domain_clean), 1)

    def test_subdomain_counting(self):
        """Single domain (1 dot) -> 1, 1 subdomain (2 dots) -> 0, multiple (>2) -> -1."""
        domain_1 = "google.com"
        self.assertEqual(check_sub_domain(domain_1), 1)

        domain_2 = "mail.google.com"
        self.assertEqual(check_sub_domain(domain_2), 0)

        domain_multi = "secure.login.banking.portal.com"
        self.assertEqual(check_sub_domain(domain_multi), -1)

        # Multi-part ccTLD handling (e.g. hud.ac.uk -> should count as legitimate 1 dot domain)
        domain_cctld = "hud.ac.uk"
        self.assertEqual(check_sub_domain(domain_cctld), 1)

    def test_https_token_in_domain(self):
        """Deceptive 'http' or 'https' in domain part should return -1."""
        deceptive_domain = "http://https-secure-account-verification.com"
        domain = get_domain(deceptive_domain)
        self.assertEqual(check_https_token(domain), -1)

        normal_domain = "https://example.com"
        domain_normal = get_domain(normal_domain)
        self.assertEqual(check_https_token(domain_normal), 1)

    def test_empty_and_malformed_url(self):
        """Extractor should handle empty strings and malformed input gracefully."""
        res_empty = extract_features("")
        self.assertEqual(len(res_empty['vector']), 8)
        self.assertEqual(res_empty['vector'], [1] * 8)

        res_none = extract_features(None)
        self.assertEqual(res_none['vector'], [1] * 8)


if __name__ == '__main__':
    unittest.main()
