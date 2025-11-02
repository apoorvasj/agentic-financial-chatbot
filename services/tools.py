from langchain_community.tools.google_finance import GoogleFinanceQueryRun
from langchain_community.utilities.google_finance import GoogleFinanceAPIWrapper
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool
from langchain_core.tools import StructuredTool

def get_tools():
    google_tool = GoogleFinanceQueryRun(api_wrapper=GoogleFinanceAPIWrapper())
    yahoo_tool = YahooFinanceNewsTool()
    tools = [yahoo_tool, google_tool]
    return tools

