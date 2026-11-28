# Kiambu Dairy Co-op Payment Calculator

A simple Python CLI tool for the dairy co-op manager to quickly calculate how much a farmer is owed based on the current weekly buying price.

## Problem it solves
Calculating farmer payments manually on a calculator is slow and prone to errors. This tool takes the farmer's name and litres supplied, and instantly prints their total payout based on the current rate.

## How to run

1. Ensure you have Python installed.
2. Clone this repo or download the files.
3. Update the `price.txt` file with the current week's buying price (e.g., `55.0`).
4. Run the script:
   ```bash
   python dairy_calculator.py
## Example Output
```
Kiambu Dairy Co-op Payment Calculator
--------------------------------------
Current buying price: KES 55.00 per litre

Farmer name: Alice Wambui
Litres supplied today: 100

--- Receipt ---
Farmer : Alice Wambui
Litres : 100.0 L
Price  : KES 55.00/L
Total  : KES 5,500.00
---------------