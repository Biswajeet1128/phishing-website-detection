"""
Dataset Acquisition & Conversion Script
AI-Based Phishing Website Detection System

Downloads the official UCI Phishing Websites dataset archive (ID: 327)
and converts the raw ARFF file into dataset/phishing.csv.
"""

import os
import sys
import zipfile
import urllib.request
import pandas as pd

UCI_ZIP_URL = "https://archive.ics.uci.edu/static/public/327/phishing+websites.zip"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, 'dataset')
CSV_PATH = os.path.join(DATASET_DIR, 'phishing.csv')
TEMP_ZIP = os.path.join(DATASET_DIR, 'uci_phishing_temp.zip')


def download_and_prepare_dataset(force: bool = False):
    """Download and unpack dataset from UCI Machine Learning Repository."""
    if os.path.exists(CSV_PATH) and not force:
        print(f"[OK] Dataset already exists at {CSV_PATH}")
        df = pd.read_csv(CSV_PATH)
        print(f"     Shape: {df.shape[0]} rows, {df.shape[1]} columns.")
        return CSV_PATH

    print(f"[*] Downloading UCI Phishing Websites dataset from:\n    {UCI_ZIP_URL}")
    os.makedirs(DATASET_DIR, exist_ok=True)
    
    urllib.request.urlretrieve(UCI_ZIP_URL, TEMP_ZIP)
    print(f"[+] Download complete: {os.path.getsize(TEMP_ZIP) / 1024:.1f} KB")

    print("[*] Extracting Training Dataset.arff...")
    with zipfile.ZipFile(TEMP_ZIP, 'r') as z:
        z.extract('Training Dataset.arff', DATASET_DIR)

    arff_path = os.path.join(DATASET_DIR, 'Training Dataset.arff')
    print("[*] Converting ARFF to CSV format...")

    attributes = []
    data_rows = []
    is_data = False

    with open(arff_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.lower().startswith('@attribute'):
                parts = line.split()
                attributes.append(parts[1])
            elif line.lower().startswith('@data'):
                is_data = True
            elif is_data:
                data_rows.append([int(val.strip()) for val in line.split(',')])

    df = pd.DataFrame(data_rows, columns=attributes)
    df.to_csv(CSV_PATH, index=False)
    print(f"[+] Saved {CSV_PATH} ({df.shape[0]} rows, {df.shape[1]} columns)")

    # Cleanup temporary download files
    if os.path.exists(TEMP_ZIP):
        os.remove(TEMP_ZIP)
    if os.path.exists(arff_path):
        os.remove(arff_path)
    print("[+] Cleaned temporary download artifacts.")
    return CSV_PATH


if __name__ == '__main__':
    force_download = '--force' in sys.argv
    download_and_prepare_dataset(force=force_download)
