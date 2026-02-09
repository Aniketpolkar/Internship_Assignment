from google import genai
import os
# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client(api_key=os.environ(GEMINI_API_KEY))

while True:
    user = input("You: ")
    if user.lower() in ["bye", "exit", "quit"]:
        print("Bot: Goodbye!")
        break

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=user
    )

    print("Bot:", response.text)