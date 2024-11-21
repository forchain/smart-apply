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
        
        self.logger.info(f"Fact verification completed: {result}")
        
        try:
            # Extract JSON content between first { and last }
            result_str = str(result)
            start_idx = result_str.find('{')
            end_idx = result_str.rfind('}')
            
            if start_idx == -1 or end_idx == -1:
                raise json.JSONDecodeError("No JSON object found", result_str, 0)
                
            json_str = result_str[start_idx:end_idx + 1]
            result_dict = json.loads(json_str)
            
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