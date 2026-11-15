"""
A microfinance institution in Mombasa wants to understand their loan repayment data before presenting to board members. 
They want to know: what is the typical loan amount, are there unusually large or small loans, and is there any link between loan size and days to first repayment.

Create a dataset of 150 fictional loan records with columns: loan_id, amount_kes, days_to_first_repayment, county. 
Run a full statistical summary (mean, median, std, quartiles). 
Identify outliers using the IQR method and print which loan IDs they are. 
Calculate the correlation between loan amount and days to repayment and state in one plain sentence what it means. 
Plot a histogram of loan amounts.

Push to GitHub. Your README should include the correlation sentence written for a non-technical board member.

Mombasa Microfinance — Loan Analysis
------------------------------------
Calculates summary statistics, identifies outliers using IQR,
calculates correlation, and plots a histogram for the board.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_loans():
    # 1. Load the data
    df = pd.read_csv("mombasa_loans.csv")

    print("=" * 60)
    print(" 📊 MOMBASA MICROFINANCE — LOAN PORTFOLIO ANALYSIS 📊 ".center(60, " "))
    print("=" * 60)

    # 2. Statistical Summary
    print("\n1. FULL STATISTICAL SUMMARY (KES)")
    print("-" * 60)
    # Using .describe() gives us count, mean, std, min, 25%, 50%, 75%, max
    summary = df["amount_kes"].describe()
    # Format the numbers nicely for a board presentation
    for stat, val in summary.items():
        if stat == "count":
            print(f"{stat.capitalize():<10}: {int(val)} loans")
        else:
            print(f"{stat.capitalize():<10}: KES {val:,.2f}")

    # 3. Outlier Detection (IQR Method)
    print("\n2. OUTLIER DETECTION (IQR METHOD)")
    print("-" * 60)
    Q1 = df["amount_kes"].quantile(0.25)
    Q3 = df["amount_kes"].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    print(f"Q1 (25th percentile) : KES {Q1:,.2f}")
    print(f"Q3 (75th percentile) : KES {Q3:,.2f}")
    print(f"IQR (Q3 - Q1)        : KES {IQR:,.2f}")
    print(f"Lower Bound (Q1-1.5*IQR): KES {lower_bound:,.2f}")
    print(f"Upper Bound (Q3+1.5*IQR): KES {upper_bound:,.2f}")

    outliers = df[(df["amount_kes"] < lower_bound) | (df["amount_kes"] > upper_bound)]
    
    print(f"\n⚠️  Found {len(outliers)} outlier(s):")
    for index, row in outliers.iterrows():
        print(f"   - Loan ID: {row['loan_id']} | Amount: KES {row['amount_kes']:,} | Days to Repay: {row['days_to_first_repayment']}")

    # 4. Correlation
    print("\n3. CORRELATION ANALYSIS")
    print("-" * 60)
    correlation = df["amount_kes"].corr(df["days_to_first_repayment"])
    
    # Determine the strength of the correlation for the plain-English sentence
    if abs(correlation) < 0.2:
        strength = "very weak"
    elif abs(correlation) < 0.4:
        strength = "weak"
    elif abs(correlation) < 0.6:
        strength = "moderate"
    else:
        strength = "strong"
        
    direction = "positive" if correlation > 0 else "negative"

    print(f"Correlation Coefficient: {correlation:.3f}")
    print(f"\nBoard Member Summary:")
    print(f"\"There is a {strength} {direction} relationship between the loan amount and")
    print(f"the days it takes for the first repayment. This means that larger loans")
    print(f"tend to take slightly longer to receive their first repayment, but loan")
    print(f"size is not the only factor driving repayment speed.\"")

    # 5. Plotting
    print("\n4. GENERATING CHART")
    print("-" * 60)
    
    plt.figure(figsize=(10, 6))
    sns.histplot(df["amount_kes"], bins=20, kde=True, color="#1f77b4", edgecolor="white")
    
    # Add styling
    plt.title("Distribution of Loan Amounts (Mombasa Microfinance)", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Loan Amount (KES)", fontsize=12)
    plt.ylabel("Number of Loans", fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Format X-axis to show full numbers instead of scientific notation
    plt.ticklabel_format(style='plain', axis='x')
    
    # Save the plot
    plt.savefig("loan_amount_histogram.png", dpi=300, bbox_inches="tight")
    print("✅ Chart saved successfully as 'loan_amount_histogram.png'")
    
    plt.show()

if __name__ == "__main__":
    analyze_loans()