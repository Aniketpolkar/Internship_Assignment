# def query_clinical_knowledge(symptoms: str) -> str:
#     """
#     Mock clinical knowledge lookup.
#     Replace with real APIs (UpToDate, NICE, CDC, etc).
#     """

#     symptoms_lower = symptoms.lower()

#     if "fever" in symptoms_lower and "cough" in symptoms_lower:
#         return (
#             "Possible causes include viral respiratory infection. "
#             "General guidance suggests rest, hydration, and monitoring symptoms."
#         )

#     if "chest pain" in symptoms_lower:
#         return (
#             "Chest pain may indicate a serious condition. "
#             "Immediate medical evaluation is recommended."
#         )

#     return (
#         "Symptoms are non-specific. General advice includes rest, hydration, "
#         "and seeking medical attention if symptoms worsen."
#     )

import os
import requests

RAPIDAPI_KEY = "16418ff01amsh4606eb3d625843ap129d60jsndf1404cb0494"

API_URL = "https://ai-doctor-api-ai-medical-chatbot-healthcare-ai-assistant.p.rapidapi.com/chat"

HEADERS = {
    "content-type": "application/json",
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": "ai-doctor-api-ai-medical-chatbot-healthcare-ai-assistant.p.rapidapi.com"
}

def query_clinical_knowledge(symptoms: str) -> str:
    """
    Clinical knowledge lookup using AI Doctor RapidAPI.
    This is NOT a medical diagnosis.
    """

    payload = {
        "message": symptoms,
        "language": "en"
    }

    try:
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json=payload,
            timeout=15
        )

        if response.status_code != 200:
            return "Unable to retrieve clinical information at this time."

        data = response.json()

        # API usually returns a 'response' or 'answer' field
        return data.get("response") or data.get("answer") or "No clinical advice available."

    except requests.exceptions.RequestException:
        return "Clinical service is currently unavailable."
