import streamlit as st
from dotenv import load_dotenv
import os
from auth import login_page
from home import home_page
from pdf_insights import pdf_insights_page
from csv_analyzer import csv_analyzer_page
from news_insights import news_insights_page

# --- Load environment variables ---
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

# --- Streamlit page configuration ---
st.set_page_config(page_title="🧠 FinSight AI", layout="wide")

# --- Light Theme CSS ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
        html, body, [class*="css"]  {
            font-family: 'Inter', sans-serif;
            background: #F6F8FB;
            color: #22356F;
        }
        h1, h2, h3, h4 {
            font-weight: 800;
            color: #1976D2;
        }
        /* Sidebar */
        [data-testid="stSidebar"] {
            background: #fff !important;
            color: #22356F !important;
            border-right: 1.5px solid #E3EAF2;
            min-width: 270px;
            max-width: 300px;
        }
        .stSidebar h2 {
            color: #1976D2 !important;
        }
        /* Sidebar button style */
        .stSidebar button {
            background: #F6F8FB !important;
            color: #1976D2 !important;
            border: 2px solid #E3EAF2 !important;
            border-radius: 8px !important;
            margin-bottom: 0.7rem !important;
            font-weight: 600 !important;
            box-shadow: 0 2px 8px rgba(25,118,210,0.03);
            transition: background 0.2s, color 0.2s, border 0.2s;
        }
        .stSidebar button:focus, .stSidebar button:active, .stSidebar button:hover {
            background: #1976D2 !important;
            color: #fff !important;
            border: 2px solid #1976D2 !important;
        }
        /* Card style for main panels */
        .main-card {
            background: #fff;
            border-radius: 22px;
            box-shadow: 0 4px 32px rgba(25,118,210,0.10);
            padding: 2.5rem 2rem;
            margin-bottom: 2rem;
            border: 1px solid #E3EAF2;
        }
        /* Main button style */
        .main-btn {
            background: #1976D2;
            color: #fff;
            border: none;
            border-radius: 8px;
            padding: 0.7rem 1.5rem;
            font-size: 1.1rem;
            font-weight: 700;
            box-shadow: 0 2px 8px rgba(25,118,210,0.12);
            cursor:pointer;
            transition: background 0.2s;
        }
        .main-btn:hover {
            background: #1565C0;
        }
        /* Info badge */
        .info-badge {
            background: #E3EAF2;
            color: #1976D2;
            padding: 0.3rem 0.8rem;
            border-radius: 1rem;
            font-size: 1.1rem;
            font-weight: 600;
            display: inline-block;
        }
    </style>
""", unsafe_allow_html=True)

# --- Session state initialization ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "pdf_paths" not in st.session_state:
    st.session_state.pdf_paths = []
if "news_vectorstore" not in st.session_state:
    st.session_state.news_vectorstore = None
if "news_qa_history" not in st.session_state:
    st.session_state.news_qa_history = []
if "csv_df" not in st.session_state:
    st.session_state.csv_df = None
if "chart_type" not in st.session_state:
    st.session_state.chart_type = "Line"
if "x_cols" not in st.session_state:
    st.session_state.x_cols = []
if "y_cols" not in st.session_state:
    st.session_state.y_cols = []

# --- Sidebar Navigation ---
def sidebar_navigation():
    st.sidebar.markdown("<h2 style='color:#1976D2; font-weight:800;'>📊 FinSight</h2>", unsafe_allow_html=True)
    st.sidebar.markdown('<div style="height:1.5rem;"></div>', unsafe_allow_html=True)
    if st.sidebar.button("🏠 Home"):
        st.session_state.page = "Home"
    if st.sidebar.button("📁 PDF Insights"):
        st.session_state.page = "PDF Insights"
    if st.sidebar.button("📊 CSV Analyzer"):
        st.session_state.page = "CSV Analyzer"
    if st.sidebar.button("📰 News Insights"):
        st.session_state.page = "News Insights"
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "Home"
        st.session_state.messages = []
        st.session_state.vectorstore = None
        st.session_state.summary = ""
        st.session_state.pdf_paths = []
        st.session_state.news_vectorstore = None
        st.session_state.csv_df = None
        st.session_state.chart_type = "Line"
        st.session_state.x_cols = []
        st.session_state.y_cols = []
        st.rerun()

# --- Main App Routing ---
if not st.session_state.logged_in:
    login_page()
else:
    sidebar_navigation()
    if st.session_state.page == "Home":
        home_page()
    elif st.session_state.page == "PDF Insights":
        pdf_insights_page()
    elif st.session_state.page == "CSV Analyzer":
        csv_analyzer_page()
    elif st.session_state.page == "News Insights":
        news_insights_page()