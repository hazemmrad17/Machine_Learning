"""
Script to create example data files for both classes (Benign and Malignant)
"""
import pandas as pd
import json
import os

# Load data
data_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data.csv')
df = pd.read_csv(data_path)

# Fix column names (replace spaces with underscores)
df.columns = df.columns.str.replace(' ', '_')

# Get examples from both classes
benign_sample = df[df['diagnosis'] == 'B'].iloc[0]
malignant_sample = df[df['diagnosis'] == 'M'].iloc[0]

# Extract only the 30 features
features = [
    'radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean',
    'smoothness_mean', 'compactness_mean', 'concavity_mean',
    'concave_points_mean', 'symmetry_mean', 'fractal_dimension_mean',
    'radius_se', 'texture_se', 'perimeter_se', 'area_se',
    'smoothness_se', 'compactness_se', 'concavity_se',
    'concave_points_se', 'symmetry_se', 'fractal_dimension_se',
    'radius_worst', 'texture_worst', 'perimeter_worst', 'area_worst',
    'smoothness_worst', 'compactness_worst', 'concavity_worst',
    'concave_points_worst', 'symmetry_worst', 'fractal_dimension_worst'
]

benign_example = benign_sample[features].to_dict()
malignant_example = malignant_sample[features].to_dict()

# Save examples
examples_dir = os.path.join(os.path.dirname(__file__), '..', 'web_ui', 'examples')
os.makedirs(examples_dir, exist_ok=True)

with open(os.path.join(examples_dir, 'benign_example.json'), 'w') as f:
    json.dump(benign_example, f, indent=2)

with open(os.path.join(examples_dir, 'malignant_example.json'), 'w') as f:
    json.dump(malignant_example, f, indent=2)

print("✅ Example files created:")
print(f"  - {os.path.join(examples_dir, 'benign_example.json')}")
print(f"  - {os.path.join(examples_dir, 'malignant_example.json')}")

