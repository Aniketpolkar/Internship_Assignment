from typing import TypedDict, Optional, List

class ClinicalState(TypedDict):
    symptoms: Optional[str]
    knowledge: Optional[str]
    advice: Optional[str]
    messages: List[str]
