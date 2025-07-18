# backend/app/agent/graph.py

from typing import Annotated
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from app.tools.calendar_tools import check_availability, book_appointment
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# Define the state for our graph
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# Initialize tools and the LLM
tools = [check_availability, book_appointment]
tool_node = ToolNode(tools)
model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest",
    temperature=0,
    google_api_key=os.getenv("GEMINI_API_KEY") # This is the crucial addition
)
model = model.bind_tools(tools)

# Define the function that determines whether to continue or not
def should_continue(state: AgentState) -> str:
    messages = state['messages']
    last_message = messages[-1]
    # If there are no tool calls, then we finish
    if not last_message.tool_calls:
        return "end"
    # Otherwise if there are, we continue
    else:
        return "continue"

# Define the function that calls the model
def call_model(state: AgentState):
    messages = state['messages']
    response = model.invoke(messages)
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}

# Define the graph
workflow = StateGraph(AgentState)

# Define the two nodes we will cycle between
workflow.add_node("agent", call_model)
workflow.add_node("action", tool_node)

# Set the entrypoint as `agent`
# This means that this node is the first one called
workflow.set_entry_point("agent")

# We now add a conditional edge
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "action",
        "end": "__end__",
    },
)

# We now add a normal edge from `tools` to `agent`.
# This means that after `tools` is called, `agent` will be called next.
workflow.add_edge("action", "agent")

# Finally, we compile it!
# This compiles it into a LangChain Runnable,
# meaning you can use it as you would any other runnable
agent_graph = workflow.compile()