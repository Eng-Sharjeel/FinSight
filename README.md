# FinSight AI

## Introduction
**FinSight AI** is an AI-powered RAG web application that helps financial analysts, researchers, and professionals extract insights from **PDF reports**, **news URLs**, and **CSV datasets** using advanced LLMs and embeddings.

## 🚀 Features

- Upload and analyze **financial PDFs**  
- Summarize and chat with **news articles** (URL input)  
- Explore and visualize **CSV financial data**  
- Ask financial questions 
- Built-in **retrieval-augmented generation (RAG)** pipeline  
- Source tracking, chat history download, and summaries  
- Clean, responsive UI with multi-page navigation

## Installation and Setup Guide

1. create a virtual environment:

   ```sh
   python -m venv venv
    ```
2. activate the virtual environment for windows:

   ```sh
   venv\Scripts\activate
    ```
3. activate the virtual environment for mac:

   ```sh
   source venv/bin/activate
    ```
4. install requirements using pip:

   ```sh
   pip install -r requirements.txt
    ```
4. Add API keys in .env file

Create a **.env** file to store your private API keys for Groq, and Gemini.

## Tools and Technologies Used
- **Programming Language:** Python 3.13
- **Framework:** Streamlit
- **AI APIs:**
  - Google Generative AI (Gemini)
  - GROQ (LLaMA3, Mixtral)
- **Libraries & Packages:**
  - `streamlit` – UI framework
  - `python-dotenv` – For environment variable management
  - `google-generativeai` – Gemini embeddings and models
  - `langchain` – RAG pipeline and LLM orchestration
  - `faiss-cpu` – Vector store for similarity search
  - `PyPDFLoader`, `UnstructuredURLLoader` – Data ingestion from PDFs and URLs
  - `matplotlib`, `seaborn`, `pandas` – CSV analysis and visualizations

## How to Run
- Open terminal in VS Code and run the command:
   
   ```sh
  streamlit run app.py
   ```

