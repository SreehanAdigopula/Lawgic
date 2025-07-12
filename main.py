#region imports
import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
import fitz
#endregion
load_dotenv()
client = OpenAI()

# Main Page configuration - MUST BE FIRST
st.set_page_config(page_title="Lawgic", layout="centered", initial_sidebar_state="collapsed")

# Enhanced CSS for better user experience
st.markdown("""
<style>
    #MainMenu, footer, header, .stDeployButton {visibility: hidden;}
    
    /* Smooth scrolling for the entire page */
    html {
        scroll-behavior: smooth;
    }
    
    .stApp {
        background-color: #000000 !important;
        color: white !important;
    }
    
    .main .block-container {
        background-color: #000000 !important;
        color: white !important;
        max-width: 1200px !important;
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }
    
    /* Center all text content */
    .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        text-align: center !important;
        color: white !important;
    }
    
    /* Enhanced typography */
    .stMarkdown h1 {
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        letter-spacing: 2px !important;
        margin-bottom: 0.5rem !important;
        font-family: 'Times New Roman', serif !important;
    }
    
    .stMarkdown h2 {
        font-size: 2.5rem !important;
        font-weight: 600 !important;
        margin: 2rem 0 1.5rem 0 !important;
        color: #f0f0f0 !important;
    }
    
    .stMarkdown p {
        font-size: 1.2rem !important;
        line-height: 1.8 !important;
        color: #e0e0e0 !important;
        margin-bottom: 1.5rem !important;
        max-width: 800px !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }
    
    /* Smooth button transitions */
    .stButton button {
        background-color: #333 !important;
        color: white !important;
        border: 2px solid #555 !important;
        border-radius: 25px !important;
        padding: 12px 30px !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        transform: translateY(0) !important;
    }
    
    .stButton button:hover {
        background-color: #555 !important;
        border-color: #777 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(255,255,255,0.1) !important;
    }
    
    /* Chat components with smooth animations */
    .stChatMessage {
        background-color: #222 !important;
        color: white !important;
        border-radius: 10px !important;
        transition: all 0.2s ease !important;
    }
    
    .stChatMessage:hover {
        background-color: #333 !important;
    }
    
    .stChatInput input {
        background-color: #1a1a1a !important;
        color: white !important;
        border: 1px solid #555 !important;
        border-radius: 20px !important;
        transition: border-color 0.3s ease !important;
    }
    
    .stChatInput input:focus {
        border-color: #777 !important;
        box-shadow: 0 0 0 2px rgba(255,255,255,0.1) !important;
    }
    
    .stExpander {
        background-color: #1a1a1a !important;
        border: 1px solid #333 !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
    }
    
    .stExpander:hover {
        border-color: #555 !important;
    }
    
    .stTextArea textarea {
        background-color: #1a1a1a !important;
        color: white !important;
        border: 1px solid #555 !important;
        border-radius: 10px !important;
        transition: border-color 0.3s ease !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #777 !important;
        box-shadow: 0 0 0 2px rgba(255,255,255,0.1) !important;
    }
    
    .stFileUploader {
        background-color: #1a1a1a !important;
        color: white !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
    }
    
    .stFileUploader:hover {
        background-color: #2a2a2a !important;
    }
    
    /* Smooth fade-in animation for content */
    .stMarkdown {
        animation: fadeIn 0.8s ease-in-out !important;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Add subtle gradient for visual depth */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at 50% 50%, rgba(255,255,255,0.02) 0%, transparent 70%);
        pointer-events: none;
        z-index: 1;
    }
    
    /* Ensure content is above the gradient */
    .main .block-container {
        position: relative;
        z-index: 2;
    }
</style>
""", unsafe_allow_html=True)

# Create enhanced landing page with better UX
st.markdown("")
st.markdown("")  # Extra spacing at top

st.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <h1 style="font-size: 5rem; font-family: 'Georgia', serif; font-weight: 900; color: #FBE8C6; margin-bottom: 0.3rem;">
        👨‍⚖️ LAWGIC ⚖️
    </h1>
    <h3 style="font-size: 1.7rem; font-family: 'Segoe UI', sans-serif; font-weight: 400; color: #D8C7AE;">
        Free Legal Advice for Everyone
    </h3>
</div>
""", unsafe_allow_html=True)

# Add more spacing for better visual hierarchy
st.markdown("")
st.markdown("")
st.markdown("")
st.markdown("")

# Main content section - all centered
st.markdown("## What is LAWGIC?")

st.markdown("")  # Spacing after header

# Description paragraphs - will be centered by CSS
st.markdown("""
LAWGIC is an AI-powered legal chatbot designed to make legal information
accessible to everyone — especially those who can't afford a lawyer.
Through a simple, user-friendly chat interface, LAWGIC provides instant,
plain-language answers to common legal questions in areas like housing,
employment, and immigration.
""")

st.markdown("""
While it doesn't replace a lawyer, it helps users understand their rights,
find trusted legal resources, and take the first steps toward resolving
their issues. Built for impact and simplicity, LAWGIC is legal help —
without the legal bills.
""")

st.markdown("")
st.markdown("")  # Extra spacing before button


# Add generous spacing between landing page and chat section
st.markdown("")
st.markdown("")
st.markdown("")
st.markdown("")
st.markdown("")
st.markdown("")
st.markdown("")
st.markdown("")

# Main Page configuration
st.set_page_config(page_title="Lawgic", layout="centered", initial_sidebar_state="collapsed")

# Title and subtitle
st.markdown("""
<div class="main-header">
   <div class="logo-subtitle">
    <h2 style="font-size: 1.7rem; font-weight: 600; color: #FBE8C6; margin-bottom: 0.3rem;">
        How Can I Help?
    </h2>
    <p style="font-size: 1.1rem; color: #E6D3B3; font-family: 'Segoe UI', sans-serif;">
        Got a legal question? I'm here to help — just ask away! ⚖️
    </p>
</div>
</div>
""", unsafe_allow_html=True)

# ----- Custom CSS -----
st.markdown("""
<style>
    #MainMenu, footer, header, .stDeployButton {visibility: hidden;}

    .stApp {
        background-color: #000000;
        color: white;
        font-family: 'Segoe UI', sans-serif;
    }

    .main-header {
        text-align: center;
        padding: 2rem 0 1rem 0;
        color: white;
    }

    .logo-title {
        font-size: 3rem;
        font-weight: 800;
        font-family: 'Times New Roman', serif;
        letter-spacing: 2px;
        color: white;
    }

    .logo-subtitle {
        font-size: 1.3rem;
        color: #bbbbbb;
        font-family: 'Segoe UI', sans-serif;
        margin-top: -0.5rem;
    }

    .chat-container {
        background: #111111;
        border-radius: 15px;
        padding: 0rem;
        box-shadow: 0 8px 25px rgba(255, 255, 255, 0.05);
        margin: 1.5rem 0;
    }

    .stChatMessage.user, .stChatMessage.assistant {
        background-color: #1a1a1a !important;
        color: white !important;
        border-radius: 20px !important;
        padding: 0 !important;  /* ✅ Removed padding */
        margin: 1rem 0 !important;
        border: 1px solid #333 !important;
        font-size: 1rem !important;
        line-height: 1.6 !important;
        transition: all 0.25s ease-in-out !important;
        display: flex !important;
        gap: 0.75rem !important;
        align-items: flex-start !important;
        animation: fadeIn 0.4s ease-in-out;
    }

    input[type="text"] {
        padding: 0 rem !important;
        border-radius: 10px !important;
        border: 1px solid #666666 !important;
        font-size: 1rem !important;
        background-color: #1a1a1a !important;
        color: white !important;
    }

    textarea {
        background-color: #1a1a1a !important;
        color: white !important;
        border: 1px solid #555 !important;
        font-size: 1rem;
    }

    .stButton>button {
        background-color: #333;
        color: white;
        border: 1px solid #999;
    }

    .stButton>button:hover {
        background-color: #555;
        color: white;
        border: 1px solid white;
    }

    /* Floating upload icon */
    .chat-upload {
        position: fixed;
        bottom: 3.5rem;
        left: 1.5rem;
        z-index: 100;
    }

    .chat-upload input[type="file"] {
        opacity: 0;
        position: absolute;
        width: 24px;
        height: 24px;
        cursor: pointer;
    }

    .chat-upload label {
        background-color: #333;
        border-radius: 50%;
        width: 34px;
        height: 34px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        border: 1px solid #777;
        transition: 0.2s ease;
    }

    .chat-upload label:hover {
        background-color: #555;
        border-color: white;
    }

    .chat-upload label::before {
        content: "📎";
        font-size: 18px;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ----- Floating Upload Icon (Visual only) -----
st.markdown("""
<div class="chat-upload">
    <form action="#">
        <label for="pdf-upload"></label>
        <input type="file" id="pdf-upload" name="pdf-upload" accept=".pdf">
    </form>
</div>
""", unsafe_allow_html=True)


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Lawgic, a helpful lawyer who answers in plain English."}
    ]

# PDF Upload in a collapsible expander (functional!)
with st.expander("📎Upload a legal PDF (optional)"):
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

#  Add black spacer between upload & chat
st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)

# Store message history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Lawgic, a helpful lawyer who provides legal help people understand legal rights and options without needing a lawyer and answers in plain English. If a .pdf is uploaded you provide important details and summarize it for the user"}
    ]

# Show past messages
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

