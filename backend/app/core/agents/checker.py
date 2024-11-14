from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain.tools import Tool
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from typing import Dict
import json
import logging

class FactChecker:
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.logger = logging.getLogger(__name__)

    def verify(self, cover_letter: str, resume: str) -> Dict:
        """Verify cover letter content"""
        self.logger.info("Starting fact verification...")
        
        # 直接使用 LLM 而不是通过 agent
        prompt = ChatPromptTemplate.from_template("""You are a rigorous fact-checking expert.

        Your tasks are:
        1. Carefully review resume content
        2. Check each statement in the cover letter
        3. Flag any content that doesn't match the resume
        4. If any errors are found:
           - Provide correction suggestions
           - Generate a corrected version of the cover letter
        
        Cover Letter:
        {cover_letter}

        Resume:
        {resume}
        
        Provide your verification result in the following JSON format:
        {{
            "is_accurate": boolean,
            "corrections": [list of corrections needed],
            "corrected_letter": "complete corrected version of letter if needed"
        }}
        """)
        
        chain = prompt | self.llm | (lambda x: x.content)
        
        result = chain.invoke({
            "cover_letter": cover_letter,
            "resume": resume
        })
        
        self.logger.info("Fact verification completed")
        
        try:
            result_dict = json.loads(str(result))
            return {
                "is_accurate": result_dict.get("is_accurate", False),
                "corrections": result_dict.get("corrections", []),
                "corrected_letter": result_dict.get("corrected_letter", "")
            }
        except json.JSONDecodeError:
            self.logger.error("Failed to parse verification result as JSON")
            return {
                "is_accurate": False,
                "corrections": ["Error parsing verification result"],
                "corrected_letter": cover_letter
            } 