# Lawgic — Streamlit Chatbot
# ==========================
# A Streamlit application that delivers:
#   • An AI-driven chat assistant for common U.S. legal questions
#   • Plain-language PDF summarisation
#   • A polished, responsive user interface

# ───────────────────────────────── Imports ──────────────────────────────
import tempfile
import fitz                     # PyMuPDF – lightweight PDF parsing
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv  # noqa: F401 (env vars loaded elsewhere)

# ────────────────────────────── OpenAI Client ───────────────────────────
# API key is stored securely in `.streamlit/secrets.toml`
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ──────────────── Utility: version-safe Streamlit rerun ────────────────
def safe_rerun() -> None:
    """
    Programmatically rerun the app across Streamlit versions.
    """
    if hasattr(st, "experimental_rerun"):
        st.experimental_rerun()
    elif hasattr(st, "rerun"):
        st.rerun()
    else:
        # Fallback for very old versions
        st.session_state._needs_rerun = True  # type: ignore[attr-defined]

# ────────────────────────── Session-State Defaults ─────────────────────
if "sidebar_state" not in st.session_state:
    # Initial sidebar visibility (matches `initial_sidebar_state`)
    st.session_state.sidebar_state = "expanded"

if "current_page" not in st.session_state:
    st.session_state.current_page = "homepage"

if "messages" not in st.session_state:
    # System prompt establishes the assistant’s capabilities
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are Lawgic, an AI-powered legal chatbot that provides "
                "clear, accessible answers to U.S. legal questions in areas "
                "like housing, employment, immigration, and legal documentation."
            ),
        }
    ]

# ───────────────────────────── UI Callbacks ────────────────────────────
def toggle_sidebar() -> None:
    """Expand / collapse the sidebar and trigger rerun."""
    st.session_state.sidebar_state = (
        "collapsed" if st.session_state.sidebar_state == "expanded" else "expanded"
    )

# Sidebar toggle button (always visible)
st.button(
    "🔽 Hide Sidebar" if st.session_state.sidebar_state == "expanded" else "▶️ Show Sidebar",
    on_click=toggle_sidebar,
)

# ──────────────────────────── Page Metadata ────────────────────────────
st.set_page_config(
    page_title="Lawgic",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state=st.session_state.sidebar_state,
)

# ────────────────────────── Global Stylesheet ──────────────────────────
# Inject custom CSS to give the app its distinctive look & feel.
st.markdown(
    '''
<style>
#MainMenu, footer, header, .stDeployButton {visibility: hidden;}

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
html, body {font-family: 'Inter', sans-serif !important;}

:root {--accent: #FBE8C6;}

.stApp {
    background: #000;
    color: #fff;
}
.main .block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* Typography */
.stMarkdown h1 {font-size: 4.2rem; font-weight: 800; color: var(--accent);}
.stMarkdown h2 {font-size: 2.4rem; font-weight: 600; color: var(--accent);} 
.stMarkdown p  {font-size: 1.15rem; line-height: 1.7; color: #e3e3e3; 
                max-width: 800px; margin: 0 auto 1.2rem;}

/* Chat banner & container */
.chat-banner {
    position: sticky; top: 0; z-index: 5;
    background: rgba(254, 222, 179, .12);
    backdrop-filter: blur(4px);
    border-bottom: 1px solid rgba(255, 255, 255, .08);
    padding: .6rem 1rem;
    text-align: center;
    font-weight: 600;
    letter-spacing: 1px;
    color: var(--accent);
}
.chat-container {
    background: radial-gradient(circle at 0 0,
                rgba(255, 255, 255, .04) 0%, transparent 70%);
    padding: 1rem;
    border-radius: 12px;
}

/* Chat messages */
.stChatMessage {
    background: rgba(255, 255, 255, .05) !important;
    border-radius: 14px !important;
    padding: .8rem 1rem !important;
}
.stChatMessage:hover {transform: translateY(-2px);}

/* Chat input */
.stChatInput input {
    background: #1a1a1a !important;
    color: #fff !important;
    border: 1px solid #555 !important;
    border-radius: 20px !important;
}

/* Buttons & sliders */
.stButton button, .stSlider > div[data-baseweb="slider"] span {
    background: var(--accent) !important;
    color: #000 !important;
}
.stButton button:hover {box-shadow: 0 0 8px var(--accent);} 

.stMarkdown {animation: fadeIn .5s ease-in-out;}
</style>
''',
    unsafe_allow_html=True,
)

# ──────────────────────── PDF Summariser Widget ────────────────────────
def pdf_summariser_widget(label: str = "📄 Upload a legal document (PDF) to summarise"):
    """
    Allow the user to upload a PDF and receive a plain-language summary.
    """
    with st.expander(label):
        uploaded = st.file_uploader("Choose a PDF", type=["pdf"], key=label)
        if not uploaded:
            return

        # Save PDF to a temp file for processing
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded.read())
            pdf_path = tmp.name

        try:
            # Extract text (15k chars max for this demo)
            with fitz.open(pdf_path) as doc:
                text = "\n".join(page.get_text() for page in doc)

            st.success("PDF loaded — summarising…")

            snippet = text[:15_000]

            with st.spinner("Calling GPT…"):
                response = client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "Summarise legal documents in plain-language bullet points."
                            ),
                        },
                        {"role": "user", "content": f"Summarise this document:\n\n{snippet}"},
                    ],
                )

            st.markdown("### 📝 Summary")
            st.write(response.choices[0].message.content)

        except Exception as exc:
            st.error(f"Could not process PDF: {exc}")

# ───────────────────────────── Page Layouts ────────────────────────────
def show_homepage() -> None:
    """Render the landing page with product pitch and PDF widget."""
    st.markdown(
        """
<div style='text-align:center; padding:4rem 0 2rem;'>
  <h1>👨‍⚖️ LAWGIC ⚖️</h1>
  <h3 style='font-weight:400; color:#D8C7AE; font-size:1.6rem;'>
      Free Legal Advice for Everyone
  </h3>
  <p>Accessible, clean answers to U.S. legal questions.</p>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown("## What is LAWGIC?")
    st.write(
        "LAWGIC is an AI-powered legal chatbot designed to make legal "
        "information accessible to everyone — especially those who can’t "
        "afford a lawyer. While it doesn’t replace a lawyer, it helps users "
        "understand their rights, find trusted resources, and take their "
        "first steps toward resolution."
    )

    pdf_summariser_widget()

    if st.button("🚀 Start Chatting", type="primary"):
        st.session_state.current_page = "chat"
        safe_rerun()

def show_chat() -> None:
    """Render the chat interface and real-time conversation."""
    # Optional PDF summarisation on the chat page
    st.markdown("### 📄 Upload PDF to Summarise (Chat Page)")
    pdf_summariser_widget("📄 Upload PDF inside Chat page")

    # Chat banner
    st.markdown(
        '<div class="chat-banner">👨‍⚖️ Lawgic Chat • Ask anything about U.S. law</div>',
        unsafe_allow_html=True,
    )

    # Chat history container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    # Replay previous assistant / user messages (skip system prompt)
    for msg in st.session_state.messages[1:]:
        st.chat_message(msg["role"]).write(msg["content"])

    # Chat input
    user_question = st.chat_input("Ask Anything…")
    if user_question:
        st.chat_message("user").write(user_question)
        st.session_state.messages.append({"role": "user", "content": user_question})

        with st.spinner("Thinking..."):
            try:
                reply = client.responses.create(
                    model="o4-mini",
                    input=st.session_state.messages,
                    tools=[
                        {
                            "type": "file_search",
                            "vector_store_ids": ["vs_68733d52acf88191af43980b966b48c5"],
                        }
                    ],
                )
                assistant_answer = reply.output_text
                st.chat_message("assistant").write(assistant_answer)
                st.session_state.messages.append(
                    {"role": "assistant", "content": assistant_answer}
                )
            except Exception as exc:
                st.error(f"Error processing request: {exc}")

    st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────── Sidebar ───────────────────────────────
with st.sidebar:
    st.header("Navigation")

    selected = st.radio(
        "Go to",
        options=["Homepage", "Chat"],
        index=0 if st.session_state.current_page == "homepage" else 1,
    )

    if selected.lower() != st.session_state.current_page:
        st.session_state.current_page = selected.lower()
        safe_rerun()

    # Additional tools only on chat page
    if st.session_state.current_page == "chat":
        st.divider()
        st.header("Utilities & Filters")

        pdf_summariser_widget("📄 Summarise a PDF inside chat sidebar")

        st.divider()
        st.selectbox(
            "Topic Filter",
            options=["All", "Housing", "Employment", "Immigration", "Legal Documentation"],
        )

        if st.button("🔄 Reset Chat"):
            st.session_state.messages = st.session_state.messages[:1]  # keep system prompt
            safe_rerun()

# ────────────────────────────── Routing ────────────────────────────────
(show_homepage if st.session_state.current_page == "homepage" else show_chat)()
