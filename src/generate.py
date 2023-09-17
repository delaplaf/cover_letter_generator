from typing import Any, Dict, List

from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma

from extract_data import extract_data


def generate_cover_letter(
    data: Dict[str, Any], model_parameters: Dict[str, Any]
) -> Any:
    extracted_data = extract_data(data)
    query = get_query()

    return qa_data(extracted_data, model_parameters, query)


def get_query() -> str:
    query = "Write a cover letter with the provided job post and company information"
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
