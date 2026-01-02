import requests

city = input("What is your city: ")
url = f"https://goweather.herokuapp.com/weather/{city}"

print("Getting weather...")
data = requests.get(url).json()
print(f"We got {data}")
# API_KEY = "6e57568d1fbf75aa27ad03e276394fcf"
# CITY = "Lagos"
# BASE_URL = "https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}"