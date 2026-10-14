# Exercise: Fetching live data from a public API and printing a clean, human readable summary
import requests

# Fetch page 1 of fake user profiles
url = "https://reqres.in/api/users?page=1"
response = requests.get(url)

if response.status_code == 200:
    payload = response.json()
    users_list = payload.get("data", [])
    
    for user in users_list:
        print(f"{user['first_name']} {user['last_name']} - {user['email']}")
