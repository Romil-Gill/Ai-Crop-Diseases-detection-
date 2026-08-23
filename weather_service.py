"""
FasalRakshak AI - Weather Service Module
Integration layer for Open-Meteo Geocoding & Forecast APIs.
Handles network timeouts, error fallbacks, and disease weather context evaluation.
"""

import requests
from typing import Dict, Any, List, Optional
from weather_risk_data import evaluate_weather_favorability

GEOCODING_API_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_API_URL = "https://api.open-meteo.com/v1/forecast"
REQUEST_TIMEOUT = 4.0  # 4-second timeout to prevent UI hanging


def search_location(query: str) -> List[Dict[str, Any]]:
    """
    Searches location names via Open-Meteo Geocoding API.
    Returns normalized list of matching places.
    """
    if not query or len(query.strip()) < 2:
        return []

    try:
        response = requests.get(
            GEOCODING_API_URL,
            params={
                "name": query.strip(),
                "count": 5,
                "language": "en",
                "format": "json"
            },
            timeout=REQUEST_TIMEOUT
        )
        if response.status_code != 200:
            return []

        data = response.json()
        results = data.get("results", [])

        normalized = []
        for item in results:
            normalized.append({
                "name": item.get("name", ""),
                "admin1": item.get("admin1", ""),
                "country": item.get("country", ""),
                "latitude": round(float(item.get("latitude", 0.0)), 4),
                "longitude": round(float(item.get("longitude", 0.0)), 4),
                "timezone": item.get("timezone", "Asia/Kolkata")
            })

        return normalized
    except Exception as e:
        print(f"[WEATHER SERVICE WARNING] Geocoding API request failed: {e}")
        return []


def fetch_weather_context(latitude: float, longitude: float, class_name: str, location_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieves current & 48-hour forecast weather data from Open-Meteo API and evaluates disease risk favorability.
    Handles network errors gracefully by returning a clean fallback payload.
    """
    try:
        response = requests.get(
            FORECAST_API_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m",
                "hourly": "temperature_2m,relative_humidity_2m,dew_point_2m,precipitation,precipitation_probability",
                "forecast_days": 2,
                "timezone": "auto"
            },
            timeout=REQUEST_TIMEOUT
        )

        if response.status_code != 200:
            return _build_fallback_response("Open-Meteo weather service returned non-200 status code.")

        data = response.json()
        current_raw = data.get("current", {})
        hourly_raw = data.get("hourly", {})

        temp_c = float(current_raw.get("temperature_2m", 25.0))
        humidity = float(current_raw.get("relative_humidity_2m", 70.0))
        precip = float(current_raw.get("precipitation", 0.0))
        wind_kmh = float(current_raw.get("wind_speed_10m", 5.0))
        weather_code = int(current_raw.get("weather_code", 0))

        # Build 24-48 hour compact forecast summary
        hourly_temps = hourly_raw.get("temperature_2m", [])
        hourly_hums = hourly_raw.get("relative_humidity_2m", [])
        hourly_precip = hourly_raw.get("precipitation", [])

        # 24h summary
        temp_24h_max = max(hourly_temps[:24]) if len(hourly_temps) >= 24 else temp_c
        temp_24h_min = min(hourly_temps[:24]) if len(hourly_temps) >= 24 else temp_c
        precip_24h_total = sum(hourly_precip[:24]) if len(hourly_precip) >= 24 else precip

        # Evaluate disease weather favorability
        disease_eval = evaluate_weather_favorability(class_name, temp_c, humidity, precip_24h_total)

        return {
            "status": "success",
            "weather_available": True,
            "location": {
                "name": location_name or f"{latitude:.2f}, {longitude:.2f}",
                "latitude": latitude,
                "longitude": longitude,
                "timezone": data.get("timezone", "Asia/Kolkata")
            },
            "current": {
                "temperature_c": temp_c,
                "humidity_percent": humidity,
                "precipitation_mm": precip,
                "wind_kmh": wind_kmh,
                "weather_code": weather_code
            },
            "forecast_summary": {
                "next_24h": {
                    "temp_max_c": round(temp_24h_max, 1),
                    "temp_min_c": round(temp_24h_min, 1),
                    "total_precip_mm": round(precip_24h_total, 1)
                }
            },
            "disease_context": disease_eval,
            "weather_source": {
                "provider": "Open-Meteo",
                "url": "https://open-meteo.com",
                "notes": "Weather data retrieved via Open-Meteo API. Agricultural context derived from ICAR and extension guidelines."
            }
        }

    except Exception as e:
        print(f"[WEATHER SERVICE ERROR] Weather API call failed: {e}")
        return _build_fallback_response(f"Weather context temporarily unavailable ({str(e)}).")


def _build_fallback_response(message: str) -> Dict[str, Any]:
    """Generates a clean fallback response when external weather service is unreachable or errors out."""
    return {
        "status": "partial_success",
        "weather_available": False,
        "message": message,
        "disease_context": {
            "available": False,
            "favorability": "UNAVAILABLE",
            "favorability_label": "Weather Context Unavailable",
            "matched_factors": [],
            "unmatched_factors": [],
            "explanation": "Weather service is currently offline or unreachable. Diagnosis and advisory remain fully functional.",
            "disclaimer": "Weather context is supplementary and does not affect diagnosis reliability.",
            "sources": []
        },
        "weather_source": {
            "provider": "Open-Meteo",
            "url": "https://open-meteo.com"
        }
    }
