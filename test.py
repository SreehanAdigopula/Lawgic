#region imports
import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
import fitz
#endregion

# Load environment variables and initialize OpenAI client
load_dotenv()
client = OpenAI()

# Main Page configuration - MUST BE FIRST
st.set_page_config(page_title="Lawgic", layout="centered", initial_sidebar_state="collapsed")

# Scroll to top on reload using JavaScript
st.markdown("""
<script>
    window.onload = function() {
        window.scrollTo(0, 0);
    }
</script>
""", unsafe_allow_html=True)

# Enhanced CSS for better user experience (cleaned and optimized)
st.markdown("""
<style>
    #MainMenu, footer, header, .stDeployButton {visibility: hidden;}
    html {scroll-behavior: smooth;}
    .stApp, .main .block-container {
        background-color: #000 !important;
        color: white !important;
        max-width: 1200px !important;
        padding: 2rem 2rem 2rem 2rem !important;
    }
    .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        text-align: center !important;
        color: white !important;
    }
    .stMarkdown h1 {
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        letter-spacing: 2px !important;
        margin-bottom: 0.5rem !important;
        font-family: 'Times New Roman', serif !important;
    }
    .stMarkdown h2 {
        font-size: 2.5rem !important;
        margin: 2rem 0 1.5rem 0 !important;
        color: #f0f0f0 !important;
    }
    .stMarkdown p {
        font-size: 1.2rem !important;
        line-height: 1.8 !important;
        color: #e0e0e0 !important;
        max-width: 800px !important;
        margin: 0 auto 1.5rem auto !important;
    }
    .stButton button {
        background-color: #333 !important;
        color: white !important;
        border: 2px solid #555 !important;
        border-radius: 25px !important;
        padding: 12px 30px !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    .stButton button:hover {
        background-color: #555 !important;
        border-color: #777 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(255,255,255,0.1) !important;
    }
    .stExpander {
        background-color: #1a1a1a !important;
        border: 1px solid #333 !important;
        border-radius: 10px !important;
    }
    .stExpander:hover {border-color: #555 !important;}
    .stFileUploader:hover {background-color: #2a2a2a !important;}
    .stMarkdown {animation: fadeIn 0.8s ease-in-out !important;}
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# ------------------ HEADER ------------------
st.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <h1 style="font-size: 5rem; font-family: 'Georgia', serif; font-weight: 900; color: #FBE8C6; margin-bottom: 0.3rem;">
        👨‍⚖️ LAWGIC
    </h1>
    <h3 style="font-size: 1.7rem; font-family: 'Segoe UI', sans-serif; font-weight: 400; color: #D8C7AE;">
        Free Legal Advice for Everyone
    </h3>
</div>
""", unsafe_allow_html=True)

# ------------------ INTRO ------------------
st.markdown("""
<div style="height: 40px;"></div>
<div style="padding: 40px 30px; background-color: #1A120B; border-radius: 15px; text-align: center;">
    <h2 style="font-size: 2.8rem; color: #FBE8C6; margin-bottom: 1rem;">What is LAWGIC?</h2>
    <p style="font-size: 1.2rem; color: #E6D3B3; line-height: 1.8; max-width: 800px; margin: auto;">
        LAWGIC is an AI-powered legal chatbot designed to make legal information
        accessible to everyone — especially those who can't afford a lawyer.
        Through a simple, user-friendly chat interface, LAWGIC provides instant,
        plain-language answers to common legal questions in areas like housing,
        employment, and immigration.
        <br><br>
        While it doesn't replace a lawyer, it helps users understand their rights,
        find trusted legal resources, and take the first steps toward resolving
        their issues. Built for impact and simplicity, LAWGIC is legal help —
        without the legal bills.
    </p>
</div>
<div style="height: 80px;"></div>
""", unsafe_allow_html=True)

# ------------------ PDF UPLOAD ------------------
with st.expander("📎 Upload a legal PDF (optional)"):
    uploaded_file = st.file_uploader("Choose PDF", type=["pdf"])

if uploaded_file:
    pdf_text = ""
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    for page in doc:
        pdf_text += page.get_text()
    doc.close()

    st.success("✅ Document uploaded and read successfully.")
    st.text_area("📝 Extracted Text Preview", pdf_text[:1500] + ("..." if len(pdf_text) > 1500 else ""), height=200)

    st.session_state.messages.append({
        "role": "system",
        "content": "This is the uploaded legal document content:\n\n" + pdf_text[:3000]
    })

# Spacer before chat
st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)

# ------------------ CHAT ------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Lawgic, a helpful lawyer who answers in plain English."}
    ]

# Display previous messages
for msg in st.session_state.messages[1:]:
    st.chat_message(msg["role"]).write(msg["content"])

# Chat input
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
