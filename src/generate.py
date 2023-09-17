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
        "I want you to act as a cover letter writer."
        "I'll provide you with a job advert, main information on the company,"
        "a resume and sometimes other informations."
        "Use this information to create a custom cover letter for the job advert"
        "The cover letter should follow this structure structure:\n\n"
        "Paragraphe 1: highlight informations about the job and the company, and why I'm interested in joining it\n"
        "Paragraphe 2: skills and experiences from my resume and other informations that align with the job description.\n"
        "Paragraphe 3: why I'm a good fit for the role and company culture.\n"
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
            model=model_parameters["model"],
            openai_api_key=model_parameters["api_key"],
        ),
        retriever=vectordb.as_retriever(search_kwargs={"k": 7}),
        chain_type="stuff",
    )

    return qa_chain.run(query)


def split_all_text_in_documents(data: Dict[str, str]) -> List[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=0,
        length_function=len,
    )

    documents = text_splitter.create_documents(
        [text for text in data.values()]
    )
    return text_splitter.split_documents(documents)
