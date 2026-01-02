from fastmcp import FastMCP
mcp = FastMCP("Weather")

@mcp.tool()
def get_weather(city: str = "New York") -> str:
    "Get the current weather for a given city"
    # In a real implementation, you would call a weather API here.
    # For demonstration purposes, we'll return a mock response.
    mock_weather_data = {
        "New York": "Sunny, 75°F",
        "Los Angeles": "Cloudy, 68°F",
        "Chicago": "Rainy, 60°F"
    }
    return mock_weather_data.get(city, "Weather data not available for this city.")

if __name__ == "__main__":
    mcp.run(transport="streamable-http")