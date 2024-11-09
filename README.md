# Smart Apply

Streamline Your Job Application Process With LLM

## Features

* Support for multiple AI models (OpenAI and DeepSeek)
* Configurable default settings for API keys and content
* User-friendly web interface with model selection
* Customizable cover letter generation
* Default templates for job descriptions and resumes

## Installation

1. Clone this repository:

```bash
git clone https://github.com/forchain/smart-apply.git
cd smart-apply
```

2. Create a virtual environment and install the required packages:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
pip install --upgrade pip  # Ensure pip is up to date
pip install -r requirements.txt
```

3. Configure the application:

```bash
cp config.yaml.example config.yaml
# Edit config.yaml with your settings
```

4. Run the Streamlit app:

```bash
streamlit run app.py
```

If you encounter any module errors, try reinstalling the requirements:
```bash
pip uninstall smart-apply  # Remove any existing installation
pip install -r requirements.txt  # Reinstall all requirements
```

## Configuration
The `config.yaml` file supports the following settings:

```yaml
# AI Model Providers
openai:
  model: gpt-4-turbo-preview
  api_key: your_openai_key_here  # optional
  base_url: https://api.openai.com/v1

deepseek:
  model: deepseek-chat
  api_key: your_deepseek_key_here  # optional
  base_url: https://api.deepseek.com

# Default Templates
defaults:
  resume: |
    # Your default resume template here
    
  jd: |
    # Your default job description template here
```

### Configuration Options:

1. **AI Model Settings**:
   - `model`: Specify the model to use (e.g., gpt-4-turbo-preview for OpenAI)
   - `api_key`: Your API key for the service (can also be entered in UI)
   - `base_url`: API endpoint URL

2. **Default Templates**:
   - `resume`: Default resume template to pre-fill in the UI
   - `jd`: Default job description template to pre-fill in the UI

## Usage
1. Select your preferred AI model provider from the sidebar (OpenAI or DeepSeek)
2. Enter your API key (if not configured in config.yaml)
3. Modify the pre-filled job description and resume (or use the defaults)
4. Click "Generate Cover Letter" to create a customized cover letter
5. Download the generated cover letter using the download button

## Change Log
* 2024-11-05: Added multi-model support
  * Added support for OpenAI and DeepSeek models
  * Implemented configurable defaults
  * Added model selection dropdown
* 2024-11-05: Added Streamlit web interface
  * Created basic web interface for inputting JD and resume
  * Implemented cover letter generation using AI APIs
  * Added download functionality for generated cover letters
* 2024-11-06: Configuration system update
  * Switched to YAML configuration format
  * Added support for default templates
  * Improved configuration management

## Coming Soon
* Skills gap analysis
* Application tracking
* Multiple resume management
* Application automation
