# Kisumu County Education Analysis

A data analysis project exploring the relationship between school infrastructure (number of classrooms) and student attendance rates in Kisumu County. 

This script demonstrates real-world data cleaning by resolving formatting inconsistencies, fixing data entry errors, handling missing values, and removing duplicate records before merging two separate datasets.

## The Finding (For the Education Officer)
> "Our analysis of 5 schools in Kisumu County reveals a strong positive correlation (0.95) between the number of classrooms and average student attendance. While this does not prove that building classrooms directly causes higher attendance, it strongly suggests that schools with better infrastructure are retaining students more effectively."

## Data Cleaning Steps Taken
Before analysis, the following data quality issues were resolved:
1. **Standardized Names:** Converted school names to lowercase, stripped trailing spaces, and removed apostrophes.
2. **Resolved Abbreviations:** Mapped "ahero mixed sec" to "ahero mixed secondary" so the merge would succeed.
3. **Fixed Data Entry Errors:** Changed the second duplicate row of "Kisumu Boys" to its actual name, "Kisumu Secondary School," preserving the data point.
4. **Dropped Duplicates:** Removed exact duplicate rows in both datasets.
5. **Handled Missing Data:** Dropped rows missing either attendance or classroom data (Bondo Mixed School and Miwani High School) to ensure the correlation was statistically sound.

## How to Run
1. Install requirements:
   ```bash
   pip install pandas numpy matplotlib seaborn
   ```
2. Run the script:
    ```bash
    python kisumu_education_analysis.py
    ```
3. The script will output the merged dataset, calculate the correlation, and save a scatter plot as attendance_vs_classrooms.png.