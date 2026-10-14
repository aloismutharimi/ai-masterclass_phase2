import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("NEWS_API_KEY")

url = ('https://newsapi.org/v2/top-headlines?'
       'country=us&'
       f'apiKey={api_key}')

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    articles = data['articles']
    for article in articles:
        print(f"Title: {article['title']}")
        print(f"Author: {article['author']}")
        print(f"Published At: {article['publishedAt']}")
        print(f"Description: {article['description']}")
        print(f"URL: {article['url']}\n")

elif response.status_code == 401:
    print("Your API key is invalid. Check your it again!")

elif response.status_code == 404:
    print("The requested resource was not found. Check the endpoint URL.")

elif response.status_code == 429:
    print("Too many requests. Slow down and wait before retrying.")

else:
    print(f"Unexpected error: {response.status_code}")

