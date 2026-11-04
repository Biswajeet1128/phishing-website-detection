# Dataset Documentation: UCI Phishing Websites

This directory contains the dataset used to train, evaluate, and benchmark the Machine Learning models in this project.

---

## 📌 Dataset Overview

- **Official Name:** Phishing Websites Dataset
- **Repository:** UCI Machine Learning Repository (Dataset ID: 327)
- **Official URL:** [https://archive.ics.uci.edu/dataset/327/phishing+websites](https://archive.ics.uci.edu/dataset/327/phishing+websites)
- **Creators:** Rami M. Mohammad, Fadi Thabtah, and Lee McCluskey (University of Huddersfield, UK)
- **License:** Creative Commons Attribution 4.0 International (CC BY 4.0)

---

## 📊 Dataset Characteristics

- **Total Instances:** 11,055 records
- **Total Attributes:** 31 (30 predictive features + 1 target class)
- **Missing Values:** 0 (dense, fully populated)
- **Feature Data Types:** Discrete categorical, encoded as `{-1, 0, 1}`
- **Target Variable (`Result`):**
  - `1`: Legitimate Website (6,157 instances, 55.69%)
  - `-1`: Phishing Website (4,898 instances, 44.31%)

### Binary Target Mapping in Scikit-Learn
For standard binary classification in Python:
- `Phishing (-1) -> 1` (Positive threat class)
- `Legitimate (+1) -> 0` (Negative safe class)

---

## 🔍 Feature Breakdown (30 Attributes)

The dataset features fall into four functional categories:

### 1. Address Bar-Based Features (8 Features - Used in Model B & Chrome Extension)
These 8 features are deterministically extractable from the URL string itself without making network calls or parsing remote web pages:
1. `having_IP_Address`: Checks if an IP address is used in place of a domain name (`-1`: Phishing, `1`: Legitimate).
2. `URL_Length`: Measures URL string length (`<54`: `1`, `54-75`: `0`, `>75`: `-1`).
3. `Shortining_Service`: Detects known URL shortening services like bit.ly, tinyurl (`-1`: Phishing, `1`: Legitimate).
4. `having_At_Symbol`: Checks for `@` symbol trick in URL (`-1`: Phishing, `1`: Legitimate).
5. `double_slash_redirecting`: Position of last `//` occurring after position 7 (`-1`: Phishing, `1`: Legitimate).
6. `Prefix_Suffix`: Domain name includes hyphen `-` symbol (`-1`: Phishing, `1`: Legitimate).
7. `having_Sub_Domain`: Number of subdomains / dots (`1 dot`: `1`, `2 dots`: `0`, `>2 dots`: `-1`).
8. `HTTPS_token`: HTTP or HTTPS token embedded inside the domain name (`-1`: Phishing, `1`: Legitimate).

### 2. Abnormal-Based Features (6 Features - Model A Benchmark)
9. `Request_URL`: Percentage of external objects loaded from external domains.
10. `URL_of_Anchor`: Percentage of anchor URLs pointing to external/empty targets.
11. `Links_in_tags`: Percentage of links in `<meta>`, `<script>`, `<link>` tags.
12. `SFH`: Server Form Handler action target validation.
13. `Submitting_to_email`: Use of `mailto:` function to submit form inputs.
14. `Abnormal_URL`: Hostname not matching WHOIS record.

### 3. HTML and JavaScript-Based Features (5 Features - Model A Benchmark)
15. `Redirect`: Number of HTTP page redirects.
16. `on_mouseover`: Status bar customization via JavaScript onMouseOver.
17. `RightClick`: Disabled right-click context menu via JavaScript.
18. `popUpWidnow`: Pop-up window containing text input fields.
19. `Iframe`: Use of invisible iframe tags.

### 4. Domain-Based Features (11 Features - Model A Benchmark)
20. `SSLfinal_State`: SSL certificate validity, age, and trusted issuer.
21. `Domain_registeration_length`: Domain registration expiration threshold.
22. `Favicon`: Favicon loaded from an external domain.
23. `port`: Non-standard open server ports.
24. `age_of_domain`: Age of domain name from WHOIS query.
25. `DNSRecord`: DNS record resolution check.
26. `web_traffic`: Website traffic rank via Alexa/traffic monitor.
27. `Page_Rank`: Google PageRank metric.
28. `Google_Index`: Domain indexation in Google search.
29. `Links_pointing_to_page`: Inbound backlink count.
30. `Statistical_report`: Host IP matches PhishTank / StopBadware blacklist feeds.

---

## 📥 How to Download or Recreate

If `phishing.csv` is not present, you can automatically download and convert it directly from UCI using the included helper script:

```bash
python dataset/download_dataset.py
```

To force a fresh re-download:
```bash
python dataset/download_dataset.py --force
```

---

## 📚 Citation

If you use this dataset, please cite the original authors:

```bibtex
@article{mohammad2014predicting,
  title={Predicting phishing websites based on self-structuring neural network},
  author={Mohammad, Rami M and Thabtah, Fadi and McCluskey, Lee},
  journal={Neural Computing and Applications},
  volume={25},
  number={2},
  pages={443--458},
  year={2014},
  publisher={Springer}
}
```
