# What are APIs and Why they matter?
# An API (Application Programming Interface) is a way for one program to talk to another.
# How an API works:
# Step 1: You send a request - Your code sends an HTTP request to a URL, the URL is the address of the API
# Step 2: The API processes your request - The server receives your request, checks if you are allowed to make it, runs needed logic, and prepares a response
# Step 3: You receive a response - The API sends back data or response, usually in JSON format

# Reading API Documentation:
# Every API has documentation that tells you what requests it accepts and what it sends back
# Base URL: the root address all requests start from
# Endpoints: the specific paths you add to the base URL to get different data
# Parameters: options you can add to control what comes back
# Authentication: whether you need a key or account to use it
# Rate limits: how many requests you are allowed per minute or per day
# Response format: the structure of what comes back so you know how to parse it

import requests

url = "https://restcountries.com/v3.1/name/kenya"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    country = data[0]

    name = country["name"]["common"]
    capital = country["capital"][0]
    population = country["population"]
    currency = list(country["currencies"].keys())[0]

    print(f"Country: {name}")
    print(f"Capital: {capital}")
    print(f"Population: {population:,}")
    print(f"Currency: {currency}")
else:
    print("Request failed. Status:", response.status_code)