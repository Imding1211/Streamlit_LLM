
from controller.setting import SettingController

import streamlit as st

version = 1.3

#=============================================================================#

SettingController = SettingController()
base_url          = SettingController.setting['base_url']

#=============================================================================#

st.set_page_config(layout="wide")

#=============================================================================#

st.title("設定")

#-----------------------------------------------------------------------------#

base_url_container = st.container(border=True)

base_url_container.text_input("URL", 
    base_url,
    key="base_url",
    )

if base_url_container.button("確認", key=4):
    SettingController.change_base_url(st.session_state.base_url)
    st.toast('URL已更新。')

if st.button("還原初始設定"):
	SettingController.generate_default_setting()
	st.toast('已還原初始設定。')

st.caption(f"版本:{version}")