# csv_analyzer.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO, BytesIO

def csv_analyzer_page():
    st.markdown("""
    <div class="main-card">
        <h2>📊 CSV Analyzer</h2>
        <p>Upload your CSV file, view stats, and generate graphs.</p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"], key="csv_upload")

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file, encoding ='latin1')
            st.session_state.csv_df = df  # Store DataFrame in session state
            st.success("✅ CSV File Uploaded Successfully!")

            st.subheader("📄 File Overview")
            st.write(st.session_state.csv_df.head())

            st.subheader("📊 Statistical Summary (.describe())")
            st.write(st.session_state.csv_df.describe())

            st.subheader("ℹ Dataset Info (.info())")
            buffer = StringIO()
            st.session_state.csv_df.info(buf=buffer)
            info_str = buffer.getvalue()
            info_lines = info_str.strip().split('\n')
            info_clean = []
            for line in info_lines:
                if ':' in line:
                    parts = line.split(':', 1)
                    info_clean.append(f"**{parts[0].strip()}**: {parts[1].strip()}")
                else:
                    info_clean.append(line)
            for line in info_clean:
                st.markdown(f"- {line}")

            st.subheader("📉 Dynamic Graph Generator")
            chart_type = st.selectbox("Select Chart Type", ["Line", "Bar", "Scatter", "Area", "Box", "Histogram", "Heatmap"], key="chart_type")
            x_cols = st.multiselect("Select X-axis column(s)", st.session_state.csv_df.columns, key="x_cols")
            y_cols = st.multiselect("Select Y-axis column(s)", st.session_state.csv_df.columns, key="y_cols")

            if st.button("Generate Graph", key="generate_graph_button"):
                if not x_cols or not y_cols:
                    st.warning("Please select at least one column for both X and Y axes.")
                else:
                    fig, ax = plt.subplots(figsize=(10, 6))
                    try:
                        if chart_type == "Line":
                            for y in y_cols:
                                st.session_state.csv_df.plot(x=x_cols[0], y=y, ax=ax, kind='line')
                        elif chart_type == "Bar":
                            for y in y_cols:
                                st.session_state.csv_df.plot(x=x_cols[0], y=y, ax=ax, kind='bar')
                        elif chart_type == "Scatter":
                            for y in y_cols:
                                sns.scatterplot(x=st.session_state.csv_df[x_cols[0]], y=st.session_state.csv_df[y], ax=ax)
                        elif chart_type == "Area":
                            st.session_state.csv_df[x_cols + y_cols].plot.area(ax=ax)
                        elif chart_type == "Box":
                            st.session_state.csv_df[y_cols].plot.box(ax=ax)
                        elif chart_type == "Histogram":
                            st.session_state.csv_df[y_cols].plot.hist(ax=ax, alpha=0.7)
                        elif chart_type == "Heatmap":
                            corr = st.session_state.csv_df.corr(numeric_only=True)
                            sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)

                        ax.set_title(f"{chart_type} Chart")
                        st.pyplot(fig)

                        buf = BytesIO()
                        fig.savefig(buf, format="png")
                        st.download_button("📥 Download Graph", data=buf.getvalue(), file_name="generated_graph.png", mime="image/png")
                    except Exception as e:
                        st.error(f"Error while plotting graph: {e}")

        except pd.errors.EmptyDataError:
            st.error("❌ Uploaded file is empty.")
        except Exception as e:
            st.error(f"❌ Error reading CSV file: {e}")
    elif "csv_df" in st.session_state and st.session_state.csv_df is not None:
        st.subheader("📄 File Overview")
        st.write(st.session_state.csv_df.head())

        st.subheader("📊 Statistical Summary (.describe())")
        st.write(st.session_state.csv_df.describe())

        st.subheader("ℹ Dataset Info (.info())")
        buffer = StringIO()
        st.session_state.csv_df.info(buf=buffer)
        info_str = buffer.getvalue()
        info_lines = info_str.strip().split('\n')
        info_clean = []
        for line in info_lines:
            if ':' in line:
                parts = line.split(':', 1)
                info_clean.append(f"**{parts[0].strip()}**: {parts[1].strip()}")
            else:
                info_clean.append(line)
        for line in info_clean:
            st.markdown(f"- {line}")

        st.subheader("📉 Dynamic Graph Generator")
        chart_type = st.selectbox("Select Chart Type", ["Line", "Bar", "Scatter", "Area", "Box", "Histogram", "Heatmap"], key="chart_type")
        x_cols = st.multiselect("Select X-axis column(s)", st.session_state.csv_df.columns, key="x_cols")
        y_cols = st.multiselect("Select Y-axis column(s)", st.session_state.csv_df.columns, key="y_cols")

        if st.button("Generate Graph", key="generate_graph_button"):
            if not x_cols or not y_cols:
                st.warning("Please select at least one column for both X and Y axes.")
            else:
                fig, ax = plt.subplots(figsize=(10, 6))
                try:
                    if chart_type == "Line":
                        for y in y_cols:
                            st.session_state.csv_df.plot(x=x_cols[0], y=y, ax=ax, kind='line')
                    elif chart_type == "Bar":
                        for y in y_cols:
                            st.session_state.csv_df.plot(x=x_cols[0], y=y, ax=ax, kind='bar')
                    elif chart_type == "Scatter":
                        for y in y_cols:
                            sns.scatterplot(x=st.session_state.csv_df[x_cols[0]], y=st.session_state.csv_df[y], ax=ax)
                    elif chart_type == "Area":
                        st.session_state.csv_df[x_cols + y_cols].plot.area(ax=ax)
                    elif chart_type == "Box":
                        st.session_state.csv_df[y_cols].plot.box(ax=ax)
                    elif chart_type == "Histogram":
                        st.session_state.csv_df[y_cols].plot.hist(ax=ax, alpha=0.7)
                    elif chart_type == "Heatmap":
                        corr = st.session_state.csv_df.corr(numeric_only=True)
                        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)

                    ax.set_title(f"{chart_type} Chart")
                    st.pyplot(fig)

                    buf = BytesIO()
                    fig.savefig(buf, format="png")
                    st.download_button("📥 Download Graph", data=buf.getvalue(), file_name="generated_graph.png", mime="image/png")
                except Exception as e:
                    st.error(f"Error while plotting graph: {e}")