import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

# Load dataset
df = pd.read_csv('data/nutrition.csv')

# Features
X = df[['protein', 'carbs', 'fat']]

# Target
y = df['calories']

# Train model
model = LinearRegression()
model.fit(X, y)

# Save model
joblib.dump(model, 'model/calorie_model.pkl')

print("Model trained successfully!")