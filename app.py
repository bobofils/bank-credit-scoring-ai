import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from utils import load_model

model = load_model()

st.set_page_config(page_title="Bank AI Dashboard", layout="centered")

st.title("🏦 Banque - Dashboard de Scoring Crédit")

st.markdown("Analyse intelligente du risque client")

# =========================
# 👤 INPUT CLIENT
# =========================
age = st.slider("Âge", 18, 70, 30)
income = st.number_input("Revenu mensuel (FCFA)", 0, 5000000, 300000)
loan = st.number_input("Montant du crédit (FCFA)", 0, 10000000, 1000000)

# =========================
# 🔘 ANALYSE
# =========================
if st.button("📊 Analyser le risque"):

    data = np.array([[age, income, loan]])

    prediction = model.predict(data)[0]
    proba = model.predict_proba(data)[0][1]

    risk_percent = round((1 - proba) * 100, 2)

    # =========================
    # 💳 SCORE
    # =========================
    st.subheader("💳 Score de risque")

    st.metric("Risque client", f"{risk_percent} %")

    if prediction == 1:
        st.success("Client fiable ✅")
    else:
        st.error("Client à risque ⚠️")

    # =========================
    # 📊 GRAPHIQUE
    # =========================
    st.subheader("📊 Visualisation")

    fig, ax = plt.subplots()
    ax.bar(["Fiabilité", "Risque"], [proba*100, risk_percent], color=["green", "red"])
    st.pyplot(fig)

    # =========================
    # 🧠 EXPLICATION IA
    # =========================
    st.subheader("🧠 Analyse IA")

    if risk_percent < 30:
        st.info("Très bon client, risque faible de défaut.")
    elif risk_percent < 60:
        st.warning("Client moyen, vigilance recommandée.")
    else:
        st.error("Client risqué, crédit déconseillé.")