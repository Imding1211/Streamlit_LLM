
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from typing import Dict, Generator
from ollama import Client
from io import BytesIO
from PIL import Image

from controller.setting import SettingController

import pandas as pd
import humanize
import base64
import re


#=============================================================================#

class ModelController():

    def __init__(self):

        self.SettingController = SettingController()
        self.llm_model         = self.SettingController.setting['llm_model']
        self.base_url          = self.SettingController.setting['base_url']
        self.client            = Client(host=self.base_url)
        self.llm               = ChatOllama(model=self.llm_model, base_url=self.base_url)

#-----------------------------------------------------------------------------#

    def ollama_to_dataframe(self):

        json_info = self.client.list()

        df_info = pd.DataFrame({
            'model'             : [info['model'] for info in json_info['models']],
            'date'              : [info['modified_at'].strftime("%Y-%m-%d %H:%M:%S") for info in json_info['models']],
            'size'              : [humanize.naturalsize(info['size'], binary=True) for info in json_info['models']],
            'format'            : [info['details']['format'] for info in json_info['models']],
            'family'            : [info['details']['family'] for info in json_info['models']],
            'parameter_size'    : [info['details']['parameter_size'] for info in json_info['models']],
            'quantization_level': [info['details']['quantization_level'] for info in json_info['models']]
            })

        return df_info

#-----------------------------------------------------------------------------#

    def generate_response(self, messages: list) -> dict:

        response = self.llm.invoke([(item['role'], item['response_content']) for item in messages])

        match = re.search(r"<think>(.*?)</think>\s*(.*)", response.content, re.DOTALL)

        if match:
            think_content    = match.group(1).strip()
            response_content = match.group(2).strip()

            return {"think_content": think_content, "response_content": response_content}

        else:
            return {"think_content": "", "response_content": response.content}

#-----------------------------------------------------------------------------#

    def generate_response_vision(self, text: str, image:str) -> Generator:

        content_parts = []

        if image != "":

            image_part = {
                "type": "image_url",
                "image_url": f"data:image/jpeg;base64,{image}"
                }

            content_parts.append(image_part)

        text_part = {
            "type": "text", 
            "text": text
            }
            
        content_parts.append(text_part)

        for chunk in self.llm.stream([HumanMessage(content=content_parts)]):
             yield chunk.content

#-----------------------------------------------------------------------------#

    def convert_to_base64(self, file_path):

        pil_image = Image.open(file_path)

        buffered = BytesIO()
        pil_image.save(buffered, format="JPEG")

        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

        return img_str

