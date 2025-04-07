import os
import pdfplumber
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        return ''.join([page.extract_text() or '' for page in pdf.pages])

def parse_resume_with_claude(resume_text):
    prompt = f"""
You are a resume parsing AI. Extract and return the following fields from the resume text:

- Full Name
- Email
- Phone
- Summary
- Skills
- Education
- Work Experience (Company, Job Title, Duration, Description)

Resume:
\"\"\"
{resume_text}
\"\"\"
"""
    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1000,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

if __name__ == "__main__":
    resume_path = "resume.pdf"
    resume_text = extract_text_from_pdf(resume_path)
    parsed_output = parse_resume_with_claude(resume_text)
    print("\nParsed Resume:\n")
    print(parsed_output)

