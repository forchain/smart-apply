import streamlit as st
from pathlib import Path
from smart_apply.cover_letter import CoverLetterGenerator

# Page config
st.set_page_config(
    page_title="Smart Apply - Cover Letter Generator",
    page_icon="📝",
    layout="wide"
)

# Title and description
st.title("Smart Apply")
st.subheader("Generate Personalized Cover Letters")

# Input sections
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Job Description")
    job_description = st.text_area(
        "Paste the job description here",
        height=300,
        placeholder="Enter the job description..."
    )

with col2:
    st.markdown("### Your Resume")
    resume_text = st.text_area(
        "Paste your resume here",
        height=300,
        placeholder="Enter your resume..."
    )

# API Key input
api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

if st.button("Generate Cover Letter"):
    if not api_key:
        st.error("Please enter your OpenAI API key in the sidebar")
    elif not job_description or not resume_text:
        st.error("Please provide both the job description and your resume")
    else:
        try:
            with st.spinner("Generating your cover letter..."):
                # Generate cover letter
                generator = CoverLetterGenerator(api_key)
                cover_letter = generator.generate(job_description, resume_text)
                
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
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}") 