from google import genai
from google.genai import types
import requests
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

def get_current_temperature(location: str):
    url = "https://api.weatherapi.com/v1/current.json"
    params = {
        "key": WEATHER_API_KEY,
        "q": location,
        "aqi": "no"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "error" in data:
        return {"error": data["error"]["message"]}

    return {
        "location": data["location"]["name"],
        "country": data["location"]["country"],
        "temperature_c": data["current"]["temp_c"],
        "condition": data["current"]["condition"]["text"]
    }

weather_function = {
    "name": "get_current_temperature",
    "description": "Gets the current temperature for a given city using WeatherAPI.com",
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

tools = types.Tool(function_declarations=[weather_function])
config = types.GenerateContentConfig(tools=[tools])

st.set_page_config(page_title="Gemini Weather App", layout="centered")

st.title("🌤️ Gemini Weather Assistant")
st.write("Ask for the current temperature in any city.")

city = st.text_input("Enter a city name", placeholder="London")

if st.button("Get Temperature") and city:
    with st.spinner("Thinking..."):
        
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=f"What is the temperature in {city}?",
            config=config
        )

        part = response.candidates[0].content.parts[0]

        if part.function_call:
            function_call = part.function_call

            weather_result = get_current_temperature(**function_call.args)

            followup = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=[
                    f"What is the temperature in {city}?",
                    types.Content(
                        role="tool",
                        parts=[
                            types.Part(
                                function_response=types.FunctionResponse(
                                    name=function_call.name,
                                    response=weather_result
                                )
                            )
                        ]
                    )
                ]
            )
            st.success("Result")
            st.markdown(f"### {followup.text}")
        else:
            st.warning("No function call was triggered.")
            st.write(response.text)
