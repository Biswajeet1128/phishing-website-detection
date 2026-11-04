"""
Data Preprocessing Module
AI-Based Phishing Website Detection System

Handles dataset loading, validation, cleaning, target encoding,
and stratified train-test splitting for Model A and Model B.
"""

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# Supported URL-only features derivable without webpage download or network scanning
URL_FEATURES = [
    'having_IP_Address',
    'URL_Length',
    'Shortining_Service',
    'having_At_Symbol',
    'double_slash_redirecting',
    'Prefix_Suffix',
    'having_Sub_Domain',
    'HTTPS_token'
]

# All 30 features from the original UCI Phishing Websites dataset
ALL_FEATURES = [
    'having_IP_Address',
    'URL_Length',
    'Shortining_Service',
    'having_At_Symbol',
    'double_slash_redirecting',
    'Prefix_Suffix',
    'having_Sub_Domain',
    'SSLfinal_State',
    'Domain_registeration_length',
    'Favicon',
    'port',
    'HTTPS_token',
    'Request_URL',
    'URL_of_Anchor',
    'Links_in_tags',
    'SFH',
    'Submitting_to_email',
    'Abnormal_URL',
    'Redirect',
    'on_mouseover',
    'RightClick',
    'popUpWidnow',
    'Iframe',
    'age_of_domain',
    'DNSRecord',
    'web_traffic',
    'Page_Rank',
    'Google_Index',
    'Links_pointing_to_page',
    'Statistical_report'
]

# Target mapping:
# Original UCI Dataset: -1 = Phishing, 1 = Legitimate
# Scikit-learn Binary Target: 1 = Phishing (positive threat class), 0 = Legitimate (safe class)
TARGET_COLUMN = 'Result'
LABEL_MAPPING = {-1: 1, 1: 0}
REVERSE_LABEL_MAPPING = {1: 'Phishing', 0: 'Legitimate'}


def load_dataset(csv_path: str = None) -> pd.DataFrame:
    """Load dataset from CSV file.
    
    If csv_path is None, defaults to the project's dataset/phishing.csv.
    """
    if csv_path is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_path = os.path.join(base_dir, 'dataset', 'phishing.csv')
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            f"Dataset not found at {csv_path}. "
            f"Run python dataset/download_dataset.py to fetch the official UCI dataset."
        )
        
    df = pd.read_csv(csv_path)
    return df


def validate_dataset(df: pd.DataFrame) -> dict:
    """Validate dataset structure, types, nulls, and expected columns."""
    report = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'missing_values': int(df.isnull().sum().sum()),
        'duplicate_rows': int(df.duplicated().sum()),
        'has_target': TARGET_COLUMN in df.columns,
        'features_present': [col for col in ALL_FEATURES if col in df.columns],
        'missing_features': [col for col in ALL_FEATURES if col not in df.columns],
        'target_distribution': df[TARGET_COLUMN].value_counts().to_dict() if TARGET_COLUMN in df.columns else {}
    }
    return report


def get_preprocessed_data(df: pd.DataFrame, test_size: float = 0.2, random_state: int = 42, drop_duplicates: bool = False):
    """Preprocess data and split into stratified train and test sets.
    
    Returns:
        dict: Containing train and test sets for Model A and Model B, along with target labels.
    """
    data = df.copy()
    
    if drop_duplicates:
        data = data.drop_duplicates().reset_index(drop=True)
        
    # Verify target column exists
    if TARGET_COLUMN not in data.columns:
        raise ValueError(f"Target column '{TARGET_COLUMN}' not found in dataframe.")
        
    # Map target: Phishing (-1) -> 1, Legitimate (1) -> 0
    y = data[TARGET_COLUMN].map(LABEL_MAPPING)
    
    # Check for unmapped targets
    if y.isnull().any():
        raise ValueError(f"Found unexpected values in target column: {data[TARGET_COLUMN].unique()}")
        
    X_all = data[ALL_FEATURES]
    X_url = data[URL_FEATURES]
    
    # Stratified Train-Test Split (prevents data leakage across sets)
    X_train_a, X_test_a, y_train, y_test = train_test_split(
        X_all, y,
        test_size=test_size,
        random_state=random_state,
        stratify=y
    )
    
    X_train_b = X_train_a[URL_FEATURES].copy()
    X_test_b = X_test_a[URL_FEATURES].copy()
    
    return {
        'X_train_a': X_train_a,
        'X_test_a': X_test_a,
        'X_train_b': X_train_b,
        'X_test_b': X_test_b,
        'y_train': y_train,
        'y_test': y_test,
        'all_features': ALL_FEATURES,
        'url_features': URL_FEATURES,
        'label_mapping': LABEL_MAPPING,
        'reverse_label_mapping': REVERSE_LABEL_MAPPING
    }


if __name__ == '__main__':
    print("Testing preprocessing module...")
    df = load_dataset()
    val = validate_dataset(df)
    print(f"Dataset validated successfully: {val['total_rows']} rows, {val['total_columns']} columns.")
    print(f"Missing values: {val['missing_values']}, Duplicates: {val['duplicate_rows']}")
    print(f"Target distribution (Original): {val['target_distribution']}")
    
    data = get_preprocessed_data(df)
    print(f"Model A train shape: {data['X_train_a'].shape}, test shape: {data['X_test_a'].shape}")
    print(f"Model B train shape: {data['X_train_b'].shape}, test shape: {data['X_test_b'].shape}")
    print(f"Target distribution in train (0=Legit, 1=Phish): {data['y_train'].value_counts().to_dict()}")
    print("Preprocessing module is working perfectly.")
