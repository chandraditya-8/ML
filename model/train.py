# train_model.py

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
import joblib

# Load dataset
df = pd.read_csv('data/nutrition.csv')

# Clean column names
df.columns = df.columns.str.lower().str.strip()

print(df.columns)

# Remove missing values
df = df.dropna()

# Correct column names from your dataset
numeric_cols = [
    'calories',
    'protein',
    'carbs',
    'fat',
    'iron',
    'vitamin_c'
]

# Convert to numeric
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Remove invalid rows
df = df.dropna()

# Features
X = df[['protein', 'carbs', 'fat', 'iron']]

# Multiple outputs
y = df[['calories', 'fat', 'vitamin_c']]

# Model
model = MultiOutputRegressor(
    RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )
)

# Train model
model.fit(X, y)

# Save model
joblib.dump(model, 'diet_model.pkl')

print(" Model trained successfully")