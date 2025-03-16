import os
from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from tavily import TavilyClient
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal
from langchain_core.messages import ToolMessage, SystemMessage, HumanMessage, AIMessage

# Set API Keys
os.environ["OPENAI_API_KEY"] = "enter your api here"
os.environ["TAVILY_API_KEY"] = "enter your api here"

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o", max_tokens=300, temperature=0.5)

# Define Tools
@tool
def web_search(query):
    """Performs a web search using Tavily API."""
    try:
        client = TavilyClient()
        return client.search(query=query.strip('"'), search_depth="advanced", max_results=5)
    except Exception as e:
        return {"error": str(e)}

@tool
def calculator(math_expression):
    """Evaluates a mathematical expression."""
    try:
        return eval(math_expression)
    except Exception as e:
        return {"error": str(e)}

# Bind Tools
tools = [web_search, calculator]
tools_by_name = {tool.name: tool for tool in tools}
llm_with_tools = llm.bind_tools(tools)

# System Message for LLM
system_msg = """
You are a cricket research assistant. Your responses must be short, precise, and directly relevant.  

### Guidelines:
- **Concise Output:** Summarize findings in 3-4 bullet points. Avoid unnecessary details.
- **Actionable Insights:** Highlight match-winning moments, key stats, and trends.
- **No Redundancy:** Avoid repeating information across iterations.
- **Data Accuracy:** Use verified sources. Ignore outdated/unverified claims.
"""


# Define Research State
class ResearchState(TypedDict):
    messages: list
    iteration: int

MAX_ITERATIONS = 2

# Define LLM Call Node
def llm_call(state: ResearchState):
    new_messages = state["messages"] + [
        llm_with_tools.invoke([SystemMessage(content=system_msg)] + state["messages"])
    ]
    return {"messages": new_messages, "iteration": state["iteration"]}

# Define Tool Node
def tool_node(state: ResearchState):
    result = [ToolMessage(content=tools_by_name[tc["name"]].invoke(tc["args"]), tool_call_id=tc["id"]) for tc in state["messages"][-1].tool_calls]
    return {"messages": state["messages"] + result, "iteration": state["iteration"] + 1}

# Stopping Condition
def should_continue(state: ResearchState) -> Literal["Action", END]:
    return "Action" if state["iteration"] < MAX_ITERATIONS else END

# Build Agent Graph
agent_builder = StateGraph(ResearchState)
agent_builder.add_node("llm_call", llm_call)
agent_builder.add_node("environment", tool_node)
agent_builder.add_edge(START, "llm_call")
agent_builder.add_conditional_edges("llm_call", should_continue, {"Action": "environment", END: END})
agent_builder.add_edge("environment", "llm_call")
agent = agent_builder.compile()

# Task Input
task = """
Research and summarize key moments of the 2025 ICC World Cup final match between India and New Zealand, including:
- Notable performances by key players (e.g., Virat Kohli, Rohit Sharma, etc.).
- Match-winning moments and their impact.
- Brief match statistics: wickets, runs, and turning points.
"""

# Invoke Agent
state = {"messages": [HumanMessage(content=task)], "iteration": 0}
final_state = agent.invoke(state)


# Extract only the final AI response
# Extract only AI-generated responses
llm_responses = [
    msg.content for msg in final_state["messages"] if isinstance(msg, AIMessage)
]

# Print only the last LLM response (or modify for more control)
if llm_responses:
    print(llm_responses[-1])  # Print only the last response

