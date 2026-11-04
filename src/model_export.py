"""
Model Serialization and Export Module
AI-Based Phishing Website Detection System

Converts trained Scikit-learn models (Decision Tree & Random Forest)
into a portable JSON format for client-side JavaScript execution
within the Chrome Extension without external dependencies.
"""

import os
import sys
import json
import joblib
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.data_preprocessing import URL_FEATURES, LABEL_MAPPING, REVERSE_LABEL_MAPPING


def serialize_tree_node(tree, node_id, feature_names):
    """Recursively convert a Scikit-learn tree node into a nested dictionary."""
    is_leaf = tree.children_left[node_id] == -1 and tree.children_right[node_id] == -1
    node_counts = tree.value[node_id][0].tolist()
    total_samples = sum(node_counts)
    probs = [round(c / total_samples, 4) if total_samples > 0 else 0.0 for c in node_counts]
    predicted_class = int(np.argmax(node_counts))
    
    node_dict = {
        'node_id': int(node_id),
        'is_leaf': bool(is_leaf),
        'samples': int(total_samples),
        'class_counts': node_counts,
        'probabilities': probs,
        'predicted_class': predicted_class,
        'predicted_label': REVERSE_LABEL_MAPPING.get(predicted_class, 'Unknown')
    }
    
    if not is_leaf:
        feat_idx = int(tree.feature[node_id])
        node_dict['feature_index'] = feat_idx
        node_dict['feature_name'] = feature_names[feat_idx]
        node_dict['threshold'] = float(tree.threshold[node_id])
        node_dict['left'] = serialize_tree_node(tree, tree.children_left[node_id], feature_names)
        node_dict['right'] = serialize_tree_node(tree, tree.children_right[node_id], feature_names)
        
    return node_dict


def export_decision_tree(dt_model, feature_names, output_path=None):
    """Serialize a DecisionTreeClassifier into a standalone JSON model file."""
    tree_struct = serialize_tree_node(dt_model.tree_, 0, feature_names)
    
    model_payload = {
        'model_type': 'DecisionTreeClassifier',
        'track': 'Model B (URL Real-Time)',
        'target_classes': [0, 1],
        'class_names': ['Legitimate', 'Phishing'],
        'feature_names': feature_names,
        'num_features': len(feature_names),
        'tree': tree_struct,
        'threshold': 0.5,
        'metadata': {
            'criterion': dt_model.criterion,
            'max_depth': dt_model.max_depth,
            'n_classes': int(dt_model.n_classes_),
            'n_features': int(dt_model.n_features_in_)
        }
    }
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(model_payload, f, indent=2)
            
    return model_payload


def export_random_forest(rf_model, feature_names, max_trees=20, output_path=None):
    """Serialize a Random Forest ensemble into JSON format."""
    trees = []
    # Export first max_trees estimators to maintain lightweight extension footprint
    selected_estimators = rf_model.estimators_[:max_trees]
    for idx, est in enumerate(selected_estimators):
        trees.append({
            'tree_index': idx,
            'root': serialize_tree_node(est.tree_, 0, feature_names)
        })
        
    model_payload = {
        'model_type': 'RandomForestClassifier',
        'track': 'Model B (URL Real-Time)',
        'num_trees': len(trees),
        'total_trained_trees': len(rf_model.estimators_),
        'target_classes': [0, 1],
        'class_names': ['Legitimate', 'Phishing'],
        'feature_names': feature_names,
        'num_features': len(feature_names),
        'trees': trees,
        'threshold': 0.5
    }
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(model_payload, f, indent=2)
            
    return model_payload


def export_selected_model():
    """Export the chosen Model B for Chrome Extension deployment."""
    print("Exporting trained Model B to JSON for browser-side JavaScript inference...")
    
    dt_path = os.path.join(BASE_DIR, 'models', 'model_b', 'decision_tree.joblib')
    rf_path = os.path.join(BASE_DIR, 'models', 'model_b', 'random_forest.joblib')
    
    if not os.path.exists(dt_path):
        raise FileNotFoundError(f"Trained model not found at {dt_path}. Run train_models.py first.")
        
    dt_model = joblib.load(dt_path)
    
    # 1. Export Decision Tree to models/model_b/model.json
    export_dest_b = os.path.join(BASE_DIR, 'models', 'model_b', 'model.json')
    export_decision_tree(dt_model, URL_FEATURES, export_dest_b)
    print(f"Exported Decision Tree JSON to: {export_dest_b}")
    
    # 2. Copy/export directly to extension directory
    ext_dest = os.path.join(BASE_DIR, 'extension', 'model.json')
    dt_payload = export_decision_tree(dt_model, URL_FEATURES, ext_dest)
    print(f"Exported Chrome Extension model to: {ext_dest}")
    
    # 2b. Generate extension/model_data.js for direct script tag loading
    ext_js_dest = os.path.join(BASE_DIR, 'extension', 'model_data.js')
    with open(ext_js_dest, 'w', encoding='utf-8') as f:
        f.write("/**\n * Embedded Model Data for Chrome Extension\n * AI-Based Phishing Website Detection System\n */\n")
        f.write("const MODEL_DATA = ")
        json.dump(dt_payload, f, indent=2)
        f.write(";\n\nif (typeof module !== 'undefined' && module.exports) {\n  module.exports = MODEL_DATA;\n}\n")
    print(f"Exported Chrome Extension model_data.js to: {ext_js_dest}")
    
    # Also export Random Forest as ensemble option
    rf_model = joblib.load(rf_path)
    rf_dest = os.path.join(BASE_DIR, 'models', 'model_b', 'random_forest.json')
    export_random_forest(rf_model, URL_FEATURES, max_trees=25, output_path=rf_dest)
    print(f"Exported Random Forest JSON to: {rf_dest}")
    
    print("\nModel export completed successfully.")


if __name__ == '__main__':
    export_selected_model()
