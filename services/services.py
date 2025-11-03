from state.state import State

def decide_to_generate(state:State):
    """
    Determines whether to generate an answer, or re-generate a question.

    Args:
        state (dict): The current graph state

    Returns:
        str: Binary decision for next node to call
    """
    
    decision = state.get("re_gen_required")
    if decision == "yes":
        return "rewrite_query"
    elif decision == "no":
        return "generate"
    else:
        raise ValueError(f"Unexpected or missing value for 're_gen_required': {decision}")
    
def correct_hallucination(state:State):
    """
    Determines whether the current generation has hallucination present.

    Args:
        state (dict): The current graph state
    
    Returns:
        str: Binary decision for next node to call
    """

    decision= state["hallucination_present"]
    if(decision== "yes"):
        return "regenerate"
    else:
        return "end"