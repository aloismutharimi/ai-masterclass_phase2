'''
A Nairobi supermarket chain wants to understand whether their foot traffic follows seasonal patterns. 
They have daily transaction counts for the past 18 months. 
The operations manager wants a chart showing the monthly trend and a 30-day rolling average so he can spot whether sales are genuinely growing or just fluctuating.

Generate 18 months of realistic daily transaction data (use numpy to create seasonal variation: higher in December, lower in February). 
Resample to monthly totals, plot the monthly bars alongside a 30-day rolling average, and add a title and labels a non-technical manager can read. 
Save the chart as a PNG. Write two sentences in your README describing the trend you would report to the client.

Push to GitHub. The PNG should be included in the repo.
'''
"""
Nairobi Supermarket Chain — Foot Traffic Analysis
-------------------------------------------------
Generates 18 months of simulated daily transaction data,
plots the monthly trend with a 30-day rolling average,
and saves the chart as a PNG.

Usage:
    python supermarket_traffic_analysis.py
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def generate_data():
    """Creates 18 months of realistic daily transactions with seasonality."""
    np.random.seed(42)  # For reproducible results

    # 18 months of daily dates starting Jan 1, 2023
    dates = pd.date_range(start="2023-01-01", periods=18 * 30, freq="D")
    
    # Base trend: slow, steady growth over 18 months
    trend = np.linspace(800, 1200, len(dates))
    
    # Seasonality: Higher in December, lower in February
    # We use sine/cosine waves to simulate the yearly cycle
    day_of_year = dates.dayofyear
    # December (approx day 335-365) gets a boost, Feb (day 32-59) drops
    seasonality = 150 * np.sin(2 * np.pi * (day_of_year - 60) / 365)
    
    # Weekly seasonality (Weekends are busier)
    weekly = np.where(dates.dayofweek >= 5, 200, 0)  # Sat/Sun boost
    
    # Random noise (unpredictable daily fluctuations)
    noise = np.random.normal(0, 80, len(dates))
    
    # Combine them all
    transactions = trend + seasonality + weekly + noise
    # Ensure no negative transactions
    transactions = np.clip(transactions, 100, None).astype(int)

    return pd.DataFrame({"Date": dates, "Transactions": transactions})


def analyze_and_plot(df):
    """Resamples data, calculates rolling average, and creates the chart."""
    
    # Set Date as index for time-series resampling
    df = df.set_index("Date")

    # 1. Monthly totals (Resample to Month-End, sum transactions)
    monthly_totals = df["Transactions"].resample("ME").sum()

    # 2. 30-Day Rolling Average (Smooths out daily noise to show the true trend)
    rolling_avg = df["Transactions"].rolling(window=30).mean()

    # 3. Setup the plot
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot monthly totals as bars
    ax.bar(monthly_totals.index, monthly_totals.values, 
           width=20, color="#4facfe", alpha=0.7, label="Monthly Total Transactions")

    # Plot the 30-day rolling average as a line
    ax.plot(rolling_avg.index, rolling_avg.values, 
            color="#ff6b6b", linewidth=2.5, label="30-Day Rolling Average (Daily)")

    # Formatting for a non-technical manager
    ax.set_title("Nairobi Supermarket: Daily Foot Traffic Trend (18 Months)", 
                 fontsize=16, fontweight="bold", pad=20)
    ax.set_xlabel("Month", fontsize=12)
    ax.set_ylabel("Number of Transactions", fontsize=12)
    ax.legend(loc="upper left", fontsize=11)
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    # Format X-axis dates nicely
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    plt.xticks(rotation=45)

    # Add annotation for the December peak
    peak_month = monthly_totals.idxmax()
    peak_value = monthly_totals.max()
    ax.annotate(f"Peak: {peak_month.strftime('%b %Y')}", 
                xy=(peak_month, peak_value), 
                xytext=(peak_month, peak_value + 5000),
                arrowprops=dict(facecolor='black', arrowstyle='->'),
                fontsize=10, ha='center')

    plt.tight_layout()
    
    # Save the chart
    plt.savefig("traffic_trend.png", dpi=300)
    print("✅ Chart saved as 'traffic_trend.png'")
    
    # Show the plot (optional, can comment out for server environments)
    plt.show()

    # Return the monthly totals for the README narrative
    return monthly_totals


if __name__ == "__main__":
    print("Generating simulated data...")
    df = generate_data()
    
    print("Analyzing trends and plotting...")
    monthly = analyze_and_plot(df)
    
    print("\n--- Manager's Summary ---")
    print(f"Total transactions over 18 months: {monthly.sum():,}")
    print(f"Highest month: {monthly.idxmax().strftime('%B %Y')} ({monthly.max():,} transactions)")
    print(f"Lowest month: {monthly.idxmin().strftime('%B %Y')} ({monthly.min():,} transactions)")