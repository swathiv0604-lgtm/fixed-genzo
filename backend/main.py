from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from openai import OpenAI
import os
import sqlite3

# Load environment variables
load_dotenv()

app = FastAPI()

# Allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to DB
conn = sqlite3.connect("chat_history.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS chats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_message TEXT,
    bot_reply TEXT
)
""")
conn.commit()

# Groq client setup
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),
)

@app.get("/")
def home():
    return {"message": "✅ Genzo FastAPI backend is running successfully!"}

@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        user_message = data.get("message", "")

        if not user_message:
            return {"response": "⚠️ Please send a valid message."}

        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are Genzo, a friendly AI assistant."},
                {"role": "user", "content": user_message},
            ],
        )
        bot_reply = completion.choices[0].message.content

        cursor.execute(
            "INSERT INTO chats (user_message, bot_reply) VALUES (?, ?)",
            (user_message, bot_reply)
        )
        conn.commit()

        return {"response": bot_reply}

    except Exception as e:
        return {"response": f"⚠️ Backend error: {e}"}
