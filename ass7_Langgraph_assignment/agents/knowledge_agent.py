from services.knowledge_api import query_clinical_knowledge

def knowledge_agent(state):
    """
    Calls the clinical knowledge API using symptoms.
    """
    symptoms = state.get("symptoms")
    if not symptoms:
        return state

    knowledge = query_clinical_knowledge(symptoms)
    state["knowledge"] = knowledge
    state["messages"].append(f"Knowledge retrieved: {knowledge}")

    return state
