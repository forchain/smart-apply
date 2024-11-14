from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain.tools import Tool
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import logging

class LetterWriter:
    def __init__(self, llm: ChatOpenAI, examples: list[str] = None, language: str = "zh"):
        self.llm = llm
        self.examples = examples or []
        self.language = language
        self.logger = logging.getLogger(__name__)

    def write(self, match_report: str) -> str:
        """Generate cover letter based on matching report"""
        self.logger.info("Starting cover letter generation...")
        
        # 直接使用 LLM 而不是通过 agent
        prompt = ChatPromptTemplate.from_template("""You are a professional cover letter writing expert.

        1. Analyze the writing style, tone, and structure of the following cover letter examples:
        
        {examples}
        
        2. Generate a cover letter based on the matching report and above examples, requirements:
           - Maintain a similar concise and direct tone as the examples
           - Highlight relevant experience and skills mentioned in the matching report
           - Use {language} language
           - Ensure content is entirely based on information from the matching report
           - Mimic the opening and closing style from the examples

        Matching Report:
        {match_report}
        
        Please write a professional cover letter based on the above requirements.
        """)
        
        chain = prompt | self.llm | (lambda x: x.content)
        
        result = chain.invoke({
            "examples": self._format_examples(),
            "language": self.language,
            "match_report": match_report
        })
        
        self.logger.info("Cover letter generation completed")
        return str(result)

    def _format_examples(self) -> str:
        """Format cover letter examples"""
        if not self.examples:
            return "No examples provided, using standard professional cover letter format."
            
        formatted_examples = []
        for i, example in enumerate(self.examples, 1):
            formatted_examples.append(f"Example {i}:\n{example}")
            
        return "\n\n".join(formatted_examples) 