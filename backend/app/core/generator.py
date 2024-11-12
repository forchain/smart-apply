from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
import logging
from .config import Config

class CoverLetterGenerator:
    def __init__(self, api_key: str, provider: str = "openai", language: str = "zh", example: str = ""):
        self.provider = provider.lower()
        self.language = language.lower()
        self.config = Config()
        
        # Get provider configuration
        base_url = self.config.get_base_url(self.provider)
        self.model = self.config.get_model(self.provider)
        
        if not base_url or not self.model:
            raise ValueError(f"Invalid configuration for provider: {self.provider}")
        
        # Initialize LangChain chat model
        self.chat = ChatOpenAI(
            model=self.model,
            openai_api_key=api_key,
            openai_api_base=base_url,
            temperature=0.7
        )

        # Create system prompt
        system_prompt = """You are a professional cover letter writer. 
Your task is to generate a cover letter that closely follows the style, tone, and structure of the provided example while adapting the content to match the specific job description and resume."""

        # Create base prompt
        user_prompt = f"""First, carefully analyze the following example cover letter style:

{example.strip() if example.strip() else 'No example provided - use a professional, standard cover letter format.'}

Now, using the same writing style, tone, and structure as the example above, generate a cover letter in {self.language} language based on:

Job Description:
{{job_description}}

Resume:
{{resume}}

Important requirements:
1. Match the exact structure and format of the example (if provided)
2. Use similar transition phrases and expressions
3. Maintain the same level of formality and tone
4. Adapt the content to highlight relevant experience and skills
5. Keep similar paragraph length and organization
6. Ensure the output is in {self.language} language

Remember: The goal is to create a cover letter that feels like it was written in the same style as the example while being perfectly tailored to this specific job and candidate."""

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", user_prompt)
        ])

        # Print prompt for debugging
        print("User Prompt:")
        print(user_prompt)

        # Create output parser
        self.output_parser = StrOutputParser()

        # Create generation chain
        self.chain = self.prompt | self.chat | self.output_parser

    def generate(self, job_description: str, resume: str) -> str:
        try:
            # Generate cover letter using LangChain
            cover_letter = self.chain.invoke({
                "job_description": job_description,
                "resume": resume
            })

            return cover_letter.strip()

        except Exception as e:
            logging.error(f"Error generating cover letter with {self.provider}: {str(e)}")
            raise