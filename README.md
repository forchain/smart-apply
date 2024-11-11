# Smart Apply

Streamline Your Job Application Process With LLM

## Features

* Support for multiple AI models (OpenAI and DeepSeek)
* Configurable default settings for API keys and content
* User-friendly web interface with model selection
* Customizable cover letter generation
* Default templates for job descriptions and resumes
* Client-server architecture for better scalability

## Architecture
The application consists of two main components:
* FastAPI backend server - Handles AI model interactions and core logic
* Streamlit frontend - Provides user interface and interaction

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

## Running the Application

You have three options to run the application:

### Option 1: Run both services with single command

On Unix-like systems (Linux/MacOS):
```bash
chmod +x run.sh  # Make script executable (first time only)
./run.sh
```

On Windows:
```batch
run.bat
```

### Option 2: Run services separately
1. Start the FastAPI server:
```bash
python run_server.py
```

2. In a new terminal, start the Streamlit frontend:
```bash
streamlit run app.py
```

### Option 3: Development mode
For development, you might want to run the services in separate terminals to see the logs clearly:
* Terminal 1: `python run_server.py`
* Terminal 2: `streamlit run app.py`

The services will be available at:
* Frontend: http://localhost:8501
* Backend API: http://localhost:8000
* API Documentation: http://localhost:8000/docs

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
   - `model`: Specify the model to use
   - `api_key`: Your API key for the service (can also be entered in UI)
   - `base_url`: API endpoint URL

2. **Default Templates**:
   - `resume`: Default resume template to pre-fill in the UI
   - `jd`: Default job description template to pre-fill in the UI

## API Endpoints

The FastAPI backend provides the following endpoints:

* `POST /generate` - Generate cover letter
  - Request body: job description, resume, API key, and model provider
  - Returns: Generated cover letter

* `GET /config/{provider}` - Get provider configuration
  - Path parameter: AI model provider name
  - Returns: Provider configuration including API key and model settings

For detailed API documentation, visit http://localhost:8000/docs when the server is running.

# Architect
smart-apply/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── routes.py        # FastAPI routes (原 server.py)
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py        # 配置管理
│   │   │   └── generator.py     # 原 cover_letter.py
│   │   └── models/
│   │       ├── __init__.py
│   │       └── request.py       # Pydantic models
│   ├── config/
│   │   ├── config.yaml.example
│   │   └── config.yaml
│   ├── requirements.txt
│   └── main.py                  # FastAPI 入口 (原 run_server.py)
│
├── frontend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py           # 前端配置
│   │   └── pages/
│   │       ├── __init__.py
│   │       └── home.py         # Streamlit 页面 (原 app.py)
│   ├── config/
│   │   └── config.yaml
│   └── requirements.txt
│
├── scripts/
│   ├── run.sh                  # Unix 启动脚本
│   └── run.bat                 # Windows 启动脚本
│
├── README.md
└── setup.py

## Change Log
* 2024-11-09: Major architecture update
  * Split into client-server architecture
  * Added FastAPI backend
  * Improved error handling and configuration
* Previous changes...

## Coming Soon
* Skills gap analysis
* Application tracking
* Multiple resume management
* Application automation
