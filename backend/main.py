from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from openai import OpenAI
import os
import sqlite3

# ---------- Load environment variables ----------
load_dotenv()

app = FastAPI()

# ---------- Allow all origins (for Streamlit frontend) ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this later to your Streamlit domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Connect to SQLite database ----------
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

# ---------- Initialize Groq client ----------
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),
)

# ---------- Root route ----------
@app.get("/")
def home():
    return {"message": "✅ Genzo FastAPI backend is running successfully!"}

# ---------- Chat route ----------
@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "")

    if not user_message.strip():
        return {"response": "⚠️ Please enter a valid message."}

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are Genzo, a friendly AI assistant."},
                {"role": "user", "content": user_message},
            ],
        )
        bot_reply = completion.choices[0].message.content
    except Exception as e:
        bot_reply = f"⚠️ AI model error: {e}"

    # ---------- Save conversation ----------
    cursor.execute(
        "INSERT INTO chats (user_message, bot_reply) VALUES (?, ?)",
        (user_message, bot_reply)
    )
    conn.commit()

    return {"response": bot_reply}
