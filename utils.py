import os
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader 
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

def create_vectorstore_from_pdfs(pdf_paths, existing_vectorstore=None):
    """
    Loads one or more PDFs, splits text into chunks, generates embeddings using Gemini,
    and creates or updates a FAISS vector store.

    Args:
        pdf_paths (list): List of file paths to PDF documents
        existing_vectorstore (FAISS, optional): Existing FAISS vectorstore to merge new embeddings into

    Returns:
        FAISS: Vector store containing the embedded chunks (new or merged)
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("GEMINI_API_KEY not set in environment.")
        st.stop()

    all_docs = []
    # Load all PDFs and extract text
    for path in pdf_paths:
        if not os.path.exists(path):
            st.warning(f"File not found: {path}")
            continue
        loader = PyPDFLoader(path)
        docs = loader.load()
        all_docs.extend(docs)

    if not all_docs:
        st.error("No valid PDF content found.")
        st.stop()

    # Split text into chunks for embedding
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = []
    for doc in all_docs:
        chunks.extend(splitter.split_text(doc.page_content))

    if not chunks:
        st.error("No text chunks created from PDFs.")
        st.stop()

    # Generate embeddings using Gemini
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=api_key
    )

    if existing_vectorstore:
        # Add new documents to existing vectorstore
        existing_vectorstore.add_texts(chunks)
        return existing_vectorstore
    else:
        # Create vector store from text chunks
        vectorstore = FAISS.from_texts(chunks, embedding=embeddings)
        return vectorstore

def local_css(file_name):
    """
    Loads custom CSS styles into Streamlit from a given file.

    Args:
        file_name (str): Path to the CSS file
    """
    if not os.path.exists(file_name):
        st.warning(f"CSS file not found: {file_name}")
        return
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
