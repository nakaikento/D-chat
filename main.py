import langchain
langchain.verbose = False
from langchain.schema import prompt
from backend.openai_utils import create_table_definition_prompt
from backend.db_utils import dataframe_to_database, execute_query, load_data
from langchain.prompts.chat import (
      ChatPromptTemplate,
      MessagesPlaceholder,
      SystemMessagePromptTemplate,
      HumanMessagePromptTemplate
)
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
import pandas as pd
import os
import streamlit as st
from streamlit_chat import message

TABLE_NAME = "Investors"

# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="D-Chat", page_icon="chart_with_upwards_trend")
st.header("D-Chat")
col1, col2 = st.columns([0.5,0.5], gap="large")
col1.subheader("Chat")
col2.subheader("Data View")

@st.cache_resource
def load_conversation():
      # 言語モデルのラッパー
      chat = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            max_tokens=150,
            model_kwargs={
                  "top_p":1.0,
                  "frequency_penalty":0.0,
                  "presence_penalty":0.0,
                  "stop":["#", ";"]
            }
      )

      # メモリオブジェクト
      memory = ConversationBufferMemory(return_messages=True)

      # 会話用のチェーン
      conversation = ConversationChain(llm=chat, memory=memory, prompt=prompt)
      
      return conversation

# データ読み込み
df = load_data()

# SQLite DBにデータを挿入
database = dataframe_to_database(df, TABLE_NAME) 

# システムメッセージ用のテンプレート
template = create_table_definition_prompt(df, TABLE_NAME)

# プロンプトテンプレート
prompt = ChatPromptTemplate.from_messages([
      SystemMessagePromptTemplate.from_template(template),
      MessagesPlaceholder(variable_name="history"),
      HumanMessagePromptTemplate.from_template("### A query to answer: {input}\nSELECT")
])

def main():

      # APIキー管理
      if 'openai_api_key' not in st.session_state:
            with col1:
                  openai_api_key = st.sidebar.text_input(
                        'Please enter your OpenAI API key or [get one here](https://platform.openai.com/account/api-keys)', value="", placeholder="Enter the OpenAI API key which begins with sk-"
                  )
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

      # 会話モデルの初期化
      conversation = load_conversation()

      # Initialize the session state for generated responses and past inputs
      if 'generated' not in st.session_state:
            st.session_state['generated'] = []
      if 'past' not in st.session_state:
            st.session_state['past'] = []
      # if 'dataview' not in st.session_state:
      #       st.session_state['dataview'] = pd.DataFrame()

      # ユーザ入力待ち受け
      with col1:
            user_input = st.text_input("Query in Natural Language", placeholder="Enter your query here...") or st.button("Execute")

      if user_input:

            with st.spinner("Generating response..."):

                  response = conversation.predict(input=user_input)
                  sql_query = "SELECT " + response
                  st.session_state.past.append(user_input)
                  st.session_state.generated.append(sql_query)
                  result = execute_query(database, sql_query)
                  # st.session_state.dataview.append(result)
                  with col2:
                        st.dataframe(result)
                  
      # If there are generated responses, display the conversation using Streamlit messages
      if st.session_state['generated']:
            for i in range(len(st.session_state['generated'])):
                  with col1:
                        message(st.session_state['past'][i],
                              is_user=True, key=str(i) + '_user')
                        message(st.session_state["generated"][i], key=str(i))
      
                  # with col2:
                  #       st.dataframe(st.session_state['dataview'][i])

if __name__ == "__main__":
    main()