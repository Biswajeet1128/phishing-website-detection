/**
 * URL Feature Extraction Engine (JavaScript / Chrome Extension Manifest V3)
 * AI-Based Phishing Website Detection System
 * 
 * Extracts 8 deterministic URL-based features mirroring src/feature_extractor.py
 * to guarantee 100% parity between Python and Chrome Extension runtime.
 */

const URL_FEATURE_NAMES = [
  'having_IP_Address',
  'URL_Length',
  'Shortining_Service',
  'having_At_Symbol',
  'double_slash_redirecting',
  'Prefix_Suffix',
  'having_Sub_Domain',
  'HTTPS_token'
];

const SHORTENING_DOMAINS = new Set([
  'bit.ly', 'tinyurl.com', 'goo.gl', 'ow.ly', 't.co', 'is.gd',
  'buff.ly', 'adf.ly', 'bitly.com', 'rebrand.ly', 'cutt.ly',
  'shorte.st', 'tiny.cc', 'bc.vc', 'qr.ae', 'trib.al', 'cli.gs',
  'v.gd', 'short.gy', 'rb.gy', 'lnkd.in', 'db.tt', 'qr.net',
  '1drv.ms', 'cvatt.es', 'soo.gd', 's2r.co', 'clickmeter.com'
]);

const COMMON_MULTI_TLDS = [
  'co.uk', 'ac.uk', 'gov.uk', 'org.uk', 'ltd.uk',
  'com.au', 'net.au', 'org.au', 'edu.au', 'gov.au',
  'co.in', 'net.in', 'org.in', 'gen.in', 'firm.in', 'ind.in',
  'nic.in', 'ac.in', 'edu.in', 'res.in', 'gov.in', 'mil.in',
  'co.nz', 'net.nz', 'org.nz', 'govt.nz', 'ac.nz',
  'com.br', 'net.br', 'org.br', 'gov.br', 'edu.br',
  'com.sg', 'edu.sg', 'gov.sg', 'net.sg', 'org.sg',
  'co.za', 'org.za', 'gov.za', 'ac.za',
  'co.jp', 'ne.jp', 'or.jp', 'go.jp', 'ac.jp'
];

/**
 * Normalize URL string to ensure valid protocol for parsing
 */
function normalizeUrl(url) {
  if (!url || typeof url !== 'string') return '';
  url = url.trim();
  if (!/^[a-zA-Z][a-zA-Z0-9+\-.]*:\/\//.test(url)) {
    url = 'http://' + url;
  }
  return url;
}

/**
 * Extract clean hostname / domain from URL
 */
function getDomain(url) {
  const norm = normalizeUrl(url);
  try {
    const parsed = new URL(norm);
    let host = parsed.hostname.toLowerCase();
    if (host.includes('@')) {
      host = host.split('@').pop();
    }
    return host;
  } catch (e) {
    // Fallback regex if standard URL parser fails on malformed input
    const match = norm.match(/^[a-zA-Z]+:\/\/([^/?#:]+)/);
    return match ? match[1].toLowerCase() : '';
  }
}

/**
 * 1. having_IP_Address: Checks for IPv4, Hex IP, or IPv6 in domain
 * UCI: Phishing (-1), Legitimate (1)
 */
function checkIpAddress(domain) {
  if (!domain) return 1;

  // Dotted decimal IPv4 (0-255)
  const ipv4Pattern = /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
  if (ipv4Pattern.test(domain)) return -1;

  // Hexadecimal IP (0x..)
  const hexPattern = /^0x[0-9a-fA-F]+(\.0x[0-9a-fA-F]+){3}$/;
  if (hexPattern.test(domain)) return -1;

  // Pure integer decimal IP
  if (/^\d+$/.test(domain)) return -1;

  // IPv6 check
  const clean = domain.replace(/^\[|\]$/g, '');
  const ipv6Pattern = /^[0-9a-fA-F]{1,4}(?::[0-9a-fA-F]{1,4}){1,7}$/;
  if (clean.includes(':') && (ipv6Pattern.test(clean) || clean === '::1')) {
    return -1;
  }

  return 1;
}

/**
 * 2. URL_Length: Length of full URL string
 * UCI: < 54 -> Legitimate (1), 54-75 -> Suspicious (0), > 75 -> Phishing (-1)
 */
function checkUrlLength(url) {
  const len = url.length;
  if (len < 54) return 1;
  if (len <= 75) return 0;
  return -1;
}

/**
 * 3. Shortining_Service: Check if domain is a known URL shortening service
 * UCI: Phishing (-1), Legitimate (1)
 */
function checkShorteningService(domain) {
  if (!domain) return 1;
  let clean = domain.toLowerCase();
  if (clean.startsWith('www.')) {
    clean = clean.slice(4);
  }
  if (SHORTENING_DOMAINS.has(clean)) return -1;

  for (const svc of SHORTENING_DOMAINS) {
    if (clean === svc || clean.endsWith('.' + svc)) {
      return -1;
    }
  }
  return 1;
}

/**
 * 4. having_At_Symbol: Check presence of '@' in URL
 * UCI: Phishing (-1), Legitimate (1)
 */
function checkAtSymbol(url) {
  return url.includes('@') ? -1 : 1;
}

/**
 * 5. double_slash_redirecting: Check if last '//' index > 7
 * UCI: Phishing (-1), Legitimate (1)
 */
function checkDoubleSlashRedirect(url) {
  const lastIdx = url.lastIndexOf('//');
  return lastIdx > 7 ? -1 : 1;
}

/**
 * 6. Prefix_Suffix: Check for '-' symbol in domain part
 * UCI: Phishing (-1), Legitimate (1)
 */
function checkPrefixSuffix(domain) {
  return domain.includes('-') ? -1 : 1;
}

/**
 * 7. having_Sub_Domain: Count dots after stripping 'www.' and ccTLD
 * UCI: 1 dot -> Legitimate (1), 2 dots -> Suspicious (0), > 2 dots -> Phishing (-1)
 */
function checkSubDomain(domain) {
  if (!domain) return 1;
  let d = domain.toLowerCase();
  if (d.startsWith('www.')) {
    d = d.slice(4);
  }

  for (const multiTld of COMMON_MULTI_TLDS) {
    if (d.endsWith('.' + multiTld)) {
      d = d.slice(0, -(multiTld.length)) + 'tld';
      break;
    }
  }

  const dotCount = (d.match(/\./g) || []).length;
  if (dotCount <= 1) return 1;
  if (dotCount === 2) return 0;
  return -1;
}

/**
 * 8. HTTPS_token: Check for deceptive 'http' or 'https' in domain
 * UCI: Phishing (-1), Legitimate (1)
 */
function checkHttpsToken(domain) {
  let clean = domain.toLowerCase();
  if (clean.startsWith('www.')) {
    clean = clean.slice(4);
  }
  if (clean.includes('https') || clean.includes('http')) {
    return -1;
  }
  return 1;
}

/**
 * Main feature extraction routine
 */
function extractFeatures(url) {
  if (!url || typeof url !== 'string' || !url.trim()) {
    const emptyFeatures = {};
    URL_FEATURE_NAMES.forEach(f => { emptyFeatures[f] = 1; });
    return {
      features: emptyFeatures,
      vector: new Array(URL_FEATURE_NAMES.length).fill(1),
      explanations: {}
    };
  }

  const norm = normalizeUrl(url);
  const domain = getDomain(norm);

  const featIp = checkIpAddress(domain);
  const featLen = checkUrlLength(url);
  const featShort = checkShorteningService(domain);
  const featAt = checkAtSymbol(url);
  const featSlash = checkDoubleSlashRedirect(url);
  const featDash = checkPrefixSuffix(domain);
  const featSub = checkSubDomain(domain);
  const featToken = checkHttpsToken(domain);

  const features = {
    having_IP_Address: featIp,
    URL_Length: featLen,
    Shortining_Service: featShort,
    having_At_Symbol: featAt,
    double_slash_redirecting: featSlash,
    Prefix_Suffix: featDash,
    having_Sub_Domain: featSub,
    HTTPS_token: featToken
  };

  const vector = URL_FEATURE_NAMES.map(name => features[name]);

  const explanations = {
    having_IP_Address: featIp === -1 ? "IP address in hostname" : "Domain name used",
    URL_Length: featLen === -1 ? "Long suspicious URL (>75 chars)" : (featLen === 0 ? "Moderate length URL (54-75 chars)" : "Normal short URL (<54 chars)"),
    Shortining_Service: featShort === -1 ? "Shortening service detected" : "Direct domain (no shortening)",
    having_At_Symbol: featAt === -1 ? "'@' symbol in URL (credentials trick)" : "No '@' symbol",
    double_slash_redirecting: featSlash === -1 ? "Suspicious '//' redirect in path" : "Normal '//' scheme usage",
    Prefix_Suffix: featDash === -1 ? "Hyphen '-' in domain (phishing brand spoofing)" : "Clean domain without hyphens",
    having_Sub_Domain: featSub === -1 ? "Multiple suspicious subdomains (>2 dots)" : (featSub === 0 ? "Single subdomain (suspicious)" : "Standard domain (<=1 dot)"),
    HTTPS_token: featToken === -1 ? "Deceptive 'http/https' token in domain name" : "Clean domain protocol naming"
  };

  return {
    features,
    vector,
    explanations
  };
}

// Module export for Node.js unit testing and browser window global
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    URL_FEATURE_NAMES,
    extractFeatures,
    normalizeUrl,
    getDomain,
    checkIpAddress,
    checkUrlLength,
    checkShorteningService,
    checkAtSymbol,
    checkDoubleSlashRedirect,
    checkPrefixSuffix,
    checkSubDomain,
    checkHttpsToken
  };
} else if (typeof window !== 'undefined') {
  window.URLFeatureExtractor = {
    URL_FEATURE_NAMES,
    extractFeatures
  };
}
