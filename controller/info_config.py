
import streamlit as st

#=============================================================================#

model_info_config = {
    "model": st.column_config.TextColumn(
        "模型名稱", 
        help="模型名稱", 
        max_chars=100, 
        width="small"
    ),
    "date": st.column_config.TextColumn(
        "建立日期", 
        help="模型建立日期", 
        max_chars=100, 
        width="small"
    ),
    "size": st.column_config.TextColumn(
        "模型大小", 
        help="模型大小", 
        max_chars=100, 
        width="small"
    ),
    "format": st.column_config.TextColumn(
        "模型格式", 
        help="模型格式", 
        max_chars=100, 
        width="small"
    ),
    "family": st.column_config.TextColumn(
        "模型家族", 
        help="模型家族", 
        max_chars=100, 
        width="small"
    ),
    "parameter_size": st.column_config.TextColumn(
        "模型參數量", 
        help="模型參數量", 
        max_chars=100, 
        width="small"
    ),
    "quantization_level": st.column_config.TextColumn(
        "量化等級", 
        help="量化等級", 
        max_chars=100, 
        width="small"
    ),
}