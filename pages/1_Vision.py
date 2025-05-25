
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

if "messages_v" not in st.session_state:
    st.session_state.messages_v = [{
        "role"             : "system", 
        "response_content" : "使用繁體中文回答問題", 
        "image_content"    : "",
        "image_b64"        : "",
        "response_time"    : 0
    },
    {
        "role"             : "assistant", 
        "response_content" : "✋ Hi~ 請問想詢問什麼問題呢？", 
        "image_content"    : "", 
        "image_b64"        : "",
        "response_time"    : 0
    }]

#=============================================================================#

st.title("CAD LLM Vision")

#-----------------------------------------------------------------------------#

if LLM_MODEL in ["gemma3:1b", "gemma3:4b","gemma3:12b","gemma3:27b", "llama3.2-vision:latest"]:

    for message in st.session_state.messages_v:

        if message["role"] == "user":
            with st.chat_message("user", avatar="🦖"):

                if message["image_content"] != "":
                    st.image(message["image_content"], width=300)                

                st.markdown(message["response_content"])

        elif message["role"] == "assistant":
            with st.chat_message("assistant", avatar="🤖"):

                st.markdown(message["response_content"])

                if message["response_time"] > 0:
                    st.caption(f'Response Time: {message["response_time"]}')

#-----------------------------------------------------------------------------#

    if question := st.chat_input("輸入問題", accept_file=True, file_type=["jpg", "jpeg", "png"]):

        with st.chat_message("user", avatar="🦖"):

            if question and question["files"]:
                st.image(question["files"][0], width=300)

                image_b64 = ModelController.convert_to_base64(question["files"][0])

                st.session_state.messages_v.append({
                    "role"             : "user", 
                    "response_content" : question.text, 
                    "image_content"    : question["files"][0], 
                    "image_b64"        : image_b64,
                    "response_time"    : 0
                })
            
            else:
                st.session_state.messages_v.append({
                    "role"             : "user", 
                    "response_content" : question.text, 
                    "image_content"    : "", 
                    "image_b64"        : "",
                    "response_time"    : 0
                })

            if question and question.text:
                st.markdown(question.text)

#-----------------------------------------------------------------------------#

        with st.chat_message("assistant", avatar="🤖"):

            start_time = time.time()

            with st.spinner("思考中..."):
                response = st.write_stream(ModelController.generate_response_vision(
                    st.session_state.messages_v[-1]["response_content"], 
                    st.session_state.messages_v[-1]["image_b64"]
                ))

            end_time = time.time()

            st.caption(f'Response Time: {round(end_time - start_time, 2)}')

        st.session_state.messages_v.append({
            "role"             : "assistant", 
            "response_content" : response, 
            "image_content"    : "", 
            "image_b64"        : "",
            "response_time"    : round(end_time - start_time, 2)
        })

else:
    with st.chat_message("assistant", avatar="🤖"):
        st.write("你選的模型不支援vision喔，請到Model頁面重新選擇～")
