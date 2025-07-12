#region imports
import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
#endregion

load_dotenv()
client = OpenAI()

st.set_page_config(page_title="Lawgic", layout="centered")
st.title("⚖️ Lawgic")
st.caption("Legal help for underprivileged communities")

# Store message history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Lawgic, a helpful lawyer who answers in plain English."}
    ]

# Show past messages
for msg in st.session_state.messages[1:]:
    st.chat_message(msg["role"]).write(msg["content"])

# Input
user_input = st.chat_input("What's your legal question?")

if user_input:
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
            model="o4-mini",
            messages=st.session_state.messages
        )
        reply = response.choices[0].message.content
        st.chat_message("assistant").write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
