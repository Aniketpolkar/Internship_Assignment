def symptom_agent(state):
    """
    Ask the user about symptoms if not already provided.
    """
    if state.get("symptoms"):
        return state

    print("\nClinical Assistant:")
    symptoms = input("Please describe your symptoms in detail: ")

    state["symptoms"] = symptoms
    state["messages"].append(f"User symptoms: {symptoms}")
    return state
