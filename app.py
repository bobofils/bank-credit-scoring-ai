import streamlit as st
import pandas as pd
import io
from datetime import datetime
from utils import load_model, preprocess_input, predict_risk, loan_calculations

# =========================
# ⚙️ CONFIGURATION APP
# =========================
st.set_page_config(page_title="BANK Scoring AI", layout="centered")

# =========================
# 🏦 HEADER
# =========================
st.title("🏦 BANK - Credit Scoring System")
st.markdown("### AI-powered loan risk & repayment analysis")
st.warning("⚠️ Demo only - No personal data is stored")

model = load_model()

# =========================
# 👤 PROFIL UTILISATEUR
# =========================
st.header("👤 Client Profile")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Full Name")
    age = st.slider("Age", 18, 70, 30)

with col2:
    income = st.number_input("Monthly Income", 0, 10000, 3000)
    loan_amount = st.number_input("Loan Amount", 0, 50000, 10000)

# =========================
# 💰 PARAMÈTRES DU PRÊT
# =========================
st.header("💰 Loan Parameters")

col3, col4 = st.columns(2)

with col3:
    duration = st.slider("Duration (months)", 6, 60, 12)

with col4:
    interest_rate = st.slider("Interest Rate (%)", 0.0, 20.0, 5.0)

# =========================
# 🚀 BOUTON ANALYSE
# =========================
if st.button("🔍 Analyze Credit"):

    # 🤖 IA SCORING
    data = preprocess_input(age, income, loan_amount)
    prediction, proba = predict_risk(model, data)

    st.header("📊 Credit Risk Result")

    if prediction == 1:
        st.error(f"⚠️ High Risk ({proba:.2f})")
    else:
        st.success(f"✅ Low Risk ({proba:.2f})")

    # 💰 CALCUL FINANCIER
    monthly, total, interest = loan_calculations(
        loan_amount, interest_rate, duration
    )

    st.header("💰 Loan Summary")

    st.write(f"**Monthly Payment:** {monthly:.2f}")
    st.write(f"**Total Repayment:** {total:.2f}")
    st.write(f"**Total Interest:** {interest:.2f}")

    # =========================
    # 📊 TABLEAU RÉCAP
    # =========================
    df = pd.DataFrame({
        "Name": [name],
        "Age": [age],
        "Income": [income],
        "Loan": [loan_amount],
        "Duration": [duration],
        "Rate": [interest_rate],
        "Monthly Payment": [monthly],
        "Total Payment": [total],
        "Interest": [interest],
        "Risk": [prediction],
        "Probability": [proba]
    })

    # =========================
    # 📥 EXPORT EXCEL
    # =========================
    buffer = io.BytesIO()
    df.to_excel(buffer, index=False)

    filename = f"scoring_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

    st.download_button(
        "📥 Download Excel",
        data=buffer,
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # =========================
    # 📄 EXPORT PDF
    # =========================
    from fpdf import FPDF

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="BANK CREDIT REPORT", ln=True)

    pdf.cell(200, 10, txt=f"Name: {name}", ln=True)
    pdf.cell(200, 10, txt=f"Age: {age}", ln=True)
    pdf.cell(200, 10, txt=f"Income: {income}", ln=True)

    pdf.cell(200, 10, txt=f"Loan: {loan_amount}", ln=True)
    pdf.cell(200, 10, txt=f"Duration: {duration} months", ln=True)
    pdf.cell(200, 10, txt=f"Interest Rate: {interest_rate}%", ln=True)

    pdf.cell(200, 10, txt=f"Monthly Payment: {monthly:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Total Payment: {total:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Interest: {interest:.2f}", ln=True)

    pdf.cell(200, 10, txt=f"Risk: {prediction}", ln=True)

    pdf_output = pdf.output(dest='S').encode('latin1')

    st.download_button(
        "📄 Download PDF",
        data=pdf_output,
        file_name="bank_credit_report.pdf",
        mime="application/pdf"
    )