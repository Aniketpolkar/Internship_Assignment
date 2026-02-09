def advice_agent(state):
    """
    Generates safe, non-diagnostic advice.
    """
    knowledge = state.get("knowledge")
    symptoms = state.get("symptoms")

    if not knowledge or not symptoms:
        return state

    advice = f"""
Based on the information provided:

Symptoms:
- {symptoms}

General medical information:
- {knowledge}

Important:
- This is not a diagnosis.
- If symptoms worsen, persist, or include severe pain, shortness of breath,
  confusion, or chest pain, seek immediate medical care.
"""

    state["advice"] = advice.strip()
    state["messages"].append("Advice generated.")

    return state
