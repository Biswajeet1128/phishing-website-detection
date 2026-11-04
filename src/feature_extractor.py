"""
URL Feature Extraction Engine
AI-Based Phishing Website Detection System

Extracts 8 deterministic address-bar features matching the exact
specification and encoding of the UCI Phishing Websites dataset.
"""

import re
from urllib.parse import urlparse

# Exact ordered feature list expected by Model B
URL_FEATURE_NAMES = [
    'having_IP_Address',
    'URL_Length',
    'Shortining_Service',
    'having_At_Symbol',
    'double_slash_redirecting',
    'Prefix_Suffix',
    'having_Sub_Domain',
    'HTTPS_token'
]

# Comprehensive list of recognized URL shortening services
SHORTENING_DOMAINS = {
    'bit.ly', 'tinyurl.com', 'goo.gl', 'ow.ly', 't.co', 'is.gd',
    'buff.ly', 'adf.ly', 'bitly.com', 'rebrand.ly', 'cutt.ly',
    'shorte.st', 'tiny.cc', 'bc.vc', 'qr.ae', 'trib.al', 'cli.gs',
    'v.gd', 'short.gy', 'rb.gy', 'lnkd.in', 'db.tt', 'qr.net',
    '1drv.ms', 'cvatt.es', 'soo.gd', 's2r.co', 'clickmeter.com'
}

# Common multi-part ccTLDs / SLDs to accurately isolate subdomains
COMMON_MULTI_TLDS = {
    'co.uk', 'ac.uk', 'gov.uk', 'org.uk', 'ltd.uk',
    'com.au', 'net.au', 'org.au', 'edu.au', 'gov.au',
    'co.in', 'net.in', 'org.in', 'gen.in', 'firm.in', 'ind.in',
    'nic.in', 'ac.in', 'edu.in', 'res.in', 'gov.in', 'mil.in',
    'co.nz', 'net.nz', 'org.nz', 'govt.nz', 'ac.nz',
    'com.br', 'net.br', 'org.br', 'gov.br', 'edu.br',
    'com.sg', 'edu.sg', 'gov.sg', 'net.sg', 'org.sg',
    'co.za', 'org.za', 'gov.za', 'ac.za',
    'co.jp', 'ne.jp', 'or.jp', 'go.jp', 'ac.jp'
}


def normalize_url(url: str) -> str:
    """Normalize input URL for consistent parsing."""
    if not url:
        return ""
    url = url.strip()
    # If no protocol is provided, default to http:// for parsing purposes
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9+\-.]*://', url):
        url = 'http://' + url
    return url


def get_domain(url: str) -> str:
    """Extract clean domain/host from URL, removing port if present."""
    norm = normalize_url(url)
    try:
        parsed = urlparse(norm)
        host = parsed.netloc.lower()
        # Remove user:pass@ if present in netloc
        if '@' in host:
            host = host.split('@')[-1]
        # Remove port if present
        if ':' in host:
            host = host.split(':')[0]
        return host
    except Exception:
        return ""


def check_ip_address(domain: str) -> int:
    """Check if domain is an IP address (IPv4, Hex IPv4, or IPv6).
    
    UCI Rule:
        If domain has an IP address -> Phishing (-1)
        Otherwise -> Legitimate (1)
    """
    if not domain:
        return 1
        
    # Standard IPv4 dotted decimal
    ipv4_pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    if re.match(ipv4_pattern, domain):
        return -1
        
    # Hexadecimal IP (e.g., 0x58.0xCC.0xCA.0x62)
    hex_pattern = r'^0x[0-9a-fA-F]+(\.0x[0-9a-fA-F]+){3}$'
    if re.match(hex_pattern, domain):
        return -1
        
    # Integer IP representation (e.g., 2130706433 for 127.0.0.1)
    if domain.isdigit():
        return -1
        
    # IPv6 format (standard colons or bracketed)
    clean_domain = domain.strip('[]')
    ipv6_pattern = r'^[0-9a-fA-F]{1,4}(?::[0-9a-fA-F]{1,4}){1,7}$'
    if ':' in clean_domain and (re.match(ipv6_pattern, clean_domain) or clean_domain == '::1'):
        return -1

    return 1


def check_url_length(url: str) -> int:
    """Evaluate URL length.
    
    UCI Rule:
        Length < 54 -> Legitimate (1)
        54 <= Length <= 75 -> Suspicious (0)
        Length > 75 -> Phishing (-1)
    """
    length = len(url)
    if length < 54:
        return 1
    elif 54 <= length <= 75:
        return 0
    else:
        return -1


def check_shortening_service(domain: str) -> int:
    """Check if domain belongs to a known URL shortening service.
    
    UCI Rule:
        Shortening service used -> Phishing (-1)
        Otherwise -> Legitimate (1)
    """
    if not domain:
        return 1
        
    clean_domain = domain.lower()
    if clean_domain.startswith('www.'):
        clean_domain = clean_domain[4:]
        
    if clean_domain in SHORTENING_DOMAINS:
        return -1
        
    for short_svc in SHORTENING_DOMAINS:
        if clean_domain == short_svc or clean_domain.endswith('.' + short_svc):
            return -1
            
    return 1


def check_at_symbol(url: str) -> int:
    """Check presence of '@' symbol in the URL.
    
    UCI Rule:
        '@' present -> Phishing (-1)
        Otherwise -> Legitimate (1)
    """
    return -1 if '@' in url else 1


def check_double_slash_redirect(url: str) -> int:
    """Check for suspicious '//' redirection inside the URL path.
    
    UCI Rule:
        Position of last occurrence of '//' in URL > 7 -> Phishing (-1)
        Otherwise -> Legitimate (1)
    """
    last_double_slash = url.rfind('//')
    # If // appears only at protocol prefix (e.g., http:// at pos 5, https:// at pos 6 or 7)
    if last_double_slash > 7:
        return -1
    return 1


def check_prefix_suffix(domain: str) -> int:
    """Check if domain name contains hyphen '-' prefix/suffix symbol.
    
    UCI Rule:
        Hyphen '-' present in domain part -> Phishing (-1)
        Otherwise -> Legitimate (1)
    """
    return -1 if '-' in domain else 1


def check_sub_domain(domain: str) -> int:
    """Evaluate subdomain count according to UCI specification.
    
    UCI Rule:
        Omit 'www.', remove ccTLD if present.
        Dots == 1 -> Legitimate (1)
        Dots == 2 -> Suspicious (0)
        Dots > 2 -> Phishing (-1)
    """
    if not domain:
        return 1
        
    d = domain.lower()
    if d.startswith('www.'):
        d = d[4:]
        
    # Check and strip multi-part ccTLD (e.g. '.co.uk', '.edu.in')
    for multi_tld in COMMON_MULTI_TLDS:
        if d.endswith('.' + multi_tld):
            # Replace multi_tld with single placeholder to preserve 1 dot for TLD
            d = d[:-(len(multi_tld))] + 'tld'
            break
            
    num_dots = d.count('.')
    
    if num_dots <= 1:
        return 1
    elif num_dots == 2:
        return 0
    else:
        return -1


def check_https_token(domain: str) -> int:
    """Check for deceptive 'http' or 'https' token inside the domain name.
    
    UCI Rule:
        Using HTTP/HTTPS token in domain part -> Phishing (-1)
        Otherwise -> Legitimate (1)
    """
    clean_domain = domain.lower()
    if clean_domain.startswith('www.'):
        clean_domain = clean_domain[4:]
        
    # Check if 'http' or 'https' is part of the domain string (e.g. 'https-paypal.com', 'secure-http.com')
    if 'https' in clean_domain or 'http' in clean_domain:
        return -1
    return 1


def extract_features(url: str) -> dict:
    """Extract all 8 URL-based features for Model B.
    
    Returns:
        dict:
            - 'features': dict mapping feature name to value {-1, 0, 1}
            - 'vector': list of integer feature values in exact URL_FEATURE_NAMES order
            - 'explanations': dict explaining the finding for each feature
    """
    if not url or not isinstance(url, str) or not url.strip():
        # Fallback for empty or invalid input
        empty_features = {f: 1 for f in URL_FEATURE_NAMES}
        return {
            'features': empty_features,
            'vector': [1] * len(URL_FEATURE_NAMES),
            'explanations': {f: "No URL provided / Default safe" for f in URL_FEATURE_NAMES}
        }
        
    norm_url = normalize_url(url)
    domain = get_domain(norm_url)
    
    feat_ip = check_ip_address(domain)
    feat_len = check_url_length(url)
    feat_short = check_shortening_service(domain)
    feat_at = check_at_symbol(url)
    feat_slash = check_double_slash_redirect(url)
    feat_dash = check_prefix_suffix(domain)
    feat_sub = check_sub_domain(domain)
    feat_token = check_https_token(domain)
    
    features = {
        'having_IP_Address': feat_ip,
        'URL_Length': feat_len,
        'Shortining_Service': feat_short,
        'having_At_Symbol': feat_at,
        'double_slash_redirecting': feat_slash,
        'Prefix_Suffix': feat_dash,
        'having_Sub_Domain': feat_sub,
        'HTTPS_token': feat_token
    }
    
    vector = [features[name] for name in URL_FEATURE_NAMES]
    
    explanations = {
        'having_IP_Address': "IP address in hostname" if feat_ip == -1 else "Domain name used",
        'URL_Length': "Long suspicious URL (>75 chars)" if feat_len == -1 else ("Moderate length URL (54-75 chars)" if feat_len == 0 else "Normal short URL (<54 chars)"),
        'Shortining_Service': "Shortening service detected" if feat_short == -1 else "Direct domain (no shortening)",
        'having_At_Symbol': "'@' symbol in URL (credentials trick)" if feat_at == -1 else "No '@' symbol",
        'double_slash_redirecting': "Suspicious '//' redirect in path" if feat_slash == -1 else "Normal '//' scheme usage",
        'Prefix_Suffix': "Hyphen '-' in domain (phishing brand spoofing)" if feat_dash == -1 else "Clean domain without hyphens",
        'having_Sub_Domain': "Multiple suspicious subdomains (>2 dots)" if feat_sub == -1 else ("Single subdomain (suspicious)" if feat_sub == 0 else "Standard domain (<=1 dot)"),
        'HTTPS_token': "Deceptive 'http/https' token in domain name" if feat_token == -1 else "Clean domain protocol naming"
    }
    
    return {
        'features': features,
        'vector': vector,
        'explanations': explanations
    }


if __name__ == '__main__':
    test_urls = [
        "https://www.google.com",
        "http://192.168.1.1/login.html",
        "https://bit.ly/3xY8a",
        "http://user@paypal.com/verify",
        "https://legitimate.org//http://phishingsite.com",
        "https://secure-login-account-update.com",
        "https://secure.banking.portal.login.account.com",
        "http://https-secure-portal.com/login"
    ]
    
    print("Testing URL Feature Extraction Engine...")
    for u in test_urls:
        res = extract_features(u)
        print(f"\nURL: {u}")
        print(f"Vector: {res['vector']}")
        flagged = [k for k, v in res['features'].items() if v == -1]
        print(f"Flagged Phishing Features: {flagged if flagged else 'None (Clean)'}")
