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
        
        Create a compelling cover letter that highlights relevant experience and skills from the resume 
        that match the job requirements. The tone should be professional but personable.
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