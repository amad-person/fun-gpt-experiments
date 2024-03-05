import os

import streamlit as st
from dotenv import load_dotenv
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

from pathlib import Path

load_dotenv()

st.set_page_config(layout="wide")
st.title("Code RAG")

faker_code_urls = [

]

with open(Path(__file__).parent / "./faker_docs_urllist.txt", "r") as file:
    faker_docs_urls = [x.strip() for x in file.readlines()]

llm = ChatOpenAI(
    model_name="gpt-4",
    openai_api_key=os.environ.get("OPENAI_API_KEY")  # explicitly loading the env var
)

with st.form("question_list_form"):
    user_input_code_request = st.text_area("Enter your code request for Faker", "Make a pandas dataframe with three "
                                                                                "fake columns: credit card numbers, "
                                                                                "first name, last name.")
    submitted = st.form_submit_button("Submit")
    if submitted:
        loader = WebBaseLoader(faker_code_urls + faker_docs_urls)
        docs = loader.load()

        embeddings = OpenAIEmbeddings()

        text_splitter = RecursiveCharacterTextSplitter()
        documents = text_splitter.split_documents(docs)

        vector = FAISS.from_documents(documents, embeddings)

        prompt = ChatPromptTemplate.from_template("""You are a world class Python programmer. You are well-versed in 
        data analysis Python libraries like numpy, pandas. Take your time.

        Answer the following questions based only on the provided context about the Faker python library:

        <context>
        {context}
        </context>

        Write Python code to do the following: 
        {input}""")

        document_chain = create_stuff_documents_chain(llm, prompt)

        retriever = vector.as_retriever()
        retrieval_chain = create_retrieval_chain(retriever, document_chain)

        response = retrieval_chain.invoke({"input": user_input_code_request})

        st.info(response["answer"])
