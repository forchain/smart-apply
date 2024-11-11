import streamlit as st
import requests
from pathlib import Path
from backend.core.config import Config

# API endpoint
API_BASE_URL = "http://localhost:8000"

# Page config
st.set_page_config(
    page_title="Smart Apply - Cover Letter Generator",
    page_icon="📝",
    layout="wide"
)

# Title and description
st.title("Smart Apply")
st.subheader("Generate Personalized Cover Letters")

# Load configuration
config = Config()

# Sidebar - Model selection and API key
model_provider = st.sidebar.selectbox(
    "Select AI Model Provider",
    ["deepseek", "openai"],
    index=["deepseek", "openai"].index("deepseek")
)

# Get API key for selected provider
try:
    provider_config = requests.get(f"{API_BASE_URL}/config/{model_provider.lower()}").json()
    api_key = provider_config.get("api_key", "")
except Exception as e:
    st.error(f"Error fetching provider config: {str(e)}")
    api_key = ""

api_key = st.sidebar.text_input(
    f"Enter {model_provider.upper()} API Key", 
    value=api_key,
    type="password"
)

# Input sections
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Job Description")
    job_description = st.text_area(
        "Paste the job description here",
        height=300,
        placeholder="Enter the job description...",
        value=config.get_default_jd()
    )

with col2:
    st.markdown("### Your Resume")
    resume_text = st.text_area(
        "Paste your resume here",
        height=300,
        placeholder="Enter your resume...",
        value=config.get_default_resume()
    )

if st.button("Generate Cover Letter"):
    if not job_description or not resume_text:
        st.error("Please provide both the job description and your resume")
    else:
        try:
            with st.spinner("Generating your cover letter..."):
                # Call FastAPI endpoint
                response = requests.post(
                    f"{API_BASE_URL}/generate",
                    json={
                        "job_description": job_description,
                        "resume": resume_text,
                        "api_key": api_key,
                        "model_provider": model_provider.lower()
                    }
                )
                
                if response.status_code == 200:
                    cover_letter = response.json()["cover_letter"]
                    
                    # Display the generated cover letter
                    st.markdown("### Generated Cover Letter")
                    st.markdown(cover_letter)
                    
                    # Add download button
                    st.download_button(
                        label="Download Cover Letter",
                        data=cover_letter,
                        file_name="cover_letter.txt",
                        mime="text/plain"
                    )
                else:
                    st.error(f"API Error: {response.json().get('detail', 'Unknown error')}")
                    
        except Exception as e:
            st.error(f"An error occurred: {str(e)}") 