from fastapi import FastAPI
from pydantic import BaseModel
from utils import load_model, preprocess_input, predict_risk

app = FastAPI(title="ECOBANK Credit Scoring API")

model = load_model()

class ClientData(BaseModel):
    age: int
    income: float
    loan_amount: float

@app.get("/")
def home():
    return {"message": "API Credit Scoring active"}

@app.post("/predict")
def predict(data: ClientData):
    processed = preprocess_input(data.age, data.income, data.loan_amount)
    prediction, proba = predict_risk(model, processed)

    return {
        "prediction": int(prediction),
        "risk_probability": float(proba)
    }