import pandas as pd

# Load sample data
df = pd.read_csv("sample_data.csv")

# Calculate RWA under current and Basel III rules
df["Current RWA"] = df["Exposure Amount (USD)"] * df["Current RW (%)"] / 100
df["Basel III RWA"] = df["Exposure Amount (USD)"] * df["Basel III RW (%)"] / 100

# Sum total RWA
total_current_rwa = df["Current RWA"].sum()
total_basel_rwa = df["Basel III RWA"].sum()

# CET1 Capital input (example)
cet1_capital = 12000000

# CET1 Ratio calculation
cet1_current_ratio = cet1_capital / total_current_rwa
cet1_basel_ratio = cet1_capital / total_basel_rwa

# Output
print(f"Current CET1 Ratio: {cet1_current_ratio:.2%}")
print(f"Basel III CET1 Ratio: {cet1_basel_ratio:.2%}")
print(f"Capital Impact: {cet1_basel_ratio - cet1_current_ratio:.2%}")
