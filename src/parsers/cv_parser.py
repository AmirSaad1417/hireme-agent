import json
from groq import Groq
from src.config import settings

def parse_cv_text_with_ai(raw_text: str) -> dict:
    """
    Sends the raw CV text to the Groq API (llama3-8b-8192)
    and extracts a structured JSON profile using JSON mode.
    """
    # Initialize Groq client
    client = Groq(api_key=settings.GROQ_API_KEY)
    
    # Prompt instructing the LLM
    prompt = f"""
    You are an expert ATS (Applicant Tracking System) parser. Analyze the following unstructured text extracted from a CV and extract structured candidate profile data.

    Provide the output strictly as a JSON object matching this schema:
    {{
        "name": "Candidate's full name (or 'Unknown' if not found)",
        "email": "Candidate's email address (or empty string if not found)",
        "key_skills": ["Skill 1", "Skill 2", "Skill 3", ... (limit to top 10-15 key professional/technical skills)],
        "experience_level": "Junior, Mid, or Senior (deduced from years and depth of experience)",
        "target_roles": ["Role Title 1", "Role Title 2", ... (suggest 2-3 matching job roles based on experience and skills)],
        "target_location": "Target city, region or country if mentioned, otherwise empty string",
        "summary": "A brief 2-3 sentence professional summary of the candidate's background and career goals"
    }}

    Extracted CV Text:
    {raw_text}
    """
    
    # Call Groq API with JSON mode enabled
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a precise JSON extractor. Output valid JSON only, matching the user's requested schema."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.1,
    )
    
    # Extract response content
    response_content = completion.choices[0].message.content.strip()
    
    # Parse JSON
    try:
        parsed_data = json.loads(response_content)
    except json.JSONDecodeError as e:
        raise ValueError(f"AI failed to generate a valid JSON profile: {str(e)}\nRaw Response: {response_content}")
        
    return parsed_data
