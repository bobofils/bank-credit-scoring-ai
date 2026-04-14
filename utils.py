import numpy as np
import joblib
import os

# 📦 Chargement sécurisé du modèle
def load_model():
    model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
    return joblib.load(model_path)


# 🧠 Prétraitement des données
def preprocess_input(age, income, loan_amount):
    return np.array([[age, income, loan_amount]])


# 🔮 Prédiction du risque
def predict_risk(model, data):
    prediction = model.predict(data)[0]
    proba = model.predict_proba(data)[0][1]
    return prediction, proba


# 💰 Calcul crédit
def loan_calculations(loan_amount, annual_rate, months):
    monthly_rate = annual_rate / 12 / 100

    if monthly_rate == 0:
        monthly_payment = loan_amount / months
    else:
        monthly_payment = loan_amount * (
            monthly_rate / (1 - (1 + monthly_rate) ** -months)
        )

    total_payment = monthly_payment * months
    total_interest = total_payment - loan_amount

    return monthly_payment, total_payment, total_interest