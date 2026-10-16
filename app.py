import os
import requests
from dotenv import load_dotenv

# Load secret API keys from the secure .env file
load_dotenv()

WEATHER_KEY = os.getenv("WEATHER_API_KEY")
TICKETMASTER_KEY = os.getenv("TICKETMASTER_API_KEY")


def get_weather(city):
    """Fetches real-time weather conditions for the specified city."""

    # Handle spaces in city names safely
    city = city.replace(" ", "%20")

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_KEY}&units=imperial"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        return {
            "temp": data["main"]["temp"],
            "condition": data["weather"][0]["main"],
            "description": data["weather"][0]["description"]
        }
    else:
        print("❌ Error fetching weather data. Check city name or API key.")
        return None


def get_local_events(city):
    """Fetches upcoming events in the specified city using Ticketmaster API."""

    # Handle spaces in city names safely
    city = city.replace(" ", "%20")

    url = f"https://app.ticketmaster.com/discovery/v2/events.json?city={city}&apikey={TICKETMASTER_KEY}&size=5"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        if "_embedded" in data:
            return data["_embedded"]["events"]
        else:
            return []
    else:
        print("❌ Error fetching events from Ticketmaster.")
        return None


def main():
    print("--- 🗺️ Smart Local Event & Commute Planner 🗺️ ---\n")

    user_city = input("Enter your target city: ").strip()

    if not user_city:
        print("Please enter a valid city name.")
        return

    # 1. Fetch Weather
    weather = get_weather(user_city)

    if not weather:
        return

    print(
        f"\n🌤️ Current Weather in {user_city.title()}: "
        f"{weather['temp']}°F, {weather['description'].title()}"
    )

    # 2. Smart Assessment Logic
    bad_weather_conditions = ["Rain", "Snow", "Thunderstorm", "Drizzle"]

    is_indoor_day = weather["condition"] in bad_weather_conditions

    if is_indoor_day:
        print(
            "⚠️ Commute Warning: Inclement weather detected. "
            "Recommending indoor venues."
        )
    else:
        print(
            "✅ Commute Clear: Perfect weather for outdoor "
            "or indoor activities."
        )

    # 3. Fetch and Filter Events
    print(f"\nSearching for upcoming events in {user_city.title()}...")

    events = get_local_events(user_city)

    if events:
        print("\n🎉 Top Upcoming Events Found:")

        for idx, event in enumerate(events, 1):
            name = event["name"]
            date = event["dates"]["start"]["localDate"]
            venue = event["_embedded"]["venues"][0]["name"]

            print(f"\n{idx}. {name}")
            print(f"   📅 Date: {date}")
            print(f"   📍 Venue: {venue}")

    else:
        print("No major upcoming events found for this location right now.")


if __name__ == "__main__":
    main()