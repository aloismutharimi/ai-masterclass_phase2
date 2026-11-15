'''
A county government in Kisumu has student attendance records in one file and school infrastructure data in another. 
The education officer wants to know: do schools with more classrooms have better attendance rates? 
The files use slightly different school name formats, have some missing values, and one has duplicate rows.

Create two sample DataFrames: one with school name, average_attendance_pct, and county; another with school_name, num_classrooms, and water_access. 
Introduce at least two naming inconsistencies and one duplicate row. 
Clean, merge on school name, and answer the attendance vs classrooms question with a correlation and a scatter plot.

Push to GitHub. README includes your one-sentence finding as it would appear in the officer's report.
'''

"""
Kisumu County Education Analysis
--------------------------------
Merges attendance and infrastructure data to see if
more classrooms correlate with better attendance.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def create_messy_data():
    """Generates the two messy DataFrames as described in the brief."""
    
    # --- FILE 1: Attendance Records ---
    # Intentional errors:
    # - "Kisumu Boys" has a trailing space at the end.
    # - "Kisumu Girls" is spelled "Kisumu Girl's" (with apostrophe).
    # - Missing value (None) for one school's attendance.
    # - One duplicate row (Kisumu Boys High School appears twice).
    attendance_data = {
        "school_name": [
            "Kisumu Boys High School", 
            "Kisumu Girls High School", 
            "Kisumu Boys High School ",   # INCONSISTENCY: Trailing space
            "Kisumu Secondary School",   # INCONSISTENCY: Apostrophe
            "Ahero Mixed Secondary", 
            "Maseno School", 
            "Maseno School",              # DUPLICATE ROW
            "Bondo Mixed School", 
            "Miwani High School"
        ],
        "average_attendance_pct": [85.5, 88.0, 85.5, 82.0, 75.5, 92.0, 92.0, None, 80.0],
        "county": ["Kisumu"] * 9
    }
    df_attendance = pd.DataFrame(attendance_data)

    # --- FILE 2: Infrastructure Records ---
    # Intentional errors:
    # - Missing value (None) for num_classrooms.
    infrastructure_data = {
        "school_name": [
            "Kisumu Boys High School", 
            "Kisumu Girls High School", 
            "Ahero Mixed Sec",            # INCONSISTENCY: Abbreviation
            "Maseno School", 
            "Bondo Mixed School", 
            "Miwani High School",
            "Kisumu Secondary School"     # DUPLICATE ROW (just to test merge behavior)
        ],
        "num_classrooms": [12, 15, 8, 20, 6, None, 12],
        "water_access": ["Yes", "Yes", "No", "Yes", "No", "Yes", "Yes"]
    }
    df_infra = pd.DataFrame(infrastructure_data)

    return df_attendance, df_infra

def clean_data(df, name_col="school_name"):
    """Standardizes school names, removes duplicates, and handles missing values."""
    df = df.copy()
    
    # 1. Standardize names: lowercase, strip spaces, remove apostrophes
    df[name_col] = df[name_col].str.lower().str.strip().str.replace("'", "", regex=False)
    
    # 2. Fix specific abbreviations
    df[name_col] = df[name_col].replace({"ahero mixed sec": "ahero mixed secondary"})
    
    # 3. Drop rows with missing values (NaN) in the core metric columns
    df = df.dropna()
    
    # 4. Drop exact duplicates AFTER cleaning the names
    df = df.drop_duplicates()
    
    return df

def merge_and_analyze(df_att, df_infra):
    """Merges the cleaned data, calculates correlation, and plots."""
    
    # 1. Merge (Inner join keeps only schools present in both datasets)
    merged_df = pd.merge(df_att, df_infra, on="school_name", how="inner")
    
    print("\n--- Merged Data ---")
    print(merged_df)
    
    # 2. Calculate Correlation
    correlation = merged_df["num_classrooms"].corr(merged_df["average_attendance_pct"])
    
    print("\n" + "="*50)
    print(f"📈 CORRELATION: {correlation:.3f}")
    
    # Determine the narrative based on the correlation strength
    if abs(correlation) < 0.2:
        strength = "very weak"
    elif abs(correlation) < 0.4:
        strength = "weak"
    elif abs(correlation) < 0.6:
        strength = "moderate"
    else:
        strength = "strong"
        
    direction = "positive" if correlation > 0 else "negative"
    
    print(f"The correlation is {strength} {direction}.")
    print("="*50)

    # 3. Plotting
    plt.figure(figsize=(8, 5))
    sns.scatterplot(
        data=merged_df, 
        x="num_classrooms", 
        y="average_attendance_pct", 
        s=100, 
        color="darkblue"
    )
    
    # Add title and labels
    plt.title("Classrooms vs. Average Attendance (Kisumu County)", fontsize=14, fontweight="bold")
    plt.xlabel("Number of Classrooms", fontsize=12)
    plt.ylabel("Average Attendance (%)", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.6)
    
    # Save the plot
    plt.savefig("attendance_vs_classrooms.png", dpi=300, bbox_inches="tight")
    print("\n✅ Scatter plot saved as 'attendance_vs_classrooms.png'")
    plt.show()

if __name__ == "__main__":
    print("Loading messy data...")
    df_att, df_infra = create_messy_data()
    
    print("\n--- Cleaning Data ---")
    df_att_clean = clean_data(df_att)
    df_infra_clean = clean_data(df_infra)
    
    # NEW: Run the merge and analysis
    merge_and_analyze(df_att_clean, df_infra_clean)