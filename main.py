import streamlit as st
from streamlit_chat import message
from backend.core import run_llm
import os

def main():
    st.header("D-Chat")

    st.sidebar.title("Menu")

    if 'openai_api_key' not in st.session_state:
        openai_api_key = st.text_input(
            'Please enter your OpenAI API key or [get one here](https://platform.openai.com/account/api-keys)', value="", placeholder="Enter the OpenAI API key which begins with sk-")
        if openai_api_key:
            st.session_state.openai_api_key = openai_api_key
            os.environ["OPENAI_API_KEY"] = openai_api_key
        else:
            #warning_text = 'Please enter your OpenAI API key. Get yours from here: [link](https://platform.openai.com/account/api-keys)'
            #warning_html = f'<span>{warning_text}</span>'
            #st.markdown(warning_html, unsafe_allow_html=True)
            return
    else:
        os.environ["OPENAI_API_KEY"] = st.session_state.openai_api_key

    user_input = st.text_input("Query in NLP", placeholder="Enter your query here...") or st.button(
        "Execute"
    )

    if user_input:
        message(
                user_input,
                is_user=True,
            )

        with st.spinner("Generating response..."):
            query_in_sql, result = run_llm(
                user_input=user_input
            )
            message(query_in_sql)
            st.dataframe(result)

if __name__ == "__main__":
    main()