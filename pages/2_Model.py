
from controller.info_config import model_info_config
from controller.setting import SettingController
from controller.model import ModelController

import streamlit as st

#=============================================================================#

SettingController  = SettingController()
selected_llm       = SettingController.setting['llm_model']

ModelController = ModelController()
ollama_info     = ModelController.ollama_to_dataframe()
list_llm_model  = ollama_info[ollama_info["family"] != "bert"]["model"].tolist()

#=============================================================================#

def change_llm_model():
    SettingController.change_llm_model(st.session_state.llm_model)

#=============================================================================#

st.set_page_config(layout="wide")

#=============================================================================#

st.header("語言模型")

#-----------------------------------------------------------------------------#

llm_warning = st.empty()

#-----------------------------------------------------------------------------#

if selected_llm in list_llm_model:
    index_llm = list_llm_model.index(selected_llm)
else:
    llm_warning.error(f'{selected_llm}語言模型不存在，請重新選擇。', icon="🚨")
    index_llm = None

st.selectbox("請選擇語言模型:", 
    list_llm_model, 
    on_change=change_llm_model, 
    key='llm_model', 
    index=index_llm,
    placeholder='語言模型不存在，請重新選擇。'
    )

st.dataframe(
    ollama_info[ollama_info["family"] != "bert"],
    column_config=model_info_config,
    use_container_width=True,
    hide_index=True
    )
