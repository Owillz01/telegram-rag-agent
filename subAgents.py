from langchain.tools import tool
from langchain.agents import create_agent
from tools import tavilySearch

webSearchAgent = create_agent(
        model="openai:gpt-5.5", 
        tools=[tavilySearch],
)

@tool("webSearch", description="Search the web and return findings")
def webSearchSubAgent(query: str) -> str:
    result = webSearchAgent.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-2]