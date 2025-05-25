
from controller.model import ModelController

import streamlit as st
import time

#=============================================================================#

ModelController = ModelController()

#=============================================================================#

def text_to_stream(text):

    for word in text.split(" "):
        yield word + " "
        time.sleep(0.02)

#=============================================================================#

st.set_page_config(layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role"             : "system", 
        "think_content"    : "", 
        "response_content" : "使用繁體中文回答問題", 
        "response_time"    : 0
    },
    {
        "role"             : "assistant", 
        "think_content"    : "", 
        "response_content" : "✋ Hi~ 請問想詢問什麼問題呢？", 
        "response_time"    : 0
    }]

#=============================================================================#

st.title("CAD LLM")

#-----------------------------------------------------------------------------#

for message in st.session_state.messages:

    if message["role"] == "user":
        with st.chat_message("user", avatar="🦖"):
            
            st.markdown(message["response_content"])

    elif message["role"] == "assistant":
        with st.chat_message("assistant", avatar="🤖"):

            if len(message["think_content"]):
                with st.expander("思考過程"):
                    st.write(message['think_content'])

            st.markdown(message["response_content"])

            if message["response_time"] > 0:
                st.caption(f'Response Time: {message["response_time"]}')

#-----------------------------------------------------------------------------#

if question := st.chat_input("輸入問題"):

    with st.chat_message("user", avatar="🦖"):
        st.markdown(question)

    st.session_state.messages.append({
        "role"             : "user", 
        "think_content"    : "", 
        "response_content" : question, 
        "response_time"    : 0
    })

#-----------------------------------------------------------------------------#

    with st.chat_message("assistant", avatar="🤖"):

        start_time = time.time()

        with st.spinner("思考中..."):
            response = ModelController.generate_response(st.session_state.messages)

        end_time = time.time()

        if len(response['think_content']):
            with st.expander("思考過程"):
                st.write(response['think_content'])

        st.write_stream(text_to_stream(response['response_content']))

        st.caption(f'Response Time: {round(end_time - start_time, 2)}')

    st.session_state.messages.append({"role": "assistant", 
        "think_content"    : response['think_content'], 
        "response_content" : response['response_content'], 
        "response_time"    : round(end_time - start_time, 2)
    })
