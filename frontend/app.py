import streamlit as st
from streamlit_lottie import st_lottie
import json, os, requests

# ---------- Load Lottie animation ----------
def load_lottiefile():
    filepath = os.path.join(os.path.dirname(__file__), "animation.json")
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

lottie_chatbot = load_lottiefile()

# ---------- Page Config ----------
st.set_page_config(page_title="Genzo Chatbot 💬", page_icon="🤖", layout="wide")

# ---------- Custom CSS ----------
page_bg = """
<style>
body {
    background: linear-gradient(135deg, #74ABE2, #5563DE);
    background-attachment: fixed;
    color: white;
    font-family: 'Poppins', sans-serif;
}
.chat-container {
    background-color: rgba(255,255,255,0.15);
    border-radius: 20px;
    padding: 20px;
    backdrop-filter: blur(10px);
    max-width: 800px;
    margin: auto;
    box-shadow: 0px 0px 25px rgba(255,255,255,0.3);
}
.user-bubble {
    background-color: #FFC0CB;
    color: black;
    padding: 12px 20px;
    border-radius: 20px;
    margin: 8px 0;
    text-align: right;
    animation: slideRight 0.3s ease;
}
.bot-bubble {
    background-color: #D3D3D3;
    color: black;
    padding: 12px 20px;
    border-radius: 20px;
    margin: 8px 0;
    text-align: left;
    animation: slideLeft 0.3s ease;
}
@keyframes slideLeft {
  from {opacity: 0; transform: translateX(-20px);}
  to {opacity: 1; transform: translateX(0);}
}
@keyframes slideRight {
  from {opacity: 0; transform: translateX(20px);}
  to {opacity: 1; transform: translateX(0);}
}
h1 {
    text-align: center;
    font-size: 3em;
    color: white;
    text-shadow: 0px 0px 10px #000;
}
.stTextInput input {
    border-radius: 20px;
    border: 2px solid #fff;
    padding: 12px;
    font-size: 1.1em;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ---------- Header ----------
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("<h1>🤖 Genzo Chatbot</h1>", unsafe_allow_html=True)
    st.write("Chat with your friendly AI assistant — smooth, fun, and interactive! 💬")
with col2:
    st_lottie(lottie_chatbot, height=200, key="chatbot")

# ---------- Chat Container ----------
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for msg in st.session_state["messages"]:
    bubble = "user-bubble" if msg["role"] == "user" else "bot-bubble"
    st.markdown(f"<div class='{bubble}'>{msg['content']}</div>", unsafe_allow_html=True)

# ---------- Chat Input ----------
user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    
    try:
        # ✅ Make sure this URL matches your Render backend name
        backend_url = "https://genzo-fastapi-backend.onrender.com/chat"

        response = requests.post(backend_url, json={"message": user_input})
        bot_reply = response.json().get("response", "⚠️ Backend error.")
    except Exception as e:
        bot_reply = f"⚠️ Connection error: {e}"
    
    st.session_state["messages"].append({"role": "bot", "content": bot_reply})
    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)
