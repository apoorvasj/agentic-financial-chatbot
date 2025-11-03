from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import Literal
from services.prompts import retrieval_grade_prompt

#Data Model

class GradeDocuments(BaseModel):
    """Binary score for relevance check on retrieved documents."""

    binary_score: Literal["yes","no"]= Field(
        description="Documents are relevant to the question, 'yes' or 'no' "
    )

def grade_documents(llm):
    #LLM with function call
    structured_llm_grader= llm.with_structured_output(GradeDocuments)

    #Prompt
    system= retrieval_grade_prompt()

    grade_prompt = ChatPromptTemplate.from_messages([
        ("system",system),
        ("human", "Retrieved document: {document}. User question: {question}")
    ])

    retrieval_grader= grade_prompt|structured_llm_grader
    return retrieval_grader