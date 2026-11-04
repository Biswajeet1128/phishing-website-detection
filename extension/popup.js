/**
 * Popup Script for PhishShield AI Chrome Extension
 * AI-Based Phishing Website Detection System
 */

document.addEventListener('DOMContentLoaded', async () => {
  // UI Elements
  const currentUrlText = document.getElementById('currentUrlText');
  const protocolIcon = document.getElementById('protocolIcon');
  const btnCopyUrl = document.getElementById('btnCopyUrl');
  const statusBanner = document.getElementById('statusBanner');
  const statusIconBubble = document.getElementById('statusIconBubble');
  const statusHeading = document.getElementById('statusHeading');
  const statusMessage = document.getElementById('statusMessage');
  const threatLevelText = document.getElementById('threatLevelText');
  const riskScoreText = document.getElementById('riskScoreText');
  const confidenceSubtext = document.getElementById('confidenceSubtext');
  const riskMeterFill = document.getElementById('riskMeterFill');
  const featureFlagsBadge = document.getElementById('featureFlagsBadge');
  const featuresList = document.getElementById('featuresList');
  const manualUrlInput = document.getElementById('manualUrlInput');
  const btnScanManual = document.getElementById('btnScanManual');
  const recText = document.getElementById('recText');

  // Human-readable labels for the 8 features
  const FEATURE_TITLES = {
    'having_IP_Address': 'IP Address Hostname',
    'URL_Length': 'URL Character Length',
    'Shortining_Service': 'URL Shortening Service',
    'having_At_Symbol': 'At Symbol (@) Trick',
    'double_slash_redirecting': 'Path Redirection (//)',
    'Prefix_Suffix': 'Domain Dash Prefix/Suffix',
    'having_Sub_Domain': 'Subdomain Dots Count',
    'HTTPS_token': 'Domain HTTP/HTTPS Token'
  };

  // Initialize Predictor
  let predictor = null;
  try {
    if (typeof MODEL_DATA !== 'undefined') {
      predictor = new PhishingPredictor(MODEL_DATA);
    } else {
      predictor = new PhishingPredictor();
      await predictor.loadModel('model.json');
    }
  } catch (err) {
    console.error("Failed to initialize model:", err);
    renderErrorState("Model Initialization Failed", "Could not load machine learning model parameters.");
    return;
  }

  // Detect current active tab URL
  detectAndScanCurrentTab();

  // Manual Scan Event Listeners
  btnScanManual.addEventListener('click', () => {
    const inputVal = manualUrlInput.value.trim();
    if (inputVal) {
      scanUrl(inputVal, false);
    }
  });

  manualUrlInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      const inputVal = manualUrlInput.value.trim();
      if (inputVal) {
        scanUrl(inputVal, false);
      }
    }
  });

  // Copy URL Event
  btnCopyUrl.addEventListener('click', () => {
    const url = currentUrlText.textContent;
    if (url && url !== 'Detecting active tab...' && !url.startsWith('Error')) {
      navigator.clipboard.writeText(url).then(() => {
        btnCopyUrl.textContent = '✓';
        setTimeout(() => { btnCopyUrl.textContent = '📋'; }, 1500);
      });
    }
  });

  /**
   * Query Chrome active tab
   */
  function detectAndScanCurrentTab() {
    if (typeof chrome !== 'undefined' && chrome.tabs && chrome.tabs.query) {
      chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        if (chrome.runtime.lastError || !tabs || tabs.length === 0) {
          renderUnknownState("about:blank", "No active browser tab found.");
          return;
        }
        const activeTab = tabs[0];
        const tabUrl = activeTab.url || '';
        scanUrl(tabUrl, true);
      });
    } else {
      // Development / Non-extension fallback
      const demoUrl = "https://www.google.com";
      scanUrl(demoUrl, true);
    }
  }

  /**
   * Primary URL scan & evaluation routine
   */
  function scanUrl(url, isCurrentTab = true) {
    if (isCurrentTab) {
      currentUrlText.textContent = url;
      currentUrlText.title = url;
    }

    // Check for internal browser URLs
    const lowerUrl = url.toLowerCase();
    if (lowerUrl.startsWith('chrome://') ||
        lowerUrl.startsWith('chrome-extension://') ||
        lowerUrl.startsWith('edge://') ||
        lowerUrl.startsWith('about:') ||
        lowerUrl.startsWith('view-source:') ||
        lowerUrl.startsWith('devtools://') ||
        lowerUrl.startsWith('file://')) {
      renderUnknownState(url, "Browser internal or local system page. Not an external web target.");
      return;
    }

    if (!url.trim()) {
      renderUnknownState("Empty URL", "Please enter a valid URL to scan.");
      return;
    }

    // Update protocol icon
    if (lowerUrl.startsWith('https://')) {
      protocolIcon.textContent = '🔒';
    } else if (lowerUrl.startsWith('http://')) {
      protocolIcon.textContent = '⚠️';
    } else {
      protocolIcon.textContent = '🌐';
    }

    // 1. Extract 8 URL features
    const extractionResult = URLFeatureExtractor.extractFeatures(url);
    const vector = extractionResult.vector;
    const features = extractionResult.features;
    const explanations = extractionResult.explanations;

    // 2. Perform Machine Learning Inference
    try {
      const predResult = predictor.predictVector(vector);
      renderScanResults(url, predResult, features, explanations);

      // Notify background service worker to record scan
      if (typeof chrome !== 'undefined' && chrome.runtime && chrome.runtime.sendMessage) {
        chrome.runtime.sendMessage({
          action: 'RECORD_SCAN',
          isPhishing: predResult.is_phishing
        });
      }
    } catch (err) {
      console.error("Inference Error:", err);
      renderErrorState("Inference Error", err.message);
    }
  }

  /**
   * Render successful ML evaluation state
   */
  function renderScanResults(url, pred, features, explanations) {
    statusBanner.className = 'status-banner';
    
    // Count flagged indicators
    let flaggedCount = 0;
    for (const k in features) {
      if (features[k] === -1) flaggedCount++;
    }
    featureFlagsBadge.textContent = `${flaggedCount} Flagged`;

    if (pred.is_phishing) {
      // PHISHING STATE
      statusBanner.classList.add('state-phishing');
      statusIconBubble.textContent = '🚨';
      statusHeading.textContent = 'SUSPICIOUS PHISHING URL';
      statusMessage.textContent = 'High probability of phishing or credential spoofing detected by ML model.';

      threatLevelText.textContent = pred.risk_level === 'HIGH' ? 'CRITICAL RISK' : 'MODERATE RISK';
      threatLevelText.style.color = '#f87171';
      riskScoreText.textContent = `${pred.risk_score_percent}%`;
      riskScoreText.style.color = '#f87171';
      riskMeterFill.style.width = `${Math.max(pred.risk_score_percent, 15)}%`;
      riskMeterFill.style.backgroundColor = '#ef4444';

      recText.innerHTML = `<strong>Warning:</strong> Avoid entering passwords, credit card info, or personal details. The URL structure displays deceptive characteristics commonly observed in phishing attacks.`;
    } else {
      // LEGITIMATE STATE
      statusBanner.classList.add('state-legitimate');
      statusIconBubble.textContent = '🛡️';
      statusHeading.textContent = 'LEGITIMATE WEBSITE';
      statusMessage.textContent = 'URL structure adheres to authentic web conventions. No phishing indicators detected.';

      threatLevelText.textContent = 'LOW RISK';
      threatLevelText.style.color = '#34d399';
      riskScoreText.textContent = `${pred.risk_score_percent}%`;
      riskScoreText.style.color = '#34d399';
      riskMeterFill.style.width = `${Math.max(pred.risk_score_percent, 5)}%`;
      riskMeterFill.style.backgroundColor = '#10b981';

      recText.innerHTML = `<strong>Safe:</strong> URL feature analysis indicates standard website structure. Always maintain general cybersecurity caution.`;
    }

    confidenceSubtext.textContent = `Model Confidence: ${pred.confidence_percent}%`;

    // Render Feature Rows
    renderFeatureList(features, explanations);
  }

  /**
   * Render 8 feature rows in detail list
   */
  function renderFeatureList(features, explanations) {
    featuresList.innerHTML = '';
    
    URLFeatureExtractor.URL_FEATURE_NAMES.forEach(featKey => {
      const val = features[featKey];
      const expl = explanations[featKey] || '';
      const title = FEATURE_TITLES[featKey] || featKey;

      const row = document.createElement('div');
      row.className = 'feature-row';

      let badgeClass = 'badge-safe';
      let badgeLabel = 'Safe';
      if (val === -1) {
        badgeClass = 'badge-phish';
        badgeLabel = 'Risk';
      } else if (val === 0) {
        badgeClass = 'badge-suspicious';
        badgeLabel = 'Warning';
      }

      row.innerHTML = `
        <div class="feature-name-group">
          <span class="feature-title">${title}</span>
          <span class="feature-finding" title="${expl}">${expl}</span>
        </div>
        <span class="feature-badge ${badgeClass}">${badgeLabel}</span>
      `;

      featuresList.appendChild(row);
    });
  }

  /**
   * Render Unknown / Internal Browser State
   */
  function renderUnknownState(url, message) {
    statusBanner.className = 'status-banner state-unknown';
    statusIconBubble.textContent = '⚙️';
    statusHeading.textContent = 'INTERNAL BROWSER URL';
    statusMessage.textContent = message;

    protocolIcon.textContent = '⚙️';
    threatLevelText.textContent = 'N/A';
    threatLevelText.style.color = '#a5b4fc';
    riskScoreText.textContent = '--';
    riskScoreText.style.color = '#a5b4fc';
    riskMeterFill.style.width = '0%';
    confidenceSubtext.textContent = 'Model: Skipped';
    featureFlagsBadge.textContent = '0 Flagged';

    featuresList.innerHTML = `
      <div style="padding: 12px; text-align: center; color: #94a3b8; font-size: 11px;">
        Chrome internal URLs (chrome://, about:, extensions) reside locally inside the browser engine and do not represent external web domains.
      </div>
    `;

    recText.textContent = 'Internal browser pages are maintained by your browser and do not carry external web phishing risks.';
  }

  /**
   * Render Error State
   */
  function renderErrorState(title, message) {
    statusBanner.className = 'status-banner state-unknown';
    statusIconBubble.textContent = '⚠️';
    statusHeading.textContent = title;
    statusMessage.textContent = message;
    threatLevelText.textContent = 'ERROR';
    riskScoreText.textContent = '--';
    riskMeterFill.style.width = '0%';
  }
});
