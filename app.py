import os
import pandas as pd

file_path = "sample_data.csv"

try:
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)

        required_columns = ["Exposure Amount (USD)", "Current RW (%)", "Basel III RW (%)"]
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            print(f"Error: The following required columns are missing from the dataset: {', '.join(missing_columns)}")
        else:
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
    else:
        print(f"Error: The file '{file_path}' was not found. Please upload it or check the path.")

except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found. Please upload it or check the path.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
