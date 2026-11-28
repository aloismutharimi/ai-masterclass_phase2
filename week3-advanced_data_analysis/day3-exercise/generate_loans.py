"""
Mombasa Microfinance — Loan Data Generator
------------------------------------------
Creates 150 fictional loan records for board analysis.
"""

import pandas as pd
import numpy as np
import random

def generate_loan_data():
    np.random.seed(42)
    
    # 1. Setup base data
    n_loans = 150
    loan_ids = [f"ML-{str(i).zfill(4)}" for i in range(1, n_loans + 1)]
    counties = ["Mombasa", "Kilifi", "Kwale", "Lamu"]
    
    # 2. Generate Amounts (Log-normal distribution mimics real-world income/loans)
    # Most loans will be between 10k and 60k. 
    amounts = np.random.lognormal(mean=10.2, sigma=0.8, size=n_loans)
    amounts = np.round(amounts, -3) # Round to nearest 1000
    
    # 3. Generate Days to Repayment (Base: 15 days)
    # Introduce a slight positive correlation: Larger loans take slightly longer
    base_days = np.random.normal(loc=15, scale=5, size=n_loans)
    
    # Normalize amounts to 0-1 to use as a multiplier for days
    amount_multiplier = (amounts - amounts.min()) / (amounts.max() - amounts.min())
    days = base_days + (amount_multiplier * 10) # Adds up to 10 extra days for big loans
    
    days = np.clip(days, 1, 45).astype(int) # Keep between 1 and 45 days
    
    # 4. Assign Counties randomly
    county_assignments = np.random.choice(counties, size=n_loans)
    
    # 5. Inject Outliers (To test the IQR method later)
    # Let's make loan #10 a massive outlier and #50 a tiny outlier
    amounts[9] = 450000  # Massive loan
    amounts[49] = 1000   # Tiny loan
    days[9] = 40         # Massive loan takes long to repay

    # 6. Assemble DataFrame
    df = pd.DataFrame({
        "loan_id": loan_ids,
        "amount_kes": amounts.astype(int),
        "days_to_first_repayment": days,
        "county": county_assignments
    })
    
    return df

if __name__ == "__main__":
    df = generate_loan_data()
    
    # Save to CSV
    df.to_csv("mombasa_loans.csv", index=False)
    
    print("✅ Dataset generated successfully: mombasa_loans.csv")
    print(f"Total records: {len(df)}")
    print("\nFirst 5 records:")
    print(df.head())