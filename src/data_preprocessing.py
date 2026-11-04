"""
Backward-compatibility alias for src.preprocessing.
Re-exports all functions and constants from src.preprocessing.
"""

from src.preprocessing import (
    URL_FEATURES,
    ALL_FEATURES,
    TARGET_COLUMN,
    LABEL_MAPPING,
    REVERSE_LABEL_MAPPING,
    load_dataset,
    validate_dataset,
    get_preprocessed_data
)

if __name__ == '__main__':
    from src.preprocessing import load_dataset, validate_dataset
    df = load_dataset()
    print("data_preprocessing (alias) loaded successfully:", df.shape)
