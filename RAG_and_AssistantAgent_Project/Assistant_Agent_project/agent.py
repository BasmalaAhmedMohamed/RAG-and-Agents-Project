from dotenv import load_dotenv
import os
from langchain.agents import create_agent
from tools import ALL_TOOLS
from langgraph.checkpoint.memory import InMemorySaver
from langchain_openai import ChatOpenAI
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver


load_dotenv()

try:
    model_name = os.getenv("openai_model")
    openai_key = os.getenv("openai_key")
except Exception as error:
    print(f"Error while loading the model from .env file: {error}")


model = ChatOpenAI(model=model_name, temperature=0.2, api_key=openai_key)

SYSTEM_PROMPT = "use tools if you need it to answer the user query, remember earlier messages, answer briefly. If you use ask_documents tool, answer with the same return from the tool with Source file names and citations that after paragraphs in square brackets."


def build_agent():
    agent = create_agent(model=model, tools=ALL_TOOLS, system_prompt=SYSTEM_PROMPT, checkpointer=InMemorySaver())
    return agent



def build_remembered_agent(db_path: str = "agent_checkpoints.db"):
    connection = sqlite3.connect(db_path, check_same_thread=False)
    checkpointer = SqliteSaver(connection)
    
    agent = create_agent(model=model, tools=ALL_TOOLS, system_prompt=SYSTEM_PROMPT, checkpointer=checkpointer)
    
    return agent