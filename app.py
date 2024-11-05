import streamlit as st
from database.vector_store import VectorStore
from llm.error_processor import ErrorProcessor
from scraper.error_collector import ErrorCollector
import pandas as pd
import plotly.express as px


def init_session_state():
    if 'vector_store' not in st.session_state:
        st.session_state.vector_store = VectorStore()
    if 'error_processor' not in st.session_state:
        st.session_state.error_processor = ErrorProcessor()
    if 'error_collector' not in st.session_state:
        st.session_state.error_collector = ErrorCollector()


def main():
    st.set_page_config(
        page_title="Error Encyclopedia",
        page_icon="🔍",
        layout="wide"
    )

    init_session_state()

    st.title("Error Encyclopedia 📚")

    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Choose a page",
        ["Error Analysis", "Error Database", "Collect New Errors"]
    )

    if page == "Error Analysis":
        show_error_analysis()
    elif page == "Error Database":
        show_error_database()
    else:
        show_error_collection()


def show_error_analysis():
    st.header("Error Analysis")

    # Input section
    error_text = st.text_area(
        "Paste your error message here:",
        height=150
    )

    if st.button("Analyze Error"):
        if error_text:
            with st.spinner("Analyzing error..."):
                # Get similar errors
                similar_errors = st.session_state.vector_store.similarity_search(
                    error_text,
                    k=3
                )

                # Process error
                analysis = st.session_state.error_processor.process_error(
                    error_text,
                    [doc.page_content for doc in similar_errors]
                )

                # Display results
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Error Analysis")
                    st.write("**Error Type:**", analysis['error_type'])
                    st.write("**Root Cause:**", analysis['root_cause'])

                    st.subheader("Solution Steps")
                    for idx, step in enumerate(analysis['solution_steps'], 1):
                        st.write(f"{idx}. {step}")

                with col2:
                    st.subheader("Prevention Tips")
                    for idx, tip in enumerate(analysis['prevention_tips'], 1):
                        st.write(f"{idx}. {tip}")

                    st.subheader("Similar Errors")
                    for doc in similar_errors:
                        with st.expander("View Similar Error"):
                            st.write(doc.page_content)
                            if hasattr(doc.metadata, 'url'):
                                st.write(f"[Source]({doc.metadata['url']})")


def show_error_database():
    st.header("Error Database")

    # Search functionality
    search_query = st.text_input("Search errors:")

    if search_query:
        results = st.session_state.vector_store.similarity_search(
            search_query,
            k=10
        )

        for idx, doc in enumerate(results, 1):
            with st.expander(f"Result {idx}"):
                st.write(doc.page_content)
                if hasattr(doc.metadata, 'url'):
                    st.write(f"[Source]({doc.metadata['url']})")


def show_error_collection():
    st.header("Collect New Errors")

    col1, col2 = st.columns(2)

    with col1:
        language = st.selectbox(
            "Select Programming Language",
            ["python", "javascript", "java", "cpp"]
        )

    with col2:
        max_errors = st.number_input(
            "Maximum errors to collect",
            min_value=10,
            max_value=100,
            value=50
        )

    if st.button("Collect Errors"):
        with st.spinner("Collecting errors..."):
            # Collect from GitHub
            github_errors = st.session_state.error_collector.collect_github_errors(
                language,
                max_errors // 2
            )

            # Collect from Stack Overflow
            stackoverflow_errors = st.session_state.error_collector.collect_stackoverflow_errors(
                language,
                max_errors // 2
            )

            # Add to vector store
            all_errors = github_errors + stackoverflow_errors
            texts = [f"{err['title']}\n{err['body']}" for err in all_errors]
            metadatas = [{'url': err['url'], 'source': err['source']} for err in all_errors]

            st.session_state.vector_store.add_texts(texts, metadatas)

            # Show statistics
            st.success(f"Collected {len(all_errors)} new errors!")

            # Show distribution
            source_dist = pd.DataFrame({
                'source': [err['source'] for err in all_errors]
            }).value_counts().reset_index()
            source_dist.columns = ['Source', 'Count']

            fig = px.pie(
                source_dist,
                values='Count',
                names='Source',
                title='Error Sources Distribution'
            )
            st.plotly_chart(fig)


if __name__ == "__main__":
    main()
