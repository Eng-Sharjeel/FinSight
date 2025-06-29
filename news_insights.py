import streamlit as st
import os
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA

VECTORSTORE_DIR = "news_vectorstore_index"

def news_insights_page():
    st.markdown("""
    <div class="main-card">
        <h2>📰 News Research Tool</h2>
        <p>Analyze stock-related articles, ask questions, and generate summaries with sources.</p>
    </div>
    """, unsafe_allow_html=True)

    # Session State Initialization
    for key in ["news_urls", "news_qa_history", "news_vectorstore", "news_summary"]:
        if key not in st.session_state:
            st.session_state[key] = [] if "urls" in key or "history" in key else None

    # Add new URL
    new_url = st.text_input("🔗 Enter a News URL")
    if st.button("➕ Add URL"):
        if new_url and new_url not in st.session_state.news_urls:
            st.session_state.news_urls.append(new_url)
            st.success("✅ URL added.")
        elif new_url in st.session_state.news_urls:
            st.warning("⚠️ URL already added.")
        else:
            st.warning("❗ Please enter a valid URL.")

    # Show and clear URLs
    if st.session_state.news_urls:
        st.markdown("#### ✅ Added URLs")
        for idx, url in enumerate(st.session_state.news_urls):
            st.write(f"{idx+1}. {url}")
        if st.button("🗑️ Clear URLs"):
            st.session_state.news_urls = []
            st.session_state.news_vectorstore = None
            st.success("✅ URLs cleared.")

    # Process URLs
    if st.session_state.news_urls and st.button("🚀 Process URLs"):
        try:
            gemini_key = os.getenv("GEMINI_API_KEY")
            loader = UnstructuredURLLoader(urls=st.session_state.news_urls)
            docs = loader.load()

            for i, doc in enumerate(docs):
                doc.metadata = {"source": st.session_state.news_urls[i]}

            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            text_chunks = splitter.split_documents(docs)

            embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=gemini_key)
            vectorstore = FAISS.from_documents(text_chunks, embedding=embeddings)
            vectorstore.save_local(VECTORSTORE_DIR)
            st.session_state.news_vectorstore = vectorstore
            st.success("✅ URLs processed and vectorstore saved.")
        except Exception as e:
            st.error(f"❌ Processing failed: {e}")

    # Summary Button
    if st.session_state.news_vectorstore:
        if st.button("🧠 Generate Summary"):
            try:
                retriever = st.session_state.news_vectorstore.as_retriever(search_kwargs={"k": 6})
                llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama3-8b-8192")
                chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

                summary_prompt = """
                As a financial news analyst, provide a structured and concise summary of the uploaded articles.
                Include:
                - Key stock-related developments
                - Company names, sectors, and market events
                - Sentiment (positive/negative/neutral)
                - Economic implications and forecasts
                - (If possible) Latest closing stock prices for mentioned companies
                Use bullet points and focus on actionable insights.
                """
                result = chain.invoke({"query": summary_prompt})
                st.session_state.news_summary = result.get("result", "Summary not available.")
                st.success("📌 Summary generated.")
            except Exception as e:
                st.error(f"❌ Summary generation failed: {e}")

        if st.session_state.news_summary:
            with st.expander("📌 View Summary", expanded=True):
                st.markdown(st.session_state.news_summary)
                st.download_button("⬇ Download Summary", st.session_state.news_summary, "news_summary.txt", "text/plain")

    # Ask questions
    if st.session_state.news_vectorstore:
        st.markdown("#### 💬 Ask a question about the articles")
        user_query = st.text_input("Your Question", key="user_query")
        if user_query:
            try:
                retriever = st.session_state.news_vectorstore.as_retriever(search_kwargs={"k": 5})
                docs = retriever.get_relevant_documents(user_query)

                sources = set(doc.metadata.get("source") for doc in docs if "source" in doc.metadata)

                llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama3-8b-8192")
                chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
                result = chain.invoke({"query": user_query})
                answer = result.get("result", "No answer found.")

                st.markdown(f"**Answer:** {answer}")
                if sources:
                    st.markdown("**🔗 Sources Used:**")
                    for src in sources:
                        st.markdown(f"- [{src}]({src})")

                # Save chat
                st.session_state.news_qa_history.append({
                    "question": user_query, "answer": answer, "sources": list(sources)
                })

            except Exception as e:
                st.error(f"❌ Error during Q&A: {e}")

    # Show Q&A history
    if st.session_state.news_qa_history:
        st.markdown("---")
        st.markdown("### 📝 Q&A History")
        full_chat = ""
        for i, qa in enumerate(st.session_state.news_qa_history, 1):
            st.markdown(f"**Q{i}:** {qa['question']}")
            st.markdown(f"**A{i}:** {qa['answer']}")
            if qa.get("sources"):
                st.markdown("**Sources:**")
                for src in qa["sources"]:
                    st.markdown(f"- [{src}]({src})")
            full_chat += f"Q{i}: {qa['question']}\nA{i}: {qa['answer']}\nSources: {', '.join(qa.get('sources', []))}\n\n"

        st.download_button("⬇ Download Chat History", full_chat, "news_chat_history.txt", "text/plain")
