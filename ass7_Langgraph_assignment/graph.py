from langgraph.graph import StateGraph, END
from state import ClinicalState

from agents.symptom_agent import symptom_agent
from agents.knowledge_agent import knowledge_agent
from agents.advice_agent import advice_agent

def build_graph():
    workflow = StateGraph(ClinicalState)

    workflow.add_node("collect_symptoms", symptom_agent)
    workflow.add_node("fetch_knowledge", knowledge_agent)
    workflow.add_node("generate_advice", advice_agent)

    workflow.set_entry_point("collect_symptoms")

    workflow.add_edge("collect_symptoms", "fetch_knowledge")
    workflow.add_edge("fetch_knowledge", "generate_advice")
    workflow.add_edge("generate_advice", END)

    return workflow.compile()
