# HireMe Agent

An AI-powered job search and recommendation agent.

## Setup Instructions

### 1. Install Requirements
Create a virtual environment (optional but recommended) and install the dependencies listed in `requirements.txt`:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy the configuration template or edit `.env` and fill in the placeholder keys:
- `GROQ_API_KEY`: Your Groq API Key for running LLM agents.
- `ADZUNA_APP_ID`: Your Adzuna Application ID.
- `ADZUNA_APP_KEY`: Your Adzuna Application Key.
- `ADZUNA_COUNTRY`: The country code for job search (e.g., `gb`, `us`, etc.). Defaults to `gb` if not set.

### 3. Run the Application
Start the Streamlit application using:
```bash
streamlit run app.py
```
