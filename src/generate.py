from typing import Any, Dict, List

from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma

from extract_data import extract_data


def generate_cover_letter(
    data: Dict[str, Any], model_parameters: Dict[str, Any], language: str
) -> Any:
    extracted_data = extract_data(data)
    print(extracted_data)
    query = get_query(language)

    return qa_data(extracted_data, model_parameters, query)


def get_query(language: str) -> str:
    query = (
        "I want you to act as a cover letter writer. "
        "I'll provide you with the job advert, main information on the company,"
        "my resume and sometimes other informations. "
        "Use this information to create a custom, professional and "
        "effective cover letter for the job advert. "
        "Start by answering the following questions before creating the cover letter:"
        "What are my contact details? you can find them in my resume"
        "What is the company name? you can find it in the job offer"
        "What is the title of the job offer?"
        "Which kind of company it is? you can find it in the job offer and company informations"
        "Which skills on my resume are important for the job offer?"
        "Did I provide other useful information to personalize the result?"
        "With your answers to the previous questions, I'd like you to help me write a cover letter"
        "that consists of three paragraphs and follows this structure."
        "In the first paragraph, highlight details about the company and give specific reasons"
        "as to why I'm interested in joining it. Use the next paragraph to highlight"
        "any of my relevant skills, experiences, or accomplishments that align with the job."
        "The third and final paragraph should once again highlight why I'm a good fit for"
        "the company culture and role."
        "Use professional language and tone. Follow the best cover letter writing practices. "
        f"Result should be in {language}"
    )
    return query


def qa_data(
    data: Dict[str, Any], model_parameters: Dict[str, Any], query: str
) -> Any:
    documents = split_all_text_in_documents(data)

    vectordb = Chroma.from_documents(
        documents,
        embedding=OpenAIEmbeddings(openai_api_key=model_parameters["api_key"]),
    )

    qa_chain = RetrievalQA.from_chain_type(
        ChatOpenAI(
            temperature=model_parameters["temperature"],
            model="gpt-3.5-turbo",
            openai_api_key=model_parameters["api_key"],
        ),
        retriever=vectordb.as_retriever(search_kwargs={"k": 7}),
        chain_type="stuff",
    )

    return qa_chain.run(query)


def split_all_text_in_documents(data: Dict[str, str]) -> List[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )

    documents = text_splitter.create_documents(
        [text for text in data.values()]
    )
    return text_splitter.split_documents(documents)
