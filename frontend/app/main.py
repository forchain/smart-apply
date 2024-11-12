import streamlit as st
import requests
from pathlib import Path
import sys

# Add frontend directory to Python path
frontend_dir = Path(__file__).parent.parent
if str(frontend_dir) not in sys.path:
    sys.path.append(str(frontend_dir))

from app.config import Config  # Now using absolute import from frontend directory

def setup_page():
    st.set_page_config(
        page_title="Smart Apply - Cover Letter Generator",
        page_icon="📝",
        layout="wide"
    )
    st.title("Smart Apply")
    st.subheader("Generate Personalized Cover Letters")

def setup_sidebar(config):
    model_provider = st.sidebar.selectbox(
        "Select AI Model Provider",
        ["deepseek", "openai"],
        index=["deepseek", "openai"].index("deepseek")
    )
    default_api_key = config.get_provider_api_key(model_provider.lower())
    api_key = st.sidebar.text_input(
        f"Enter {model_provider.upper()} API Key", 
        value=default_api_key,
        type="password"
    )
    return model_provider, api_key

def generate_cover_letter(api_base_url, job_description, resume_text, api_key, model_provider):
    response = requests.post(
        f"{api_base_url}/generate",
        json={
            "job_description": job_description,
            "resume": resume_text,
            "api_key": api_key,
            "provider": model_provider.lower()
        }
    )
    return response

def handle_generation(job_description, resume_text, api_base_url, api_key, model_provider):
    try:
        with st.spinner("Generating your cover letter..."):
            response = generate_cover_letter(api_base_url, job_description, resume_text, api_key, model_provider)
            
            if response.status_code == 200:
                result = response.json()
                display_cover_letter(result.get("cover_letter"))
            else:
                error_detail = response.json().get('detail', 'Unknown error')
                st.error(f"API Error: {error_detail}")
                    
    except requests.exceptions.ConnectionError:
        st.error("Failed to connect to the server. Please check if the backend service is running.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

def display_cover_letter(cover_letter):
    if cover_letter:
        st.markdown("### Generated Cover Letter")
        st.markdown(cover_letter)
        st.download_button(
            label="Download Cover Letter",
            data=cover_letter,
            file_name="cover_letter.txt",
            mime="text/plain"
        )
    else:
        st.error("Failed to generate cover letter: No content received")

def render():
    config = Config()
    api_base_url = config.get_api_base_url()

    setup_page()
    model_provider, api_key = setup_sidebar(config)

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
            handle_generation(job_description, resume_text, api_base_url, api_key, model_provider)

if __name__ == "__main__":
    render()