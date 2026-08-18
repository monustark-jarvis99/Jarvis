import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def internet_search(query):
    url = "https://tavily.com"
    payload = {"api_key": TAVILY_API_KEY, "query": query, "include_answer": True}
    try:
        response = requests.post(url, json=payload).json()
        return response.get("answer", "No live internet data found, Sir.")
    except Exception:
        return "I am facing some network issues fetching live data, Sir."

@app.post("/ask_jarvis")
async def ask_jarvis(request: Request):
    data = await request.json()
    user_message = data.get("message")
    
    live_context = internet_search(user_message)
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system", 
                "content": (
                    "Aapka naam JARVIS hai. Aap Iron Man (Tony Stark) ke ultra-intelligent AI assistant hain. "
                    "Aapka baat karne ka tareeqa behad respectful, calm, aur sharp hona chahiye. "
                    "User ko hamesha 'Sir' keh kar sambodhit karein. Aapki bhasha Hinglish (Hindi + English mix) "
                    "honi chahiye jo sunne me natural aur hi-tech lage. Lambe jawab na dein, bilkul punchy aur accurate "
                    f"baat karein. Is live internet data ka use karke jawab taiyar karein: {live_context}"
                )
            },
            {"role": "user", "content": user_message}
        ]
    )
    
    jarvis_reply = response.choices.message.content
    return {"reply": jarvis_reply}
