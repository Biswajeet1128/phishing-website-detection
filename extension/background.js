/**
 * Background Service Worker (Manifest V3)
 * AI-Based Phishing Website Detection System
 */

chrome.runtime.onInstalled.addListener((details) => {
  console.log(`[PhishShield AI] Extension installed successfully. Reason: ${details.reason}`);
  // Initialize storage defaults if needed
  chrome.storage.local.set({
    extensionEnabled: true,
    scanCount: 0,
    threatsDetected: 0
  });
});

// Listener for messages from popup or content scripts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'PING') {
    sendResponse({ status: 'PONG', timestamp: Date.now() });
  } else if (request.action === 'RECORD_SCAN') {
    chrome.storage.local.get(['scanCount', 'threatsDetected'], (data) => {
      const scans = (data.scanCount || 0) + 1;
      const threats = (data.threatsDetected || 0) + (request.isPhishing ? 1 : 0);
      chrome.storage.local.set({ scanCount: scans, threatsDetected: threats });
      sendResponse({ success: true, scanCount: scans, threatsDetected: threats });
    });
    return true; // Keep message channel open for async response
  }
});
