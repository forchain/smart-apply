import openai
from typing import Optional

class CoverLetterGenerator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = api_key

    def generate(self, job_description: str, resume: str) -> str:
        """
        Generate a cover letter based on job description and resume
        """
        prompt = f"""
        Generate a professional cover letter based on the following:
        
        Job Description:
        {job_description}
        
        Resume:
        {resume}
        
        Please read the following Job Description (JD) and candidate's Resume, check if the candidate meets the requirements in the JD point by point, and finally generate a brief cover letter.
        1. Extract key requirements from JD: Read the job description and list the key requirements (such as skills, years of experience, education, language proficiency, etc.).
        2. Compare and check candidate's resume: Analyze the resume content point by point to determine if the candidate meets each requirement in the JD.
            • If requirement is met: Mark as "Meets" and provide relevant supporting content from the resume.
            • If requirement is not met: Mark as "Does not meet" and point out the specific missing parts in the resume.
        3. Generate cover letter: Based on the candidate's strengths and highlights that match the JD, help write a brief cover letter expressing their interest in the position and highlighting their relevant experience and skills.
        The cover letter format: The content of the cover letter should be between <CoverLetter> and </CoverLetter> tags.

        """
        
        client = openai.OpenAI(api_key=self.api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional cover letter writer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        
        return response.choices[0].message.content 