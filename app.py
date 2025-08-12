import streamlit as st
import pandas as pd

st.set_page_config(page_title="BaselLens", layout="wide")

st.title("📊 BaselLens – Capital Impact Visualizer")

# CET1 Capital input
cet1_capital = st.number_input("Enter CET1 Capital (USD)", min_value=0, value=12000000)

# File upload
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.strip()

        required_columns = ["Exposure Amount (USD)", "Current RW (%)", "Basel III RW (%)"]
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            st.error(f"Missing columns: {', '.join(missing_columns)}")
        else:
            # Fill missing RW values
            df["Current RW (%)"] = df["Current RW (%)"].fillna(0)
            df["Basel III RW (%)"] = df["Basel III RW (%)"].fillna(0)

            # Calculate RWA
            df["Current RWA"] = df["Exposure Amount (USD)"] * df["Current RW (%)"] / 100
            df["Basel III RWA"] = df["Exposure Amount (USD)"] * df["Basel III RW (%)"] / 100

            # Sum totals
            total_current_rwa = df["Current RWA"].sum()
            total_basel_rwa = df["Basel III RWA"].sum()

            # CET1 Ratios
            cet1_current_ratio = cet1_capital / total_current_rwa
            cet1_basel_ratio = cet1_capital / total_basel_rwa

            # Display results
            st.subheader("📈 Capital Impact Summary")
            st.metric("Current CET1 Ratio", f"{cet1_current_ratio:.2%}")
            st.metric("Basel III CET1 Ratio", f"{cet1_basel_ratio:.2%}")
            st.metric("Capital Impact", f"{cet1_basel_ratio - cet1_current_ratio:.2%}")

            st.subheader("📊 RWA Breakdown")
            st.dataframe(df[["Asset Class", "Exposure Amount (USD)", "Current RWA", "Basel III RWA"]])

    except Exception as e:
        st.error(f"Error processing file: {e}")
