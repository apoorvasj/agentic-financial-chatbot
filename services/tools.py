from langchain_community.tools.google_finance import GoogleFinanceQueryRun
from langchain_community.utilities.google_finance import GoogleFinanceAPIWrapper
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool
from langchain_core.tools import StructuredTool
from services.prompts import rewrite_prompt
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def get_tools():
    google_tool = GoogleFinanceQueryRun(api_wrapper=GoogleFinanceAPIWrapper())
    yahoo_tool = YahooFinanceNewsTool()
    tools = [yahoo_tool, google_tool]
    return tools

def rewriter(llm):
    system = rewrite_prompt()
    re_write_prompt= ChatPromptTemplate.from_messages([
        ("system",system),
        (
            "human",
            "Here is the initial question. {question}. Formulate an improved question."
        )
    ])

    question_rewriter= re_write_prompt |llm | StrOutputParser()
    return question_rewriter