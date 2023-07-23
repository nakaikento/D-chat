import langchain
langchain.verbose = False
from langchain.schema import prompt
from backend.openai_utils import create_table_definition_prompt
from backend.db_utils import dataframe_to_database, execute_query
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.schema import messages_to_dict
from langchain.prompts.chat import (
      ChatPromptTemplate,
      MessagesPlaceholder,
      SystemMessagePromptTemplate,
      HumanMessagePromptTemplate
)

import pandas as pd
import json
import os
import streamlit as st
from streamlit_chat import message

TABLE_NAME = "Investors"

# データをCSVファイルから読み込み
@st.cache_resource
def load_data():
      FILE_PATH = "backend/data/demo_dummy_data.csv"
      df = pd.read_csv(FILE_PATH)
      return df

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

# 最後に、実際に会話した内容が memory オブジェクトに保持されていることを確認します
# history = memory.chat_memory
# messages = json.dumps(messages_to_dict(history.messages), indent=2, ensure_ascii=False)
# print(f"memory: {messages}")

def main():
      # ヘッダー
      st.header("D-Chat")

      # APIキー管理
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

      # 会話モデルの初期化
      conversation = load_conversation()

      # ユーザ入力待ち受け
      user_input = st.text_input("Query in Natural Language", placeholder="Enter your query here...") or st.button(
        "Execute"
      )

      if user_input:

            message(
                  user_input,
                  is_user=True,
            )

            with st.spinner("Generating response..."):

                  response = conversation.predict(input=user_input)
                  sql_query = "SELECT " + response
                  message(sql_query)
                  result = execute_query(database, sql_query)
                  st.dataframe(result)

if __name__ == "__main__":
    main()