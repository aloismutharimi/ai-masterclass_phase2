'''
A Nakuru dairy co-op manager has two spreadsheets. One records daily milk collection per farmer (farmer name, date, litres). 
The other holds farmer details (farmer name, zone, payment rate per litre). He wants one table showing: total litres per zone this month, total payout per zone, and top farmer per zone.

Build a pandas script that merges the two DataFrames on farmer name, pivots the result by zone, and prints a clean summary table with those three columns. 
Create realistic sample data for at least 12 farmers across three zones. The output should be something you can screenshot and send to the client.

Push to GitHub. README explains what the script does and what two files it needs as inputs.
'''

"""
Nakuru Dairy Co-op — Monthly Zone Summary
-----------------------------------------
Merges daily milk collection with farmer details,
pivots by zone, and prints a clean summary table.

Usage:
    python nakuru_coop_summary.py
"""

import pandas as pd
from datetime import datetime

def build_sample_data():
    """Simulates the two spreadsheets the manager provided."""
    # Spreadsheet 1: Farmer details
    farmers = pd.DataFrame({
        "Farmer Name": [
            "John Kamau", "Mary Wanjiku", "Peter Otieno", "Grace Njeri",
            "David Mwangi", "Sarah Chebet", "James Kiprop", "Alice Wambui",
            "Samuel Ochieng", "Lucy Wairimu", "Daniel Kibet", "Ruth Achieng"
        ],
        "Zone": [
            "Olenguruone", "Olenguruone", "Olenguruone", "Olenguruone",
            "Bahati", "Bahati", "Bahati", "Bahati",
            "Njoro", "Njoro", "Njoro", "Njoro"
        ],
        "Rate Per Litre (KES)": [
            52.0, 52.0, 52.0, 52.0,
            55.0, 55.0, 55.0, 55.0,
            50.0, 50.0, 50.0, 50.0
        ]
    })

    # Spreadsheet 2: Daily collection (simulated for 5 days)
    # Instead of typing 60+ rows manually, we generate them cleanly.
    collection_rows = []
    dates = ["2026-05-01", "2026-05-02", "2026-05-03", "2026-05-04", "2026-05-05"]
    
    # Simulating different litres per farmer per day
    litres_data = {
        "John Kamau": [12, 15, 14, 12, 16],
        "Mary Wanjiku": [20, 22, 19, 21, 23],
        "Peter Otieno": [8, 9, 8, 10, 9],
        "Grace Njeri": [30, 28, 32, 31, 29],
        "David Mwangi": [18, 19, 17, 18, 20],
        "Sarah Chebet": [25, 24, 26, 25, 27],
        "James Kiprop": [15, 14, 16, 15, 14],
        "Alice Wambui": [10, 12, 11, 13, 12],
        "Samuel Ochieng": [22, 21, 23, 22, 24],
        "Lucy Wairimu": [9, 8, 10, 9, 8],
        "Daniel Kibet": [17, 18, 16, 19, 18],
        "Ruth Achieng": [14, 15, 13, 14, 16]
    }

    for date in dates:
        for farmer, daily_litres in litres_data.items():
            # Grab today's litres based on index of the date
            day_index = dates.index(date)
            collection_rows.append({
                "Farmer Name": farmer,
                "Date": date,
                "Litres": daily_litres[day_index]
            })

    collection = pd.DataFrame(collection_rows)
    return farmers, collection


def generate_summary(farmers, collection):
    """Merges, aggregates, and pivots the data."""
    
    # 1. Merge the two tables on 'Farmer Name'
    merged = pd.merge(collection, farmers, on="Farmer Name", how="left")

    # 2. Calculate the payout for each row (Litres * Rate)
    merged["Payout"] = merged["Litres"] * merged["Rate Per Litre (KES)"]

    # 3. Group by Zone and Farmer to find totals and top farmers
    # First, we need total litres and payout per farmer (to find the top farmer per zone)
    farmer_totals = merged.groupby(["Zone", "Farmer Name"]).agg(
        Total_Litres=("Litres", "sum"),
        Total_Payout=("Payout", "sum")
    ).reset_index()

    # 4. Find the top farmer per zone based on Total Litres
    # idxmax() gives us the index of the highest value in each zone group
    top_farmers = farmer_totals.loc[
        farmer_totals.groupby("Zone")["Total_Litres"].idxmax()
    ][["Zone", "Farmer Name", "Total_Litres"]].rename(
        columns={"Farmer Name": "Top Farmer", "Total_Litres": "Top Farmer Litres"}
    )

    # 5. Calculate the overall zone totals (Total Litres and Total Payout)
    zone_totals = merged.groupby("Zone").agg(
        Total_Litres=("Litres", "sum"),
        Total_Payout=("Payout", "sum")
    ).reset_index()

    # 6. Merge the zone totals with the top farmer info
    summary = pd.merge(zone_totals, top_farmers, on="Zone")

    # 7. Format the final table for printing
    final_table = summary[["Zone", "Total_Litres", "Total_Payout", "Top Farmer"]].copy()
    
    # Format currency and numbers with commas for readability
    final_table["Total_Litres"] = final_table["Total_Litres"].map("{:,.0f} L".format)
    final_table["Total_Payout"] = final_table["Total_Payout"].map("KES {:,.2f}".format)

    return final_table


def print_client_report(table):
    """Prints a clean, professional summary suitable for WhatsApp/Email."""
    print("\n" + "=" * 65)
    print(" 🐄 NAKURU DAIRY CO-OP — MONTHLY ZONE SUMMARY 🐄 ".center(65, " "))
    print(f" Generated: {datetime.now().strftime('%B %d, %Y')}".ljust(65))
    print("=" * 65)
    
    # Print the DataFrame cleanly without the default pandas index
    print(table.to_string(index=False))
    
    print("=" * 65)
    print(" Note: Top Farmer is determined by highest total litres supplied.\n")


if __name__ == "__main__":
    # 1. Load data
    farmers_df, collection_df = build_sample_data()

    # 2. Process
    summary_table = generate_summary(farmers_df, collection_df)

    # 3. Output
    print_client_report(summary_table)