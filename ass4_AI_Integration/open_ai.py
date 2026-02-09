import requests
import os
from dotenv import load_dotenv

load_dotenv()

WEATHERAPI_KEY = os.getenv("WEATHERAPI_KEY")

def get_weather(location: str):
    """
    Fetch current weather from weatherapi.com
    """
    url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "key": WEATHERAPI_KEY,
        "q": location,
        "aqi": "no"
    }

    response = requests.get(url, params=params)
    data = response.json()

    return {
        "location": data["location"]["name"],
        "country": data["location"]["country"],
        "temperature_c": data["current"]["temp_c"],
        "condition": data["current"]["condition"]["text"]
    }

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a given city using WeatherAPI.com",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name, e.g. London, Paris, Mumbai"
                    }
                },
                "required": ["location"]
            }
        }
    }
]

from openai import OpenAI

client = OpenAI(api_key="OPENAI_API_KEY")  # uses OPENAI_API_KEY from environment

messages = [
    {"role": "user", "content": "What is the weather in Paris?"}
]

response = client.chat.completions.create(
    model="gpt-4.1",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)


message = response.choices[0].message

if message.tool_calls:
    tool_call = message.tool_calls[0]
    args = tool_call.function.arguments

    weather_data = get_weather(**args)

    messages.append(message)
    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "name": "get_weather",
        "content": str(weather_data)
    })

    final_response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages
    )

    print(final_response.choices[0].message.content)


