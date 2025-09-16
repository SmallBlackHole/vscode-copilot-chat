"""
Weather Tools for the Weather Agent

This module provides tools for retrieving weather information
from OpenWeatherMap API or simulated data.
"""

import os
import requests
from typing import Annotated
from random import randint, choice


def get_weather_real(
    location: Annotated[str, "The city name or location to get the weather for."],
) -> str:
    """
    Get real weather data for a given location using OpenWeatherMap API.
    
    Args:
        location: The city name or location to get the weather for.
        
    Returns:
        A string description of the current weather.
    """
    api_key = os.getenv("WEATHER_API_KEY")
    
    if not api_key:
        # Fallback to simulated weather if no API key is provided
        return get_weather_simulated(location)
    
    try:
        # OpenWeatherMap API endpoint
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": location,
            "appid": api_key,
            "units": "metric"  # Use Celsius
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract weather information
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"]
        city_name = data["name"]
        country = data["sys"]["country"]
        
        return (
            f"Current weather in {city_name}, {country}:\n"
            f"Temperature: {temperature}°C (feels like {feels_like}°C)\n"
            f"Conditions: {description.title()}\n"
            f"Humidity: {humidity}%"
        )
        
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data for {location}: {str(e)}"
    except KeyError as e:
        return f"Error parsing weather data for {location}. Location might not be found."
    except Exception as e:
        return f"Unexpected error getting weather for {location}: {str(e)}"


def get_weather_simulated(
    location: Annotated[str, "The city name or location to get the weather for."],
) -> str:
    """
    Get simulated weather data for a given location.
    This is useful for testing or when the real API is unavailable.
    
    Args:
        location: The city name or location to get the weather for.
        
    Returns:
        A string description of simulated weather.
    """
    conditions = [
        "sunny and clear",
        "partly cloudy", 
        "cloudy",
        "light rain",
        "heavy rain",
        "thunderstorms",
        "foggy",
        "snowy"
    ]
    
    temperature = randint(-5, 35)  # Temperature range in Celsius
    condition = choice(conditions)
    humidity = randint(30, 95)
    
    return (
        f"Current weather in {location}:\n"
        f"Temperature: {temperature}°C\n"
        f"Conditions: {condition.title()}\n"
        f"Humidity: {humidity}%"
    )


def get_weather_forecast(
    location: Annotated[str, "The city name or location to get the forecast for."],
    days: Annotated[int, "Number of days for the forecast (1-5)"] = 3,
) -> str:
    """
    Get a weather forecast for a given location.
    Currently returns simulated data, but can be extended to use real API.
    
    Args:
        location: The city name or location to get the forecast for.
        days: Number of days for the forecast (1-5).
        
    Returns:
        A string description of the weather forecast.
    """
    if days < 1 or days > 5:
        days = 3
    
    conditions = ["sunny", "partly cloudy", "cloudy", "rainy", "stormy"]
    forecast_text = f"{days}-day weather forecast for {location}:\n\n"
    
    for day in range(1, days + 1):
        temp_high = randint(15, 30)
        temp_low = randint(5, temp_high - 5)
        condition = choice(conditions)
        
        forecast_text += f"Day {day}: {condition.title()}, High: {temp_high}°C, Low: {temp_low}°C\n"
    
    return forecast_text