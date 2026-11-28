# Mombasa Microfinance — Loan Portfolio Analysis

A Python analysis of 150 fictional microfinance loan records in the coastal region. This project generates key statistics, identifies unusual loans, and examines whether larger loans take longer to repay — packaged for a non-technical board presentation.

## The Board Summary (Plain English)
> "There is a weak positive relationship between the loan amount and the days it takes for the first repayment. This means that larger loans tend to take slightly longer to receive their first repayment, but loan size is not the only factor driving repayment speed."

## Key Findings
- **Typical Loan:** The median loan amount is **KES 33,000**, with 50% of all loans falling between KES 21,000 and KES 48,000.
- **Outliers:** Using the IQR method, we identified **2 outliers**: a massive loan of KES 450,000 (ML-0010) and a tiny loan of KES 1,000 (ML-0050). These should be reviewed manually by the credit team.
- **Correlation:** The correlation coefficient is **0.393**, indicating a moderate positive link between loan size and days to first repayment.

## How to Run
1. Install requirements:
   ```bash
   pip install pandas numpy matplotlib seaborn
2. Generate the dataset (creates mombasa_loans.csv):
    ```bash
    python generate_loans.py
    ```
3. Run the analysis and generate the chart:
    ```bash
    python analyze_loans.py