import streamlit as st

def home_page():
    st.markdown("""
    <div class="main-card">
        <span class="info-badge">
            Introducing FinSight AI
        </span>
        <h1 style="font-size:2.6rem; margin-top:1.2rem; margin-bottom:0.6rem;">
            The best way to analyze <span style="color:#1976D2;">financial data</span> with AI
        </h1>
        <p style="font-size:1.18rem; color:#22356F; margin-bottom:2rem;">
            Upload PDFs or CSVs, ask questions, generate summaries, and visualize your insights – all with a modern AI-powered assistant.
        </p>
        <a href="https://github.com/" target="_blank" style="text-decoration:none;">
            <button class="main-btn">
                ⭐ Give us a star
            </button>
        </a>
    </div>

    <div style="background:#F6F8FB; border-radius:16px; padding:1.5rem; margin-top:2rem; border: 1px solid #E3EAF2; box-shadow: 0 2px 12px rgba(25,118,210,0.05);">
        <h4 style='color:#1976D2; margin-bottom:0.7rem; font-weight:700;'>📜 Terms & Conditions</h4>
        <div style="font-size:0.95rem; color:#555;">
            <strong>🔒 Data Privacy:</strong>
            <ul style="padding-left: 1.2rem; margin-bottom: 0.7rem;">
                <li style="margin-bottom: 0.3rem;">Documents are processed within session for analysis.</li>
                <li style="margin-bottom: 0.3rem;">No personal data is stored permanently.</li>
                <li style="margin-bottom: 0.3rem;">Communication is encrypted.</li>
            </ul>
            <strong>🆕 Updates:</strong>
            <ul style="padding-left: 1.2rem; margin-bottom: 0.7rem;">
                <li style="margin-bottom: 0.3rem;">Terms may evolve with feature updates.</li>
            </ul>
            <strong>⚠️ Limitations:</strong>
            <ul style="padding-left: 1.2rem; margin-bottom: 0.7rem;">
                <li style="margin-bottom: 0.3rem;">Responses may not always be 100% accurate.</li>
                <li style="margin-bottom: 0.3rem;">FinSight aims to minimize hallucinations.</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)