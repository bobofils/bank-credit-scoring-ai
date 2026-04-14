from sklearn.ensemble import RandomForestClassifier
import numpy as np
import joblib

# age, income, loan_amount
X = np.array([
    [25, 200000, 500000],
    [45, 500000, 2000000],
    [35, 300000, 1000000],
    [50, 700000, 3000000],
    [28, 250000, 800000],
    [60, 900000, 4000000]
])

# 0 = risque, 1 = bon client
y = np.array([0, 1, 0, 1, 0, 1])

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

joblib.dump(model, "model.pkl")

print("Model created successfully!")