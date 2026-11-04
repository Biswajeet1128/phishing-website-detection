# B.Tech MLDA Laboratory Viva Preparation Guide
## AI-Based Phishing Website Detection System with Chrome Browser Extension
### 40 Comprehensive Questions & Answers for B.Tech CSE Viva / Oral Examination

---

### Category 1: Cybersecurity & Phishing Fundamentals

#### Q1. What is phishing, and how does it differ from other cyber attacks?
**Answer:**  
Phishing is a form of social engineering and cyber attack where adversaries craft deceptive electronic communications or clone legitimate websites to trick users into divulging sensitive information such as usernames, passwords, credit card numbers, and session tokens. Unlike malware or network intrusions that exploit software vulnerabilities, phishing exploits human cognitive vulnerabilities—primarily trust, urgency, and visual similarity.

#### Q2. What are the limitations of traditional blacklist-based phishing detection methods?
**Answer:**  
Traditional blacklist engines (such as Google Safe Browsing, PhishTank, and Spamhaus) rely on manual reporting, crawling, and human verification before adding malicious domains to a central database. Their major limitations include:
1. **Zero-Hour Phishing Blindspot**: High-volume modern phishing campaigns use disposable, algorithmically generated domains (DGA) that remain active for only 4 to 8 hours, rendering static blacklists ineffective during the attack window.
2. **High Latency**: The turnaround time between phishing domain emergence and blacklist registration is often hours or days.
3. **Database Bloat**: Maintaining lists of millions of inactive or ephemeral domains creates significant infrastructure overhead.

#### Q3. Why is Machine Learning suitable for phishing URL detection?
**Answer:**  
Machine Learning algorithms generalize statistical and structural patterns inherent in fraudulent URLs (e.g., abnormally long paths, abnormal subdomain nesting, brand-spoofing hyphens, and URL shortening redirects). Instead of querying an external database of previously seen URLs, an ML model predicts the maliciousness of completely unseen (zero-day) URLs based on extracted feature vectors in real time.

---

### Category 2: Machine Learning & Classification Concepts

#### Q4. What type of Machine Learning problem is phishing website detection?
**Answer:**  
It is a **Supervised Binary Classification** problem. The target label $Y \in \{0, 1\}$ represents the ground-truth status where $0$ indicates a Legitimate website and $1$ indicates a Phishing website. The feature vector $\mathbf{x} = [x_1, x_2, \dots, x_d]$ represents extracted structural and lexical URL characteristics.

#### Q5. What is the difference between supervised and unsupervised learning in this context?
**Answer:**  
In supervised learning, algorithms learn a mapping function $f: \mathbf{x} \to y$ from labeled historical datasets containing known legitimate and phishing examples. In unsupervised learning (such as k-means or isolation forests), algorithms attempt to detect anomalies without class labels. Phishing detection primarily uses supervised learning because high-quality labeled ground-truth datasets exist.

#### Q6. What is the Curse of Dimensionality, and how does it relate to our project?
**Answer:**  
The Curse of Dimensionality refers to the phenomenon where the volume of the feature space increases exponentially with the number of dimensions, requiring exponentially more data for statistical significance and increasing risk of overfitting. In our project, reducing the feature space from 30 features (Model A) to 8 address-bar URL features (Model B) minimized computational complexity, avoided external network dependencies, and enabled ultra-fast inference on constrained client devices.

---

### Category 3: The Two-Model Strategy

#### Q7. Explain the "Two-Model Strategy" implemented in this project.
**Answer:**  
The UCI Phishing Websites dataset contains 30 pre-extracted features:
- **Model A (Full Dataset Benchmark)**: Employs all 30 features (including external DNS, WHOIS domain expiration, SSL certificate issuer, and webpage DOM features such as iframe tags and anchor ratios). It serves as an academic benchmark of classification algorithms.
- **Model B (Real-Time URL Detection)**: Employs strictly the 8 address-bar features that can be extracted instantly from the URL string itself without requesting the target webpage, conducting port scans, or querying paid external APIs. Model B is the actual model deployed inside the Chrome Extension.

#### Q8. Why can't we deploy Model A inside the Chrome Browser Extension?
**Answer:**  
Model A requires:
1. Remote DNS and WHOIS registry lookups (e.g., `DNSRecord`, `age_of_domain`, `Domain_registeration_length`).
2. Server port scanning (e.g., testing open FTP/SSH ports).
3. Full webpage HTML download and DOM parsing (e.g., scanning `<script>`, `<iframe>`, and anchor URLs).  
Executing these checks on every visited website causes significant browsing latency, consumes excessive bandwidth, violates Chrome Web Store privacy guidelines, and creates a severe security risk by downloading malicious payload scripts just to inspect them. Model B analyzes the URL string locally before the web page is even rendered.

#### Q9. Why does Model A achieve higher accuracy (~97.6%) than Model B (~73.1%)?
**Answer:**  
Model A incorporates rich contextual signals from inside the webpage DOM (such as `URL_of_Anchor`, `SSLfinal_State`, and `web_traffic`), which provide high discriminant power for distinguishing authentic websites from clones. Model B is constrained purely to lexical features of the URL address bar. While Model B sacrifices some accuracy, it achieves sub-millisecond on-device execution, zero data leakage, and complete operational independence from external network services.

---

### Category 4: Algorithms Used

#### Q10. How does a Decision Tree work for classification?
**Answer:**  
A Decision Tree builds a hierarchical flowchart of binary decisions. Starting at the root node, it evaluates feature values against calculated thresholds and splits the training samples into left and right branches to maximize class purity (minimizing impurity). At prediction time, a sample traverses nodes down to a leaf node, which assigns the predicted class based on the majority vote of the training samples within that leaf.

#### Q11. What impurity criteria did you evaluate for the Decision Tree, and what is the difference between Gini Impurity and Entropy?
**Answer:**  
We evaluated both **Gini Impurity** and **Entropy**:
- **Gini Impurity**: $I_G(p) = 1 - \sum_{i=1}^{C} p_i^2$, measuring the probability of a randomly chosen element being incorrectly classified.
- **Entropy (Information Gain)**: $H(p) = -\sum_{i=1}^{C} p_i \log_2(p_i)$, measuring the disorder or uncertainty in information theory.  
For our dataset, Entropy with `max_depth=6` produced a slightly higher F1-score (0.7247 vs 0.7180) on Model B.

#### Q12. How does Random Forest improve upon a single Decision Tree?
**Answer:**  
Random Forest is an ensemble learning method based on **Bagging (Bootstrap Aggregating)**:
1. It trains an ensemble of $N$ diverse decision trees, each fitted on a random bootstrap sample with replacement from the training set.
2. At each node split, it evaluates a random subset of features (feature bagging) rather than all features, which decorrelates the trees.
3. The final prediction is aggregate majority voting (or average predicted probability) across all individual trees.  
This drastically reduces model variance and prevents overfitting compared to a single deep decision tree.

#### Q13. How does Naive Bayes work, and what is the "naive" assumption?
**Answer:**  
Naive Bayes applies Bayes' Theorem:
$$P(Y|X) = \frac{P(X|Y) P(Y)}{P(X)}$$
The "naive" assumption is that **all features are conditionally independent given the class label**:
$$P(x_1, x_2, \dots, x_d | Y) = \prod_{i=1}^{d} P(x_i | Y)$$
While this assumption rarely holds strictly in real-world correlated data, Naive Bayes often performs surprisingly well as a fast baseline classifier.

#### Q14. What is the difference between Gaussian Naive Bayes and Categorical Naive Bayes?
**Answer:**  
- **Gaussian Naive Bayes (GNB)** assumes continuous features distributed according to a normal (Gaussian) distribution: $P(x_i | Y) \sim \mathcal{N}(\mu, \sigma^2)$.
- **Categorical Naive Bayes (CNB)** calculates discrete categorical likelihoods $P(x_i = c | Y)$ based on categorical frequency tables with Laplace smoothing.  
Because the UCI dataset features are discrete categorical values $\{-1, 0, 1\}$, Gaussian NB fits inappropriate continuous bells over discrete points, leading to skewed class probabilities (58.5% accuracy). Categorical NB respects the discrete categories and achieved 72.9% accuracy on Model B and 93.3% on Model A.

#### Q15. Why did you include Logistic Regression in your comparisons?
**Answer:**  
Logistic Regression serves as the standard linear baseline for binary classification. It models the log-odds of the positive class as a linear combination of features through the sigmoid activation function $\sigma(z) = \frac{1}{1 + e^{-z}}$. Comparing decision tree non-linear partitions against logistic regression linear hyperplanes confirms whether non-linear feature interactions exist in the dataset.

---

### Category 5: Feature Engineering & Extraction

#### Q16. Name the 8 features used in Model B.
**Answer:**  
1. `having_IP_Address`: Presence of IPv4, hex IP, or IPv6 in hostname.
2. `URL_Length`: Length of URL string (<54 legit, 54-75 suspicious, >75 phishing).
3. `Shortining_Service`: Detection of URL shorteners (bit.ly, tinyurl, etc.).
4. `having_At_Symbol`: Presence of `@` symbol in the URL.
5. `double_slash_redirecting`: Position of last `//` occurring after index 7.
6. `Prefix_Suffix`: Presence of hyphen `-` in domain name.
7. `having_Sub_Domain`: Subdomain dots count (omitting `www.` and ccTLDs).
8. `HTTPS_token`: Embedding `http` or `https` tokens inside domain labels.

#### Q17. How does the `having_IP_Address` rule work?
**Answer:**  
Legitimate companies register branded alphanumeric domain names (e.g., `google.com`, `paypal.com`). Phishers often deploy fraudulent login scripts directly on raw IP addresses or compromised hosting servers without purchasing domains, or use hexadecimal representations (e.g., `http://0x58.0xCC...`) to bypass basic URL string filters. If an IP address is detected in the hostname, the feature returns `-1` (Phishing); otherwise, `+1` (Legitimate).

#### Q18. Why is the `@` symbol considered a phishing indicator in URLs?
**Answer:**  
In the URI specification (RFC 3986), characters before `@` designate userinfo (authentication credentials):
`http://legitimate-bank.com@malicious-phishing.com/login`  
Web browsers ignore everything before the `@` symbol and route the connection strictly to the domain *following* the `@` symbol. Phishers use this trick to deceive users who only look at the first few words of the URL.

#### Q19. How does `double_slash_redirecting` work?
**Answer:**  
The protocol scheme of a URL uses `//` (e.g., `http://` at position 5 or 6, `https://` at position 6 or 7). If an additional `//` appears later in the path (e.g., `http://legitimate.org//http://phishing.com`), the last occurrence index is $> 7$. This pattern is commonly used in open-redirect exploits and phishing redirect chains.

#### Q20. How did you handle country-code top-level domains (ccTLDs) like `.co.uk` when counting subdomains?
**Answer:**  
A domain like `hud.ac.uk` has two dots, but `ac.uk` is a single multi-part second-level domain (SLD/ccTLD) and `hud` is the actual domain name—meaning it has zero subdomains. If we simply counted dots without normalization, legitimate international websites would be falsely classified as suspicious. Our feature extractor strips known multi-part ccTLDs (`.co.uk`, `.edu.in`, `.com.au`, etc.) and the `www.` prefix before evaluating dot counts.

---

### Category 6: Data Preprocessing & Validation

#### Q21. How were the target labels mapped for Machine Learning?
**Answer:**  
The original UCI dataset encoded the target `Result` as:
- `+1`: Legitimate
- `-1`: Phishing  
For standard Scikit-learn binary classification, we mapped:
- `Phishing (-1) -> 1` (Positive threat class)
- `Legitimate (+1) -> 0` (Negative safe class)  
This ensures that evaluation metrics such as Precision, Recall, and ROC-AUC specifically measure performance on detecting phishing attacks.

#### Q22. What is data leakage, and how did you prevent it?
**Answer:**  
Data leakage occurs when information from outside the training dataset (such as test set distributions or future data) inadvertently influences model training, leading to overly optimistic evaluation metrics. We prevented leakage by:
1. Splitting data into train (80%) and test (20%) sets using stratified sampling before hyperparameter tuning.
2. Fitting all transformations and cross-validation folds strictly within training data splits.

#### Q23. Why did you use Stratified Train-Test Splitting?
**Answer:**  
Stratified sampling (`stratify=y`) guarantees that the training set and testing set maintain the exact same class proportions (55.7% legitimate and 44.3% phishing) as the original dataset. Without stratification, random sampling could introduce class distribution drift between training and testing subsets.

#### Q24. Were there any missing values or nulls in the dataset?
**Answer:**  
No. The UCI Phishing Websites dataset is fully clean and dense, with exactly 0 missing values across all 11,055 instances and 31 columns.

---

### Category 7: Model Evaluation Metrics

#### Q25. What is a Confusion Matrix, and what are its four quadrants?
**Answer:**  
A confusion matrix is a $2 \times 2$ table comparing actual ground-truth labels against model predictions:
1. **True Negative (TN)**: Legitimate website correctly classified as Legitimate.
2. **False Positive (FP)**: Legitimate website incorrectly flagged as Phishing (False Alarm).
3. **False Negative (FN)**: Phishing website incorrectly classified as Legitimate (**Security Hazard**).
4. **True Positive (TP)**: Phishing website correctly detected as Phishing.

#### Q26. Why is False Negative (FN) more dangerous than False Positive (FP) in cybersecurity?
**Answer:**  
A **False Positive** inconveniences a user by displaying an alert on a safe website, which the user can manually inspect or override.  
A **False Negative** represents a missed cyber threat: the user trusts the malicious website, submits banking credentials or passwords, and becomes a victim of identity theft or financial fraud. Therefore, in cybersecurity ML models, **Recall on the Phishing class must be prioritized to minimize False Negatives**.

#### Q27. Define Precision, Recall, and F1-Score mathematically.
**Answer:**  
- **Precision**: $\text{Precision} = \frac{TP}{TP + FP}$ (Fraction of flagged websites that are truly phishing).
- **Recall (Sensitivity)**: $\text{Recall} = \frac{TP}{TP + FN}$ (Fraction of actual phishing websites detected).
- **F1-Score**: $\text{F1} = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$ (Harmonic mean balancing precision and recall).

#### Q28. What is ROC-AUC, and what does an AUC of 0.812 mean?
**Answer:**  
ROC-AUC measures the **Area Under the Receiver Operating Characteristic Curve**, which plots True Positive Rate (Recall) against False Positive Rate ($1 - \text{Specificity}$) across all possible classification decision thresholds. An AUC of $0.812$ means that if we randomly select one phishing URL and one legitimate URL, the model assigns a higher phishing risk score to the phishing URL $81.2\%$ of the time.

---

### Category 8: Model Deployment & Serialization

#### Q29. How did you deploy the trained Python model into JavaScript?
**Answer:**  
Instead of creating a heavy backend server (e.g., Flask or FastAPI) that requires hosting and network calls, we serialized the trained Scikit-learn Decision Tree into a hierarchical JSON file (`model.json`). We then developed a lightweight JavaScript inference engine (`extension/model.js`) that directly traverses the JSON decision tree nodes inside the browser.

#### Q30. How does the JavaScript prediction engine evaluate a tree node?
**Answer:**  
The JS engine traverses the decision tree recursively:
```javascript
function traverse(node, vector) {
  if (node.is_leaf) return node.predicted_class;
  if (vector[node.feature_index] <= node.threshold) {
    return traverse(node.left, vector);
  } else {
    return traverse(node.right, vector);
  }
}
```
This requires zero dependencies, zero network requests, and executes in less than 0.1 milliseconds.

#### Q31. What is Prediction Parity, and how did you verify it?
**Answer:**  
Prediction Parity ensures that the Python model and the JavaScript model produce mathematically identical feature vectors and identical predictions for any given URL. We created an automated test suite (`tests/test_prediction_parity.py`) that feeds a battery of test URLs through both Python and Node.js engines and verifies that feature vectors and predictions match $100\%$.

---

### Category 9: Chrome Extension Architecture

#### Q32. What is Manifest V3, and why did you use it?
**Answer:**  
Manifest V3 is Google's modern specification for Chrome Extensions. It enhances browser security, privacy, and performance by:
1. Replacing persistent background pages with event-driven **Service Workers** (`background.js`).
2. Disallowing remotely hosted JavaScript code; all code must be packaged locally within the extension.
3. Enforcing minimal permissions (`activeTab`, `storage`).

#### Q33. Why is local on-device inference critical for a security extension?
**Answer:**  
1. **Zero Privacy Leakage**: The user's browsing history is never sent to a third-party cloud server.
2. **Zero Latency**: Inference executes locally in $<1\text{ ms}$, ensuring instant UI rendering when clicking the extension icon.
3. **Offline Capability**: The scanner functions even without an active internet connection.
4. **No Infrastructure Costs**: No backend servers, GPU clusters, or API keys are required.

#### Q34. How does the Chrome Extension handle internal URLs like `chrome://extensions`?
**Answer:**  
Internal browser URLs (`chrome://`, `about:blank`, `devtools://`, `file://`) do not represent external web domains. The extension detects these URL schemes and transitions into a neutral **UNKNOWN / INTERNAL** state, clearly informing the user that internal browser pages do not carry external web phishing risks.

#### Q35. What are the three UI states of the extension popup?
**Answer:**  
1. **LEGITIMATE (Green)**: Shield icon with checkmark, low threat meter, confirms safe URL structure with browsing tips.
2. **PHISHING (Red)**: Warning siren, alert banner, high risk score, highlights flagged feature indicators and warns users not to enter credentials.
3. **UNKNOWN / INTERNAL (Slate)**: Informs users that local browser system pages are exempt from external phishing scans.

---

### Category 10: Practical Viva & Troubleshooting Questions

#### Q36. If a model has 98% accuracy on a dataset with 99% legitimate websites, is it a good model?
**Answer:**  
No, this is the classic **Accuracy Paradox** under extreme class imbalance. A trivial dummy classifier that predicts "Legitimate" for every single sample would achieve 99% accuracy while having a Phishing Recall of $0\%$, completely failing its security objective. In our dataset, the classes are well balanced (55.7% vs 44.3%), and we evaluate Precision, Recall, and F1-Score rather than relying on accuracy alone.

#### Q37. What is overfitting, and how did you mitigate it in your Decision Tree?
**Answer:**  
Overfitting occurs when a model memorizes idiosyncrasies and noise in the training data rather than learning generalizable patterns, resulting in near-perfect training accuracy but poor test performance. We mitigated overfitting by:
1. Setting `max_depth=6` to restrict tree depth.
2. Requiring `min_samples_split=2` and `min_samples_leaf=1` through 5-fold cross-validation.
3. Comparing performance against ensemble Random Forests.

#### Q38. Can an attacker evade our Model B? How?
**Answer:**  
Yes. Because Model B relies purely on address-bar URL lexical characteristics:
1. An attacker could purchase an unhyphenated, short domain name (e.g., `updatebank.com`) with a standard TLD.
2. The URL would pass all 8 address-bar checks (returning $+1$ for all features).
3. Detecting such advanced attacks requires hybrid approaches combining URL analysis with webpage DOM content inspection (Model A) and real-time visual similarity matching.

#### Q39. What are the main limitations of your project?
**Answer:**  
1. **Lexical Scope**: Model B cannot detect phishing sites hosted on completely clean domain names that spoof visual layout via HTML/CSS.
2. **Static Snapshot**: Dataset reflects historical phishing patterns; emerging evasion techniques (e.g., Unicode homograph attacks or QR code phishing) require periodic retraining.
3. **No Dynamic Content Scraping**: The extension does not inspect webpage DOM elements to maintain privacy and performance.

#### Q40. What would be your next steps if you had more time for Future Scope?
**Answer:**  
1. **Hybrid Architecture**: Combine fast URL pre-filtering (Model B) with on-demand lightweight DOM inspection for borderline URLs.
2. **Homograph / Punycode Detection**: Add Internationalized Domain Name (IDN) homoglyph detection (e.g., detecting Cyrillic 'a' spoofing Latin 'a').
3. **Active Learning**: Implement an opt-in federated learning feedback loop allowing users to flag zero-day phishing pages to retrain models collaboratively.
