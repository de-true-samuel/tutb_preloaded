# weather_cli_v1.py
import requests

API_KEY = "a5c4587eb7d0fea4393168e756d914d3"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def fetch_weather(city: str):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"  # Celsius
    }

    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    temperature = data["main"]["temp"]  #cuurent was "main"
    condition = data["weather"][0]["description"]
    city_name = data["name"]

    return city_name, temperature, condition


def pretty_print(city, temp, condition):
    print(f"Weather for {city}: {temp}°C — {condition.capitalize()}")


def main():
    city_input = input("Enter city name: ").strip()

    if not city_input:
        print("City name cannot be empty.")
        return

    try:
        city, temp, condition = fetch_weather(city_input)
        pretty_print(city, temp, condition)
    except requests.exceptions.HTTPError:
        print("City not found or invalid API key.")
    except requests.exceptions.RequestException as e:
        print("Network error:", e)


if __name__ == "__main__":
    main()
    