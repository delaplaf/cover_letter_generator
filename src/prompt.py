""" Prompt template and query
"""
from langchain.prompts import PromptTemplate


def get_prompt_template() -> PromptTemplate:
    prompt_template = (
        """Act as a helpful assistant specialist in cover letter. """
        """Use the following pieces of context to create a cover letter at the end. """
        """This context is about a job advert, main information on the company,"""
        """a resume and sometimes other informations.\n\n"""
        """{context} \n\n"""
        """Details about the cover letter: {question}\n\n"""
        """Cover letter:"""
    )

    return PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )


def get_query(language: str) -> str:
    query = (
        "The cover letter should follow this structure:\n\n"
        "Paragraphe 1: highlight informations about the job and the company,"
        "and why I'm interested in joining it\n"
        "Paragraphe 2: skills and experiences from my resume and other informations"
        "that align with the job description.\n"
        "Paragraphe 3: why I'm a good fit for the role and company culture.\n"
        f"Result should be in {language}"
    )
    return query
