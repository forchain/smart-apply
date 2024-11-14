from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain.tools import StructuredTool
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
import logging

class AnalyzeMatchArgs(BaseModel):
    jd: str
    resume: str

class MatchingAnalyzer:
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.logger = logging.getLogger(__name__)

    def analyze(self, jd: str, resume: str) -> str:
        """Execute JD and resume matching analysis"""
        self.logger.info("Starting JD and resume matching analysis...")
        
        prompt = ChatPromptTemplate.from_template("""You are a professional talent matching analyst. 
        Your goal is to analyze the match between a job description and a resume.
        
        Please analyze the following:
        
        Job Description:
        {jd}
        
        Resume:
        {resume}
        
        Provide a detailed matching report that includes:
        1. Overall match score (0-100%)
        2. Key requirements analysis
        3. Specific matching points
        4. Areas for improvement
        
        Format your response in a clear, structured way.
        """)
        
        chain = prompt | self.llm | (lambda x: x.content)
        
        result = chain.invoke({
            "jd": jd,
            "resume": resume
        })
        
        self.logger.info("Match analysis completed")
        return str(result) 