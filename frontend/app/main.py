import streamlit as st
import requests
from pathlib import Path
import sys

# Add frontend directory to Python path
frontend_dir = Path(__file__).parent.parent
if str(frontend_dir) not in sys.path:
    sys.path.append(str(frontend_dir))

from app.config import Config

def setup_page():
    st.set_page_config(
        page_title="Smart Apply - Cover Letter Generator",
        page_icon="📝",
        layout="wide"
    )
    st.title("Smart Apply")
    st.subheader("Generate Personalized Cover Letters")

def setup_sidebar(config):
    # Language selection
    language = st.sidebar.selectbox(
        "Output Language",
        ["English", "Chinese"],
        index=1  # Default to Chinese
    )
    
    # Convert display language to code
    language_code = "zh" if language == "Chinese" else "en"
    
    # Load example template from config
    example_template = config.get_cover_letter_example(language_code)
    
    # Allow user to customize example template
    example = st.sidebar.text_area(
        "Cover Letter Example Template (Optional)",
        value=example_template,
        height=200,
        help="Customize the example template that the AI will use as a reference style"
    )
    
    model_provider = st.sidebar.selectbox(
        "Select AI Model",
        ["deepseek", "openai"],
        index=["deepseek", "openai"].index("deepseek")
    )
    
    default_api_key = config.get_provider_api_key(model_provider.lower())
    api_key = st.sidebar.text_input(
        f"Enter {model_provider.upper()} API Key",
        value=default_api_key,
        type="password"
    )
    
    return model_provider, api_key, language_code, example

def render():
    config = Config()
    api_base_url = config.get_api_base_url()

    setup_page()
    model_provider, api_key, language, example = setup_sidebar(config)
    
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
        st.markdown("### Resume")
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
            handle_generation(job_description, resume_text, api_base_url, api_key, model_provider, language, example)

def handle_generation(job_description, resume_text, api_base_url, api_key, model_provider, language, example):
    try:
        # Print request data for debugging
        print("Request Data:")
        request_data = {
            "job_description": job_description,
            "resume": resume_text,
            "api_key": api_key,
            "provider": model_provider.lower(),
            "language": language,
            "example": example.strip()
        }
        print(request_data)

        with st.spinner("Generating..."):
            response = requests.post(
                f"{api_base_url}/generate",
                json=request_data
            )
            
            # Print response for debugging
            print("Response Status:", response.status_code)
            print("Response Data:", response.json())
            
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

if __name__ == "__main__":
    render()