from openai import OpenAI
import logging
from .config import Config

class CoverLetterGenerator:
    def __init__(self, api_key: str, provider: str = "openai"):
        self.provider = provider.lower()
        self.config = Config()
        
        # Get provider configuration
        base_url = self.config.get_base_url(self.provider)
        self.model = self.config.get_model(self.provider)
        
        if not base_url or not self.model:
            raise ValueError(f"Invalid configuration for provider: {self.provider}")
        
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def generate(self, job_description: str, resume: str) -> str:
        try:
            # Construct the prompt
            prompt = f"""
            Based on the following job description and resume, generate a professional cover letter.
            
            Job Description:
            {job_description}
            
            Resume:
            {resume}
            
            Generate a cover letter that highlights relevant experience and skills.
            """

            # Call AI API with configured model
            response = self.client.chat.completions.create(
                model=self.model,  # Use model from config
                messages=[
                    {"role": "system", "content": "You are a professional cover letter writer."},
                    {"role": "user", "content": prompt}
                ]
            )

            # Extract and return the generated cover letter
            return response.choices[0].message.content.strip()

        except Exception as e:
            logging.error(f"Error generating cover letter with {self.provider}: {str(e)}")
            raise