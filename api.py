from fastapi import FastAPI
from pydantic import BaseModel
from utils import load_model, preprocess_input, predict_risk

# =========================
# 🚀 API INITIALISATION
# =========================
app = FastAPI(title="BANK Credit Scoring API")

model = load_model()

# =========================
# 📦 DATA MODEL
# =========================
class ClientData(BaseModel):
    age: int
    income: float
    loan_amount: float

# =========================
# 🏠 HOME ROUTE
# =========================
@app.get("/")
def home():
    return {"message": "BANK Credit Scoring API is active"}

# =========================
# 🤖 PREDICTION ENDPOINT
# =========================
@app.post("/predict")
def predict(data: ClientData):

    # Préparation des données
    processed = preprocess_input(
        data.age,
        data.income,
        data.loan_amount
    )

    # Prédiction IA
    prediction, proba = predict_risk(model, processed)

    # Résultat
    return {
        "prediction": int(prediction),
        "risk_probability": float(proba)
    }