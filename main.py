from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain.schema import HumanMessage
from langgraph_agent import agent

app = FastAPI()

# Allow CORS for frontend (React) running on localhost:3000
origins = [
    "http://localhost:3000",  # React dev server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow requests from React
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def get_response(request: QueryRequest):
    task = request.query
    state = {"messages": [HumanMessage(content=task)], "iteration": 0}
    final_state = agent.invoke(state)
    
    # Extract LLM response
    response = ""
    for msg in final_state["messages"]:
        if not isinstance(msg, HumanMessage):  # Only get AI responses
            response += msg.content + "\n"
    return {"response": response.strip()}
