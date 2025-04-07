import streamlit as st
import fitz  # PyMuPDF
import requests
from job_search_agent import search_jobs

# --- Function to extract resume text ---
def extract_text_from_pdf(uploaded_file):
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text

# --- Basic role detection from resume ---
def detect_role(text):
    roles = ["Power BI Developer", "Data Analyst", "Business Intelligence Developer", "Data Engineer"]
    for role in roles:
        if role.lower() in text.lower():
            return role
    return "Power BI Developer"  # default fallback

# --- Streamlit UI ---
st.title("💼 Job Copilot - Resume Based Job Finder")

# Resume Upload
uploaded_file = st.file_uploader("📄 Upload your Resume (PDF)", type=["pdf"])

job_title = ""
location = ""

# When resume is uploaded
if uploaded_file:
    resume_text = extract_text_from_pdf(uploaded_file)
    job_title = detect_role(resume_text)
    st.success(f"✅ Detected Role: {job_title}")
    location = st.text_input("🌍 Enter your preferred job location:", value="India")
    
    if st.button("🔍 Find Relevant Jobs"):
        try:
            jobs = search_jobs(title=job_title, location=location, results=3)
            st.subheader(f"🔎 Jobs for '{job_title}' in '{location}':")

            for idx, job in enumerate(jobs):
                st.markdown(f"### {idx+1}. {job['title']}")
                st.markdown(f"**Company:** {job.get('company', 'N/A')}")
                st.markdown(f"**Location:** {job.get('location', 'N/A')}")
                st.markdown(f"[🔗 Apply Here]({job.get('url')})")
                st.markdown("---")
        except Exception as e:
            st.error(f"❌ Error fetching jobs: {e}")

else:
    st.info("👆 Please upload your resume to begin.")
