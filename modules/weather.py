import requests
import modules.tts_engine as tts_engine

# Replace this with your actual OpenWeatherMap API key
API_KEY = "729ac328bd1bd89da7816cbaa83afdda"

def get_weather(city):
    """
    Fetches current weather data for the given city using OpenWeatherMap API.

    Args:
        city (str): hyderabad.

    Returns:
        str: A description of the current weather or an error message.
    """
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            return f"❌ Could not get weather for '{city}'. Please check the city name."

        data = response.json()
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"].capitalize()
        humidity = data["main"]["humidity"]
        city_name = data["name"]

        weather = f"Weather in {city_name}: {desc}, {temp}°C, Humidity is {humidity}%"
        
        tts_engine.run(weather)  # Speak the weather information
        return weather
    
    except Exception as e:
        return f"⚠️ Error while fetching weather: {str(e)}"
