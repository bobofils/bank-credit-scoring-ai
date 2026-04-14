import streamlit as st
import numpy as np
import pandas as pd
import io
from datetime import datetime
from utils import load_model

model = load_model()

st.set_page_config(page_title="Bank AI Dashboard", layout="wide")

st.title("🏦 Banque PRO V2 - Dashboard de Scoring Crédit")
st.markdown("Analyse intelligente du risque client")

# =========================
# 👤 PROFIL CLIENT
# =========================
st.header("👤 Profil utilisateur")

col1, col2, col3 = st.columns(3)

with col1:
    age = st.slider("Âge", 18, 70, 30)
    sexe = st.selectbox("Sexe", ["Homme", "Femme"])
    situation = st.selectbox("Situation matrimoniale", ["Célibataire", "Marié(e)", "Divorcé(e)"])

with col2:
    statut = st.selectbox("Statut professionnel", ["Salarié", "Fonctionnaire", "Indépendant", "Sans emploi"])
    anciennete = st.number_input("Ancienneté (années)", 0, 40, 2)

with col3:
    compte_actif = st.radio("Compte bancaire actif", ["Oui", "Non"])
    epargne = st.radio("Épargne mensuelle", ["Oui", "Non"])

# =========================
# 💰 REVENUS & CHARGES
# =========================
st.header("💰 Revenus & Charges")

col4, col5 = st.columns(2)

with col4:
    revenu = st.number_input("Revenu mensuel (FCFA)", 0, 10000000, 300000)
    autres_revenus = st.number_input("Autres revenus (FCFA)", 0, 5000000, 0)

with col5:
    credit_actuel = st.number_input("Mensualité crédit actuel (FCFA)", 0, 5000000, 0)
    autres_charges = st.number_input("Autres charges (FCFA)", 0, 5000000, 0)

revenu_total = revenu + autres_revenus
charges_total = credit_actuel + autres_charges

taux_endettement = 0
if revenu_total > 0:
    taux_endettement = charges_total / revenu_total

st.info(f"💡 Revenu total : {revenu_total:,.0f} FCFA")
st.warning(f"⚠️ Taux d'endettement : {taux_endettement:.2%}")

# =========================
# 💳 CRÉDIT DEMANDÉ
# =========================
st.header("💳 Crédit demandé")

col6, col7 = st.columns(2)

with col6:
    type_credit = st.selectbox("Type d'emprunt", ["Auto", "Immobilier", "Personnel"])
    montant_credit = st.number_input("Montant emprunt (FCFA)", 0, 20000000, 1000000)

with col7:
    duree = st.slider("Durée (mois)", 6, 60, 12)
    taux = st.slider("Taux d'intérêt (%)", 0.0, 20.0, 5.0)

# =========================
# 🚀 ANALYSE
# =========================
if st.button("📊 Analyser le risque"):

    # INPUT ML (simple)
    input_data = np.array([[age, revenu_total, montant_credit]])

    prediction = model.predict(input_data)[0]
    proba = model.predict_proba(input_data)[0][1]

    risk = round((1 - proba) * 100, 2)

    # =========================
    # 💳 SCORE
    # =========================
    st.subheader("💳 Score de risque")
    st.metric("Risque client", f"{risk} %")

    if prediction == 1:
        st.error("Client fiable ✅")
    else:
        st.error("Client à risque ⚠️")

    # =========================
    # 💰 CALCUL PRÊT
    # =========================
    taux_mensuel = taux / 100 / 12

    if taux_mensuel > 0:
        mensualite = (montant_credit * taux_mensuel) / (1 - (1 + taux_mensuel) ** -duree)
    else:
        mensualite = montant_credit / duree

    total_rembourse = mensualite * duree
    interet_total = total_rembourse - montant_credit

    st.subheader("💰 Simulation de remboursement")

    st.write(f"📌 Mensualité : {mensualite:,.0f} FCFA")
    st.write(f"📌 Total à rembourser : {total_rembourse:,.0f} FCFA")
    st.write(f"📌 Intérêts : {interet_total:,.0f} FCFA")

    # =========================
    # 📊 EXPORT EXCEL
    # =========================
    df = pd.DataFrame([{
        "Âge": age,
        "Sexe": sexe,
        "Situation": situation,
        "Statut": statut,
        "Ancienneté": anciennete,
        "Revenu": revenu_total,
        "Charges": charges_total,
        "Taux endettement": taux_endettement,
        "Montant crédit": montant_credit,
        "Durée": duree,
        "Mensualité": mensualite,
        "Total remboursé": total_rembourse,
        "Intérêt": interet_total,
        "Risque %": risk,
        "Défaut": prediction
    }])

    buffer = io.BytesIO()
    df.to_excel(buffer, index=False)

    st.download_button(
        "📥 Télécharger Excel",
        data=buffer,
        file_name=f"credit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # =========================
    # 📄 EXPORT PDF
    # =========================
    from fpdf import FPDF

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    pdf.cell(200, 10, "RAPPORT CREDIT BANCAIRE", ln=True)

    pdf.cell(200, 10, f"Age: {age}", ln=True)
    pdf.cell(200, 10, f"Revenu: {revenu_total}", ln=True)
    pdf.cell(200, 10, f"Montant credit: {montant_credit}", ln=True)
    pdf.cell(200, 10, f"Mensualite: {mensualite:.0f}", ln=True)
    pdf.cell(200, 10, f"Total: {total_rembourse:.0f}", ln=True)
    pdf.cell(200, 10, f"Risque: {risk}%", ln=True)

    pdf_output = pdf.output(dest="S").encode("latin1")

    st.download_button(
        "📄 Télécharger PDF",
        data=pdf_output,
        file_name="rapport_credit.pdf",
        mime="application/pdf"
    )