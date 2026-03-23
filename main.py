# Project 01 
# AI Chatbot

# step 1 
# Import Libraries
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain_core.chat_history import InMemoryChatMessageHistory

#  step 3
#  Setup

load_dotenv()

app=FastAPI()

llm=ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))


# step 3 
# Memory
store={}
def chat_history(session_id: str):
    if session_id not in store:
        store[session_id]=InMemoryChatMessageHistory()
    return store[session_id]


#  step 4
# Request Model and CORS Middleware

class ChatRequest(BaseModel):
    message: str


app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_headers=["*"],
                   allow_methods=["*"])


# step 5
# Routes

@app.get("/")
def home():
    return {"response":"AI working"}


@app.post("/chat")
def chat(req: ChatRequest):
   try:
        history=chat_history("default")
        messages=list(history.messages)+[("human",req.message)]
        response=llm.invoke(messages)
        reply=response.content
        history.add_user_message(req.message)
        history.add_ai_message(reply)
        return{"reply":reply}
   except Exception as e:
       return {"reply": f"something went wrong: {str(e)}"}