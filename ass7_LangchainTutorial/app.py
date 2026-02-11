from google import genai
import os

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

response = client.models.generate_content(
    model="gemini-2.5-flash-lite-preview-09-2025",
    contents="Where is Pune?"
)
print(response.text)
