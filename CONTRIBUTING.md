# Contributing to PhishShield AI

Thank you for your interest in contributing to **PhishShield AI** (AI-Based Phishing Website Detection System)! Open-source contributions from developers, machine learning researchers, and cybersecurity students are welcome.

---

## 📌 Code of Conduct

We are committed to providing a welcoming, inclusive, and harassment-free environment. Please treat all contributors with respect and professionalism.

---

## 🛠️ How to Contribute

### 1. Reporting Issues or Bugs
If you find a bug, inaccurate feature rule, or broken link:
1. Search the [Issues tab](https://github.com/Biswajeet1128/phishing-website-detection/issues) to ensure it hasn't already been reported.
2. If new, open an issue detailing:
   - Operating system and browser version (e.g., Chrome v125, Windows 11).
   - Expected behavior vs. actual behavior.
   - Minimal reproducible example URL or code snippet.

### 2. Suggesting Enhancements
Feature requests are welcome! Examples of valuable contributions:
- Adding support for Firefox or Edge Web Extensions.
- Implementing Internationalized Domain Name (IDN) homoglyph detection.
- Adding additional lexical URL features (e.g., Shannon entropy of domain).
- Expanding the test suite with new zero-day URL patterns.

### 3. Submitting Pull Requests

1. **Fork the Repository**:
   Click the **Fork** button on GitHub.

2. **Clone your Fork locally**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/phishing-website-detection.git
   cd phishing-website-detection
   ```

3. **Create a Feature Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Set Up Development Environment**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux / macOS:
   source venv/bin/activate

   pip install -r requirements.txt
   ```

5. **Run the Automated Test Suite**:
   Ensure all tests pass before making changes:
   ```bash
   python -m unittest discover tests
   ```

6. **Implement your Changes**:
   - Maintain parity: If modifying URL feature logic in Python (`src/feature_extractor.py`), update the corresponding JavaScript module (`extension/feature_extractor.js`) to preserve 100% parity.
   - Follow PEP 8 guidelines for Python code.
   - Write unit tests for any new features or bug fixes.

7. **Verify Parity Tests**:
   ```bash
   python -m unittest tests/test_prediction_parity.py
   ```

8. **Commit and Push**:
   ```bash
   git add .
   git commit -m "feat: Add Shannon entropy feature to URL extraction"
   git push origin feature/your-feature-name
   ```

9. **Open a Pull Request**:
   Navigate to the main repository and submit a PR from your feature branch with a clear description of the modifications.

---

## ⚖️ License

By contributing to this repository, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).
