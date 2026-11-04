/**
 * Client-Side JavaScript Machine Learning Inference Engine
 * AI-Based Phishing Website Detection System
 * 
 * Executes local tree-based inference on URL feature vectors
 * without network calls, dependencies, or external libraries.
 */

class PhishingPredictor {
  constructor(modelData = null) {
    this.model = modelData;
  }

  /**
   * Load model from JSON file path or URL
   */
  async loadModel(url = 'model.json') {
    if (typeof fetch !== 'undefined') {
      try {
        const response = await fetch(url);
        this.model = await response.json();
        return this.model;
      } catch (err) {
        console.warn("Failed to fetch model.json, checking for fallback MODEL_DATA", err);
      }
    }
    
    // Check fallback global MODEL_DATA
    if (typeof MODEL_DATA !== 'undefined') {
      this.model = MODEL_DATA;
      return this.model;
    }

    // Node.js environment fallback
    if (typeof require !== 'undefined') {
      try {
        this.model = require('./model.json');
        return this.model;
      } catch (e) {
        // Handled by caller
      }
    }

    throw new Error("Unable to load model data.");
  }

  /**
   * Recursively traverse Decision Tree node
   */
  _traverseTree(node, vector) {
    if (node.is_leaf) {
      const phishProb = node.probabilities ? node.probabilities[1] : (node.predicted_class === 1 ? 1.0 : 0.0);
      const legitProb = node.probabilities ? node.probabilities[0] : (node.predicted_class === 0 ? 1.0 : 0.0);
      return {
        predicted_class: node.predicted_class,
        label: node.predicted_label || (node.predicted_class === 1 ? 'Phishing' : 'Legitimate'),
        probabilities: [legitProb, phishProb],
        phishing_probability: phishProb,
        confidence: Math.max(legitProb, phishProb)
      };
    }

    const featVal = vector[node.feature_index];
    if (featVal <= node.threshold) {
      return this._traverseTree(node.left, vector);
    } else {
      return this._traverseTree(node.right, vector);
    }
  }

  /**
   * Evaluate a Random Forest ensemble if provided
   */
  _evaluateForest(forest, vector) {
    let totalPhishProb = 0.0;
    const treeCount = forest.trees.length;

    for (const treeItem of forest.trees) {
      const treeRes = this._traverseTree(treeItem.root, vector);
      totalPhishProb += treeRes.phishing_probability;
    }

    const avgPhishProb = totalPhishProb / treeCount;
    const avgLegitProb = 1.0 - avgPhishProb;
    const predClass = avgPhishProb >= (forest.threshold || 0.5) ? 1 : 0;

    return {
      predicted_class: predClass,
      label: predClass === 1 ? 'Phishing' : 'Legitimate',
      probabilities: [avgLegitProb, avgPhishProb],
      phishing_probability: avgPhishProb,
      confidence: Math.max(avgLegitProb, avgPhishProb)
    };
  }

  /**
   * Run inference on an 8-element feature vector
   * vector order: [having_IP_Address, URL_Length, Shortining_Service, having_At_Symbol,
   *                double_slash_redirecting, Prefix_Suffix, having_Sub_Domain, HTTPS_token]
   */
  predictVector(vector) {
    if (!this.model) {
      if (typeof MODEL_DATA !== 'undefined') {
        this.model = MODEL_DATA;
      } else {
        throw new Error("Model is not initialized. Call loadModel() first.");
      }
    }

    if (!Array.isArray(vector) || vector.length !== 8) {
      throw new Error(`Expected feature vector of length 8, got ${vector ? vector.length : 'none'}`);
    }

    let result;
    if (this.model.model_type === 'RandomForestClassifier' && this.model.trees) {
      result = this._evaluateForest(this.model, vector);
    } else if (this.model.tree) {
      result = this._traverseTree(this.model.tree, vector);
    } else {
      throw new Error("Invalid model format: missing tree structure.");
    }

    // Risk assessment logic based on phishing probability and heuristic triggers
    const phishProb = result.phishing_probability;
    const isPhishing = result.predicted_class === 1;

    let riskLevel = 'LOW';
    if (phishProb >= 0.70) {
      riskLevel = 'HIGH';
    } else if (phishProb >= 0.45) {
      riskLevel = 'MODERATE';
    }

    return {
      is_phishing: isPhishing,
      label: isPhishing ? 'Phishing' : 'Legitimate',
      risk_level: riskLevel,
      risk_score_percent: Math.round(phishProb * 100),
      confidence_percent: Math.round(result.confidence * 100),
      probabilities: result.probabilities,
      model_track: this.model.track || 'Model B'
    };
  }
}

// Module export for Node.js testing and browser window global
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { PhishingPredictor };
} else if (typeof window !== 'undefined') {
  window.PhishingPredictor = PhishingPredictor;
}
