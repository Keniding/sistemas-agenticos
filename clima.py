from typing import Annotated

import httpx
from agent_framework import tool
from pydantic import Field

WEATHER_CODES = {
    0: "despejado", 1: "mayormente despejado", 2: "parcialmente nublado",
    3: "nublado", 45: "niebla", 48: "niebla con escarcha",
    51: "llovizna ligera", 53: "llovizna moderada", 55: "llovizna intensa",
    61: "lluvia ligera", 63: "lluvia moderada", 65: "lluvia intensa",
    71: "nevada ligera", 73: "nevada moderada", 75: "nevada intensa",
    80: "chubascos ligeros", 81: "chubascos moderados", 82: "chubascos violentos",
    95: "tormenta eléctrica",
}

@tool(approval_mode="never_require")
async def get_weather(
        location: Annotated[str, Field(description="The location for which to retrieve the weather.")]
) -> str:
    """Get the real current weather for a given location using Open-Meteo."""
    async with httpx.AsyncClient(timeout=10) as http_client:
        geo_resp = await http_client.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": location, "count": 1, "language": "en", "format": "json"},
        )
        results = geo_resp.json().get("results")
        if not results:
            return f"No pude encontrar la ubicación '{location}'."

        place = results[0]
        lat, lon = place["latitude"], place["longitude"]
        display_name = f"{place['name']}, {place.get('country', '')}".strip(", ")

        weather_resp = await http_client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={"latitude": lat, "longitude": lon, "current_weather": True},
        )
        current = weather_resp.json().get("current_weather")
        if not current:
            return f"No pude obtener el clima para {display_name}."

        condition = WEATHER_CODES.get(current["weathercode"], "condición desconocida")
        return (
            f"El clima en {display_name} es {condition}, "
            f"{current['temperature']}°C, viento a {current['windspeed']} km/h."
        )
