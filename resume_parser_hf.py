import os
import requests
from dotenv import load_dotenv
import pdfplumber

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
MODEL_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        return text

def generate_prompt(resume_text):
    return f"""
You are a resume parser. Extract the following details in structured JSON:
- Name
- Email
- Phone
- Skills
- Education
- Experience
- Certifications

Resume:
\"\"\"
{resume_text}
\"\"\"
"""

def query_llm(prompt):
    response = requests.post(
        MODEL_URL,
        headers=headers,
        json={"inputs": prompt}
    )
    response.raise_for_status()
    return response.json()[0]["generated_text"]

if __name__ == "__main__":
    resume_path = "resume.pdf"
    print("📄 Reading resume...")
    resume_text = extract_text_from_pdf(resume_path)

    print("🧠 Querying model via Hugging Face...")
    prompt = generate_prompt(resume_text)
    output = query_llm(prompt)

    print("\n✅ Parsed Resume Output:\n")
    print(output)

