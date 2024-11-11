import streamlit as st
import requests
from ..config import Config

API_BASE_URL = "http://localhost:8000/api/v1"

def render():
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

    try:
        provider_config = requests.get(f"{API_BASE_URL}/config/{model_provider.lower()}").json()
        api_key = provider_config.get("api_key", "")
    except Exception as e:
        st.error(f"Error fetching provider config: {str(e)}")
        api_key = ""

    # ... 其余代码保持不变 ...

if __name__ == "__main__":
    render() 