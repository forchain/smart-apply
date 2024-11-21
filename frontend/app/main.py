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
        ["deepseek", "openai", "grok"],
        index=["deepseek", "openai", "grok"].index("deepseek")
    )
    
    default_api_key = config.get_provider_api_key(model_provider.lower())
    api_key = st.sidebar.text_input(
        f"Enter {model_provider.upper()} API Key",
        value=default_api_key,
        type="password"
    )
    
    # Add fact check option
    enable_fact_check = st.sidebar.checkbox(
        "Enable Fact Checking",
        value=False,
        help="Enable fact checking to verify cover letter content against resume (slower but more accurate)"
    )
    
    return model_provider, api_key, language_code, example, enable_fact_check

def render():
    config = Config()
    api_base_url = config.get_api_base_url()

    setup_page()
    model_provider, api_key, language, example, enable_fact_check = setup_sidebar(config)
    
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
            handle_generation(job_description, resume_text, api_base_url, api_key, 
                            model_provider, language, example, enable_fact_check)

def handle_generation(job_description, resume_text, api_base_url, api_key, model_provider, language, example, enable_fact_check):
    try:
        # Print request data for debugging
        print("Request Data:")
        request_data = {
            "job_description": job_description,
            "resume": resume_text,
            "api_key": api_key,
            "provider": model_provider.lower(),
            "language": language,
            "example": example.strip(),
            "enable_fact_check": enable_fact_check  # Add fact check flag
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
                
                # Create tabs for different sections
                if enable_fact_check:
                    tab_final, tab_initial, tab_match = st.tabs([
                        "Final Cover Letter", 
                        "Initial Draft", 
                        "Matching Report"
                    ])
                else:
                    tab_final, tab_match = st.tabs([
                        "Cover Letter", 
                        "Matching Report"
                    ])
                
                # Display content in respective tabs
                with tab_final:
                    display_cover_letter(result.get("cover_letter"))
                    
                if enable_fact_check:
                    with tab_initial:
                        display_initial_cover_letter(result.get("initial_letter"))
                    
                with tab_match:
                    display_matching_report(result.get("match_report"))
            else:
                error_detail = response.json().get('detail', 'Unknown error')
                st.error(f"API Error: {error_detail}")
                    
    except requests.exceptions.ConnectionError:
        st.error("Failed to connect to the server. Please check if the backend service is running.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

def display_matching_report(match_report):
    if match_report:
        st.markdown("### Matching Analysis Report")
        st.markdown(match_report)
        st.download_button(
            label="Download Matching Report",
            data=match_report,
            file_name="matching_report.txt",
            mime="text/plain"
        )

def display_initial_cover_letter(initial_letter):
    if initial_letter:
        st.markdown("### Initial Cover Letter (Before Fact Check)")
        st.markdown(initial_letter)
        st.download_button(
            label="Download Initial Cover Letter",
            data=initial_letter,
            file_name="initial_cover_letter.txt",
            mime="text/plain"
        )

def display_cover_letter(cover_letter):
    if cover_letter:
        st.markdown("### Final Cover Letter (After Fact Check)")
        st.markdown(cover_letter)
        st.download_button(
            label="Download Final Cover Letter",
            data=cover_letter,
            file_name="cover_letter.txt",
            mime="text/plain"
        )
    else:
        st.error("Failed to generate cover letter: No content received")

if __name__ == "__main__":
    render()