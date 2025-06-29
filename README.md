# FinSight

**FinSight AI** is an AI-powered RAG web application that helps financial analysts, researchers, and professionals extract insights from **PDF reports**, **news URLs**, and **CSV datasets** using advanced LLMs and embeddings.

## 🚀 Features

✅ Upload and analyze **financial PDFs**  
✅ Summarize and chat with **news articles** (URL input)  
✅ Explore and visualize **CSV financial data**  
✅ Ask financial questions 
✅ Built-in **retrieval-augmented generation (RAG)** pipeline  
✅ Source tracking, chat history download, and summaries  
✅ Clean, responsive UI with multi-page navigation

## 🧠 Tech Stack

- **Frontend:** Streamlit  
- **LLMs:** [Groq](https://groq.com/) (LLaMA3, Mixtral), [Gemini (Google)](https://ai.google.dev/)  
- **RAG Pipeline:** LangChain + FAISS + Custom prompts  
- **Embeddings:** `GoogleGenerativeAIEmbeddings`  
- **PDF Parsing:** `PyPDFLoader`  
- **News Loader:** `UnstructuredURLLoader`  
- **Data Viz:** `Matplotlib`, `Seaborn`

## ⚙️ Setup Instructions

```bash
# 1. Clone the repository
git clone https://github.com/your-username/FinSightAI.git
cd FinSightAI

# 2. Create and activate a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add API keys in .env file
touch .env

# 5. Run the Streamlit app
streamlit run app.py
