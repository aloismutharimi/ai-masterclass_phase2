'''
Stock Market & Financial News Snapshot Tool
===========================================
This command-line tool fetches live stock performance data from Alpha Vantage
and pairs it with recent breaking news headlines from NewsAPI for any given company.

How to Run:
1. Make sure you have the 'requests' library installed:
   pip install requests
2. Get your free API keys from:
   - Alpha Vantage: https://www.alphavantage.co/support/#api-key
   - NewsAPI: https://newsapi.org/
3. Run the script in your terminal:
   python stock_snapshot.py
'''

import json
import requests
import os
import sys

from dotenv import load_dotenv

load_dotenv()

# Configure the API
alpha_vantage_key = os.getenv("ALPHA_VANTAGE_API_KEY")
news_key = os.getenv("NEWS_API_KEY")

def fetch_stock_data(ticker):
    '''Fetch stock data from Alpha Vantage API for a given ticker symbol'''
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={alpha_vantage_key}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Check if the response contains expected data
        if "Error Message" in data or "Note" in data:
            print(
                "[Error] Alpha Vantage API limit reached or invalid ticker symbol."
            )
            return None

        quote = data.get("Global Quote", {})
        if not quote:
            return None

        return {
            "symbol": quote.get("01. symbol", ticker.upper()),
            "price": float(quote.get("05. price", 0)),
            "change": float(quote.get("09. change", 0)),
            "change_percent": quote.get("10. change percent", "0%"),
            "volume": int(quote.get("06. volume", 0)),
            "latest_trading_day": quote.get("07. latest trading day", "N/A"),
                }
    except requests.exceptions.RequestException as e:
        print(f"[Network Error] Could not connect to Alpha Vantage: {e}")
        return None


def fetch_company_news(company_query):
  """Fetches recent news articles mentioning the company from NewsAPI."""
  url = f"https://newsapi.org/v2/everything?q={company_query}&apiKey={news_key}&pageSize=3&sortBy=publishedAt"
  try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()

    if data.get("status") != "ok":
      print(
          f"[Error] NewsAPI returned an error:"
          f" {data.get('message', 'Unknown error')}"
      )
      return []

    articles = data.get("articles", [])
    news_list = []
    for art in articles:
      news_list.append({
          "title": art.get("title", "No title"),
          "source": art.get("source", {}).get("name", "Unknown Source"),
          "published_at": art.get("publishedAt", "N/A"),
          "url": art.get("url", "#"),
      })
    return news_list
  except requests.exceptions.RequestException as e:
    print(f"[Network Error] Could not connect to NewsAPI: {e}")
    return []


def main():
  print("==================================================")
  print("      STOCK MARKET & FINANCIAL NEWS SNAPSHOT      ")
  print("==================================================")

  # 1. Take user input (not hardcoded)
  ticker = input("Enter stock ticker symbol (e.g., AAPL, TSLA, MSFT): ").strip()
  if not ticker:
    print("[Error] Ticker symbol cannot be empty. Exiting.")
    sys.exit(1)

  company_query = input(
      f"Enter company name or keyword for news search (e.g., Apple, Tesla): "
  ).strip()
  if not company_query:
    company_query = ticker  # Fallback to ticker if name is omitted

  print(
      f"\nFetching live financial data and news headlines for"
      f" {ticker.upper()}..."
  )

  # 2. Make API Call 1: Stock Data
  stock_data = fetch_stock_data(ticker)
  if not stock_data:
    print(
        "[Graceful Exit] Unable to retrieve stock data. Please check your ticker"
        " or API key."
    )
    sys.exit(1)

  # 3. Make API Call 2: News Articles
  news_data = fetch_company_news(company_query)

  # Combine results into a single dictionary
  combined_snapshot = {"stock_summary": stock_data, "latest_news": news_data}

  # 4. Save response to a JSON file
  output_filename = "stock_news_snapshot.json"
  try:
    with open(output_filename, "w", encoding="utf-8") as f:
      json.dump(combined_snapshot, f, indent=4)
    print(f"[Success] Snapshot saved successfully to '{output_filename}'\n")
  except IOError as e:
    print(f"[File Error] Could not save JSON file: {e}")

  # 5. Print clean, readable output for a non-technical user
  print("--------------------------------------------------")
  print(f" FINANCIAL BRIEFING: {stock_data['symbol']}")
  print("--------------------------------------------------")
  print(f" Current Price:       ${stock_data['price']:,.2f}")

  # Add visual indicator for daily change
  change_val = stock_data["change"]
  change_arrow = "🟢 (+)" if change_val >= 0 else "🔴 (-)"
  print(
      f" Daily Change:        {change_arrow} ${change_val:,.2f}"
      f" ({stock_data['change_percent']})"
  )
  print(f" Trading Volume:      {stock_data['volume']:,} shares")
  print(f" Last Trading Day:    {stock_data['latest_trading_day']}")

  print("\n--------------------------------------------------")
  print(f" TOP NEWS HEADLINES FOR: {company_query.title()}")
  print("--------------------------------------------------")
  if news_data:
    for idx, article in enumerate(news_data, start=1):
      print(f"{idx}. {article['title']}")
      print(f"   Source: {article['source']} | Published: {article['published_at'][:10]}")
      print(f"   Link: {article['url']}")
      print()
  else:
    print("No recent news articles found matching this query.")
  print("==================================================")


if __name__ == "__main__":
  main()