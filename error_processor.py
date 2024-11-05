from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import json
from config import CONFIG # Ensure CONFIG is defined in config module

class ErrorProcessor:
    def __init__(self):
        # Initialize ChatGroq instead of Groq
        self.llm = ChatGroq(
            api_key=CONFIG['GROQ_API_KEY'],
            temperature=0.7
        )

        self.prompt = PromptTemplate(
            input_variables=["error_message", "similar_errors"],
            template="""
            Analyze this error and provide a solution:

            Error Message: {error_message}

            Similar resolved errors:
            {similar_errors}

            Please provide:
            1. Error Type:
            2. Root Cause:
            3. Solution Steps:
            4. Prevention Tips:
            """
        )

        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def process_error(self, error_message, similar_errors):
        # Format similar errors into a text list
        similar_errors_text = "\n".join([f"- {err}" for err in similar_errors])
        # Run the chain to get the response
        response = self.chain.run(
            error_message=error_message,
            similar_errors=similar_errors_text
        )
        # Parse the response
        return self._parse_response(response)

    def _parse_response(self, response):
        sections = response.split('\n')
        parsed = {
            'error_type': '',
            'root_cause': '',
            'solution_steps': [],
            'prevention_tips': []
        }

        current_section = None
        for line in sections:
            if '1. Error Type:' in line:
                current_section = 'error_type'
            elif '2. Root Cause:' in line:
                current_section = 'root_cause'
            elif '3. Solution Steps:' in line:
                current_section = 'solution_steps'
            elif '4. Prevention Tips:' in line:
                current_section = 'prevention_tips'
            elif line.strip():
                if current_section in ['solution_steps', 'prevention_tips']:
                    parsed[current_section].append(line.strip())
                elif current_section:
                    parsed[current_section] = line.strip()

        return parsed