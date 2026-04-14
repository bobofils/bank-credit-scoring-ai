from sklearn.ensemble import RandomForestClassifier
import numpy as np
import joblib

X = np.array([
    [25, 2000, 5000],
    [45, 5000, 20000],
    [35, 3000, 10000],
    [50, 7000, 30000]
])

y = np.array([0, 1, 0, 1])

model = RandomForestClassifier()
model.fit(X, y)

joblib.dump(model, "model.pkl")

print("Model created successfully!")