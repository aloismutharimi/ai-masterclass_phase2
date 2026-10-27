# Nakuru Dairy Co-op — Monthly Zone Summary

A Python script that merges two spreadsheets (daily milk collection and farmer details) and generates a clean, printable summary table for the co-op manager. 

## What It Does
Instead of manually compiling totals at the end of the month, this script:
1. Combines the daily collection records with each farmer's zone and payment rate.
2. Calculates the total litres and total payout for every zone.
3. Identifies the top-performing farmer in each zone.
4. Prints a clean summary table that can be screenshotted and sent via WhatsApp or email.

## Required Inputs
To run this script on real data, you need two Excel or CSV files. They must contain the following columns (the column names must match exactly):

**1. Collection Sheet (`collection.csv`)**
Records the daily milk supplied by each farmer.
- `Farmer Name` (e.g., "John Kamau")
- `Date` (e.g., "2026-05-01")
- `Litres` (e.g., 12.5)

**2. Farmers Sheet (`farmers.csv`)**
Records the details and payment rate for each farmer.
- `Farmer Name` (e.g., "John Kamau")
- `Zone` (e.g., "Olenguruone", "Bahati", "Njoro")
- `Rate Per Litre (KES)` (e.g., 52.0)

## How to Run
1. Ensure you have pandas installed:
   ```bash
   pip install pandas
2. Place `collection.csv` and `farmers.csv` in the same folder as the script.

3. Run the script:
    ```bash
    python nakuru_coop_summary
    ```

Example Output
```
=================================================================
        🐄 NAKURU DAIRY CO-OP — MONTHLY ZONE SUMMARY 🐄         
 Generated: May 27, 2026                                        
=================================================================
        Zone Total_Litres     Total_Payout     Top Farmer
Olenguruone      247 L     KES 12,844.00   Grace Njeri
     Bahati      235 L     KES 12,925.00   Sarah Chebet
      Njoro      218 L     KES 10,900.00  Samuel Ochieng
=================================================================
 Note: Top Farmer is determined by highest total litres supplied.
