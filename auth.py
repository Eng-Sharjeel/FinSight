import streamlit as st

# --- Hardcoded login credentials ---
USER_CREDENTIALS = {
    "admin": "admin123",
    "user": "user123"
}

# --- Login Page ---
def login_page():
    st.markdown("<h1 style='color: #1976D2; font-size:2.5rem;'>🔐 Secure Login</h1>", unsafe_allow_html=True)
    with st.form("login_form"):
        username = st.text_input("👤 Username")
        password = st.text_input("🔑 Password", type="password")
        login = st.form_submit_button("🚪 Login")
        if login:
            if USER_CREDENTIALS.get(username) == password:
                st.session_state.logged_in = True
                st.session_state.page = "Home"
                st.rerun() # Rerun the app to navigate to the home page
            else:
                st.error("❌ Invalid username or password")
    st.stop() # Stop execution until login is successful