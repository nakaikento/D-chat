import streamlit as st
from streamlit_chat import message
from backend.core import run_llm

st.header("D-Chat")

user_input = st.text_input("Query in NLP", placeholder="Enter your query here...") or st.button(
    "Execute"
)

if user_input:
    with st.spinner("Generating response..."):
        query_in_sql, result = run_llm(
            user_input=user_input
        )
        message(query_in_sql)
        st.dataframe(result)