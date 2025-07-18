# backend/app/main.py

import uuid
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langgraph.checkpoint.memory import MemorySaver
from app.agent.graph import agent_graph
from langchain_core.messages import HumanMessage
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="TailorTalk Agent Server",
    version="1.0",
    description="A FastAPI server for the TailorTalk conversational agent.",
)

# CORS configuration
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for conversation checkpoints
# In a production environment, you would replace this with a persistent store like Redis or a database
memory_checkpoints = {}

class ChatRequest(BaseModel):
    session_id: str | None = None
    message: str

class ChatResponse(BaseModel):
    response: str
    session_id: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Handles a chat request, manages conversation state, and returns the agent's response.
    """
    session_id = request.session_id or str(uuid.uuid4())
    
    # Get or create a memory checkpointer for the session
    if session_id not in memory_checkpoints:
        memory_checkpoints[session_id] = MemorySaver()
    
    checkpointer = memory_checkpoints[session_id]
    
    # Configuration for the LangGraph agent
    config = {"configurable": {"thread_id": session_id, "checkpointer": checkpointer}}
    
    # Prepare the input for the agent
    inputs = [HumanMessage(content=request.message)]
    
    # Invoke the agent graph
    final_state = agent_graph.invoke({"messages": inputs}, config)
    
    # The final response is the last message from the assistant
    response_message = final_state["messages"][-1].content
    
    return ChatResponse(response=response_message, session_id=session_id)

@app.get("/")
def read_root():
    return {"message": "Welcome to the TailorTalk Agent API"}