import streamlit as st
import os
import uuid
from utils import create_vectorstore_from_pdfs, local_css
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA

DATA_DIR = "data"

def initialize_session_state():
    for key, default in [
        ("vectorstores", {}),
        ("pdf_paths", []),
        ("pdf_names", []),
        ("selected_files_sidebar", []),  # To store selected files from sidebar
        ("summary", ""),
        ("chat_sessions", {}),
        ("current_session_id", None),
    ]:
        if key not in st.session_state:
            st.session_state[key] = default

def start_new_chat_session(pdf_paths_for_session):
    if not pdf_paths_for_session:
        st.sidebar.error("Please select at least one document to start a new chat.")
        return None

    session_id = str(uuid.uuid4())
    label = ", ".join([os.path.basename(p) for p in pdf_paths_for_session])
    st.session_state.chat_sessions[session_id] = {
        "pdfs": pdf_paths_for_session.copy(),
        "messages": [],
        "summary": "",
        "label": label
    }
    st.session_state.current_session_id = session_id
    return session_id

def select_chat_session():
    if st.session_state.chat_sessions:
        session_ids = list(st.session_state.chat_sessions.keys())
        session_labels = [
            st.session_state.chat_sessions[sid].get("label", f"Session {i+1}")
            for i, sid in enumerate(session_ids)
        ]
        idx = st.sidebar.selectbox("💬 Chat Sessions", range(len(session_ids)), format_func=lambda i: session_labels[i])
        st.session_state.current_session_id = session_ids[idx]
    else:
        st.sidebar.info("No chat sessions yet.")

def pdf_insights_page():
    initialize_session_state()
    local_css("style.css")

    st.markdown("""
        <div class="main-card">
            <h2>📁 Upload PDFs, Select Model & Chat</h2>
            <p>Extract insights and chat with your financial documents.</p>
        </div>
    """, unsafe_allow_html=True)

    # --- PDF Upload Section ---
    with st.form("pdf_upload_form"):
        uploaded_files = st.file_uploader("📄 Upload PDF Files", type=["pdf"], accept_multiple_files=True)
        model_name = st.selectbox("🤖 Select Groq Model", [
            "llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768"
        ])
        process = st.form_submit_button("✅ Process PDFs")

    newly_uploaded_paths = []
    if process and uploaded_files:
        os.makedirs(DATA_DIR, exist_ok=True)
        for pdf in uploaded_files:
            path = os.path.join(DATA_DIR, pdf.name)
            if path not in st.session_state.pdf_paths:
                with open(path, "wb") as f:
                    f.write(pdf.getbuffer())
                st.session_state.pdf_paths.append(path)
                st.session_state.pdf_names.append(pdf.name)
                newly_uploaded_paths.append(path)

        if newly_uploaded_paths:
            st.success(f"✅ Uploaded {len(newly_uploaded_paths)} new document(s) successfully!")
            with st.spinner("🔄 Processing and embedding new PDFs..."):
                for path in newly_uploaded_paths:
                    if path not in st.session_state.vectorstores:
                        vs = create_vectorstore_from_pdfs([path])
                        st.session_state.vectorstores[path] = vs
            st.success("✅ Vector stores created for newly uploaded documents!")
            # Automatically start a new chat session with newly uploaded files
            if newly_uploaded_paths:
                new_session_id = start_new_chat_session(newly_uploaded_paths)
                if new_session_id:
                    st.sidebar.success(f"🚀 Started a new chat session with the uploaded documents.")
        else:
            st.info("No new documents uploaded.")

    # --- Sidebar: Document Selection and Sessions ---
    st.sidebar.title("🗂️ Chat Sessions")

    # Display existing files in the data directory for selection
    if os.path.exists(DATA_DIR):
        pdf_files_in_data = [f for f in os.listdir(DATA_DIR) if f.endswith(".pdf")]
        if pdf_files_in_data:
            st.sidebar.subheader("📁 Select Documents for New Chat")
            st.session_state.selected_files_sidebar = st.sidebar.multiselect(
                "Choose files:",
                options=pdf_files_in_data,
                default=[],  # Start with no files selected by default
            )

            selected_paths_sidebar = [os.path.join(DATA_DIR, f) for f in st.session_state.selected_files_sidebar]

            if st.sidebar.button("➕ New Chat with Selected"):
                if selected_paths_sidebar:
                    # Ensure vector stores exist for selected files
                    with st.spinner("🔄 Creating embeddings for selected documents if they don't exist..."):
                        for path in selected_paths_sidebar:
                            if path not in st.session_state.vectorstores:
                                vs = create_vectorstore_from_pdfs([path])
                                if vs:
                                    st.session_state.vectorstores[path] = vs
                                else:
                                    st.error(f"❌ Error creating vector store for {os.path.basename(path)}.")
                                    return

                    # Now start the new chat session
                    new_session_id = start_new_chat_session(selected_paths_sidebar)
                    if new_session_id:
                        st.sidebar.success(f"🚀 Started a new chat session with selected documents.")
                else:
                    st.sidebar.warning("Please select at least one document to start a new chat.")
        else:
            st.sidebar.info("No PDF documents found in the 'data' directory.")
    else:
        st.sidebar.info("The 'data' directory does not exist.")

    select_chat_session()

    # --- Main Area: Show Current Session ---
    if st.session_state.current_session_id:
        session = st.session_state.chat_sessions[st.session_state.current_session_id]
        session_pdfs = session["pdfs"]
        st.markdown(f"**Current Session PDFs:** {', '.join([os.path.basename(p) for p in session_pdfs])}")

        # --- Generate Summary ---
        if st.button("🧠 Generate Summary for This Session"):
            groq_api_key = os.getenv("GROQ_API_KEY")
            if not groq_api_key:
                st.error("GROQ_API_KEY not set in environment.")
                st.stop()
            retrievers = [
                st.session_state.vectorstores[path].as_retriever(search_kwargs={"k": 5})
                for path in session_pdfs if path in st.session_state.vectorstores
            ]
            if not retrievers:
                st.error("No vectorstores found for selected PDFs.")
            else:
                retriever = retrievers[0]
                llm = ChatGroq(groq_api_key=groq_api_key, model_name=model_name)
                chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
                prompt = """
                    Provide a comprehensive summary of the uploaded financial document(s) with key metrics, events, risks,
                    insights, and recommendations. Include tone, trends, and future implications.
                """
                try:
                    result = chain.invoke({"query": prompt})
                    session["summary"] = result.get("result", "")
                    st.success("📌 Summary generated successfully.")
                except Exception as e:
                    st.error(f"❌ Error generating summary: {e}")

        if session.get("summary"):
            st.markdown("""
            <div class="main-card">
                <h3>📌 Summary</h3>
            """, unsafe_allow_html=True)
            st.markdown(session["summary"])
            st.download_button("⬇ Download Summary", session["summary"], "summary.txt", "text/plain")
            st.markdown("</div>", unsafe_allow_html=True)

        # --- Chat Area ---
        st.markdown("""
        <div class="main-card">
            <h3>✨ Chat with Your PDF(s)</h3>
        """, unsafe_allow_html=True)
        for msg in session["messages"]:
            st.chat_message(msg["role"]).markdown(msg["content"])

        user_input = st.chat_input("Ask a question about the selected PDF(s)...")
        if user_input:
            st.chat_message("user").markdown(user_input)
            session["messages"].append({"role": "user", "content": user_input})

            custom_prompt = f"""
                You are a knowledgeable AI assistant. Answer the following query using *only the content* from the selected document(s).

                📝 Instructions:
                - Respond strictly based on the uploaded content.
                - Structure your response using *clear and concise bullet points*.
                - Each bullet point must convey a *complete, self-contained insight or fact*.
                - If the content does *not* contain relevant information, reply with:
                "No content available."

                📌 Query: {user_input}
            """
            groq_api_key = os.getenv("GROQ_API_KEY")
            retrievers = [
                st.session_state.vectorstores[path].as_retriever(search_kwargs={"k": 4})
                for path in session_pdfs if path in st.session_state.vectorstores
            ]
            if not retrievers:
                st.error("No vectorstores found for selected PDFs.")
            else:
                retriever = retrievers[0]
                llm = ChatGroq(groq_api_key=groq_api_key, model_name=model_name)
                chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
                try:
                    result = chain.invoke({"query": custom_prompt})
                    response = result.get("result", "No answer found.")
                    st.chat_message("assistant").markdown(response)
                    session["messages"].append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"❌ Chat failed: {e}")

        if session["messages"]:
            chat_text = ""
            for msg in session["messages"]:
                role = msg["role"].capitalize()
                content = msg["content"]
                chat_text += f"{role}: {content}\n\n"
            st.download_button(
                label="⬇ Download Chat History",
                data=chat_text,
                file_name="chat_history.txt",
                mime="text/plain"
            )
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("No chat session selected. Start a new chat from the sidebar.")

    if not st.session_state.pdf_paths:
        st.info("Please upload PDF files to start chatting or generating summaries.")

if __name__ == "__main__":
    pdf_insights_page()