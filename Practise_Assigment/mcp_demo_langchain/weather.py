from mcp.server.fastmcp import FastMCP
import requests
from db import forts_collection
mcp = FastMCP("MCPServer")

# WEATHER_API = "https://wttr.in/pune"
@mcp.tool()
def get_weather(location:str)->str:
    """Get the weather for a given location"""
    response = requests.get(f"https://wttr.in/{location}")
    response.raise_for_status()
    # ?format=%C+%t
    # data = response.json()
    # filter weather by city
    # return f"The weather in {location} is {data}"
    return response.text


API_URL = "https://www.arbeitnow.com/api/job-board-api"

@mcp.tool()
def get_jobs(location: str) -> dict:
    """
    Get job listings for a location
    """
    response = requests.get(API_URL)
    response.raise_for_status()

    data = response.json()

    # Filter jobs by location (case-insensitive)
    jobs = [
        {
            "title": job["title"],
            "company": job["company_name"],
            "location": job["location"],
            "url": job["url"]
        }
        for job in data.get("data", [])
        if location.lower() in job["location"].lower()
    ]

    return {
        "location": location,
        "count": len(jobs),
        "jobs": jobs[:5]  # limit results
    }


# Tool: get_forts
@mcp.tool(name="get_forts", description="Fetch forts from MongoDB by state or limit")
def get_forts(state: str = None, limit: int = 10):
    query = {}
    if state:
        query["location.state"] = state

    fort = list(forts_collection.find(query, {"_id": 0}).limit(limit))
    return fort
if __name__ == "__main__":
    mcp.run(transport="streamable-http")