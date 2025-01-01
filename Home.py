
from controller.setting import SettingController
from controller.model import ModelController

import streamlit as st
import time

#=============================================================================#

SettingController = SettingController()
LLM_MODEL         = SettingController.setting['llm_model']

ModelController = ModelController()

#=============================================================================#

st.set_page_config(layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "使用繁體中文回答問題", "response_time": 0}]
    st.session_state.messages.append({"role": "assistant", "content": "✋ Hi~ 請問想詢問什麼問題呢？", "response_time": 0})

#=============================================================================#

st.title("TCW LLM")

#-----------------------------------------------------------------------------#

for message in st.session_state.messages:

    if message["role"] == "user":
        with st.chat_message("user", avatar="🦖"):
            st.markdown(message["content"])

    elif message["role"] == "assistant":
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(message["content"])

            if message['response_time'] > 0:
                st.caption(f'Response Time: {message["response_time"]}')

#-----------------------------------------------------------------------------#

if question := st.chat_input("輸入問題"):

    with st.chat_message("user", avatar="🦖"):
        st.markdown(question)

    st.session_state.messages.append({"role": "user", "content": question})

#-----------------------------------------------------------------------------#

    with st.chat_message("assistant", avatar="🤖"):
        
        start_time = time.time()

        response = st.write_stream(ModelController.generate_response(st.session_state.messages))

        end_time = time.time()

        st.caption(f'Response Time: {round(end_time - start_time, 2)}')

    st.session_state.messages.append({"role": "assistant", "content": response, "response_time": round(end_time - start_time, 2)})
