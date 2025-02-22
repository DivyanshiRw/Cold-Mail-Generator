import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

from dotenv import load_dotenv
load_dotenv()

class Chain:
    def __init__(self):
        self.llm= ChatGroq(temperature=0, groq_api_key= os.getenv("GROQ_API_KEY"), model_name="llama-3.3-70b-versatile")

    def extract_jobs(self, cleaned_text):
        prompt_extract= PromptTemplate.from_template(
        """
        ### SCRAPED TEXT FROM WEBSITE:
        {page_data}
        ### INSTRUCTION:
        The scraped text is from the career's page of a website.
        Your job is to extract the job postings and return them in JSON format containing the following keys:
        'role', 'experience', 'skills' and 'description'.
        Only return the valid JSON.
        ### VALID JSON (NO PREAMBLE):
        """
        )
        
        chain_extract= prompt_extract | self.llm
        res= chain_extract.invoke(input={'page_data': cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]


    def write_mail(self, job):
        prompt_email = PromptTemplate.from_template(
        """
        ### JOB DESCRIPTION:
        {job_description}
    
        ### INSTRUCTION:
        You are Divyanshi Rawat, a motivated and skilled student looking for an internship opportunity. 
        Your goal is to craft a compelling cold email to apply for the internship mentioned above, 
        highlighting your relevant skills, experiences and enthusiasm for the role.
    
        - Address the recipient professionally.
        - Clearly state your interest in the position.
        - Mention 2-3 key skills or experiences that make you a strong candidate.
        - Show enthusiasm for the company and the role.
        - Keep it concise and action-oriented, with a polite closing.

        Do not provide a preamble.
    
        ### EMAIL (NO PREAMBLE):
        """
       )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job)})
        return res.content


if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))
