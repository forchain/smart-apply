from langchain_openai import ChatOpenAI
from typing import List
import logging
from .config import Config
from .agents.analyzer import MatchingAnalyzer
from .agents.writer import LetterWriter
from .agents.checker import FactChecker

class CoverLetterGenerator:
    def __init__(self, api_key: str, provider: str = "openai", language: str = "zh", example: str = ""):
        # Configure logging
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),  # Output to console
                logging.FileHandler('cover_letter_generator.log')  # Output to file
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        self.provider = provider.lower()
        self.language = language.lower()
        self.config = Config()
        self.examples = self._parse_examples(example)
        
        # Initialize base model configuration
        base_url = self.config.get_base_url(self.provider)
        self.model = self.config.get_model(self.provider)
        
        if not base_url or not self.model:
            raise ValueError(f"Invalid configuration for provider: {self.provider}")
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            model=self.model,
            openai_api_key=api_key,
            openai_api_base=base_url,
            temperature=0.7
        )
        
        # Initialize agents
        self.analyzer = MatchingAnalyzer(self.llm)
        self.writer = LetterWriter(self.llm, self.examples, self.language)
        self.checker = FactChecker(self.llm)

    def _parse_examples(self, example_text: str) -> List[str]:
        """Parse example text, treating each line as an independent example"""
        if not example_text:
            return []
        
        # Split by lines and filter empty lines
        examples = [
            line.strip() for line in example_text.splitlines()
            if line.strip() and not line.isspace()
        ]
        
        self.logger.info(f"Found {len(examples)} examples in the provided text")
        return examples

    def generate(self, job_description: str, resume: str) -> str:
        """Main process for generating cover letter"""
        try:
            self.logger.info("Starting cover letter generation process...")
            self.logger.debug(f"Input JD length: {len(job_description)}, Resume length: {len(resume)}")
            
            # Step 1: Generate matching analysis report
            self.logger.info("Step 1: Generating match analysis report...")
            match_report = self.analyzer.analyze(job_description, resume)
            
            # Step 2: Generate initial cover letter
            self.logger.info("Step 2: Generating initial cover letter...")
            initial_letter = self.writer.write(match_report)
            
            # Step 3: Fact checking and correction
            self.logger.info("Step 3: Performing fact checking...")
            verification_result = self.checker.verify(initial_letter, resume)
            
            if not verification_result["is_accurate"]:
                self.logger.info("Corrections needed, using corrected version...")
                self.logger.debug(f"Corrections required: {verification_result['corrections']}")
                return verification_result["corrected_letter"]
            
            self.logger.info("Cover letter generation completed successfully")
            return initial_letter.strip()

        except Exception as e:
            self.logger.error(f"Error in cover letter generation: {str(e)}", exc_info=True)
            raise