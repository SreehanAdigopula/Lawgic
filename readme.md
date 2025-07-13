# Lawgic ⚖️

A Streamlit-based AI legal chatbot that provides accessible answers to U.S. legal questions and plain-language PDF summarization.

## What is Lawgic?

Lawgic is an AI-powered legal chatbot designed to make legal information accessible to everyone — especially those who can't afford a lawyer. While it doesn't replace professional legal counsel, it helps users understand their rights, find trusted resources, and take their first steps toward resolution.

## Features

- **AI Chat Assistant**: Get clear, accessible answers to U.S. legal questions in areas like housing, employment, immigration, and legal documentation
- **PDF Summarization**: Upload legal documents and receive plain-language summaries
- **Topic Filtering**: Filter conversations by legal areas (Housing, Employment, Immigration, Legal Documentation)
- **Responsive UI**: Clean, dark-themed interface optimized for legal consultations

## Prerequisites

- Python 3.11
- OpenAI API key
- Streamlit secrets configuration

## Installation

1. Clone the repository:
```bash
git clone https://github.com/SreehanAdigopula/Lawgic.git
cd Lawgic
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key in `.streamlit/secrets.toml`:
```toml
OPENAI_API_KEY = "your-api-key-here"
```

## Running the Application

Start the Streamlit app:
```bash
streamlit run 1main.py
```

The application will be available at `http://localhost:8501`

## Project Structure

- `1main.py` - Main Streamlit application with chat interface and PDF processing
- `requirements.txt` - Python dependencies
- `app.yaml` - Runtime configuration for deployment
- `.streamlit/secrets.toml` - API keys and secrets (not included in repo)

## Usage

1. **Homepage**: Learn about Lawgic and upload PDFs for summarization
2. **Chat Interface**: Ask legal questions and receive AI-powered responses
3. **PDF Upload**: Upload legal documents from multiple locations within the app
4. **Navigation**: Use the sidebar to switch between pages and access utilities

## Deployment

The app includes `app.yaml` for deployment to platforms that support Python 3.11 runtime.

## Legal Disclaimer

Lawgic provides general legal information and should not be considered as professional legal advice. For specific legal matters, consult with a qualified attorney.
