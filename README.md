# Smart Apply
Streamline Your Job Application Process With LLM

## Background
Submitting a resume can often feel like a tedious task, particularly when crafting a personalized cover letter that effectively showcases your qualifications and captures the attention of potential employers.

## Highlights
Introducing Smart Apply, a solution designed to streamline your job application process and help you stand out from the competition. With Smart Apply, you can:

* **Generate a Customized Cover Letter**: Input the job description (JD) and your resume, and our system will generate a tailored cover letter that aligns with the specific requirements of the position. Each application will have a unique and optimized letter, ensuring that your submission stands out.
* **Receive a Skills Report**: Get a detailed report highlighting the skills you possess and those you may need to enhance to better match the job requirements. This feedback helps you continuously improve and align your qualifications with the demands of the market.
* **Automate Your Application**: Save time by automatically submitting your resume and cover letter to the job posting. No more manual uploads or repetitive form filling-let Smart Apply handle the details so you can focus on other aspects of your job search.

## Installation

1. Clone this repository:

```bash
git clone https://github.com/forchain/smart-apply.git
```

2. Create a virtual environment and install the required packages:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

3. Run the Streamlit app:

```bash
streamlit run app.py
```

## Usage

1. Get an OpenAI API key from [OpenAI Platform](https://platform.openai.com/)
2. Enter your OpenAI API key in the sidebar
3. Paste the job description and your resume in the respective text areas
4. Click "Generate Cover Letter" to create a customized cover letter
5. Download the generated cover letter using the download button

## Change Log
* 2024-11-05: Added Streamlit web interface
  * Created basic web interface for inputting JD and resume
  * Implemented cover letter generation using OpenAI API
  * Added download functionality for generated cover letters

## Development Steps
1. ✅ Generate a Streamlit app to input JD and resume, and generate a cover letter
2. Add skills analysis and matching feature
3. Implement automated application submission

## Coming Soon
* Skills gap analysis
* Application tracking
* Multiple resume management
* Application automation
