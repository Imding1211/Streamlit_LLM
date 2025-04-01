import base64
from io import BytesIO

from PIL import Image


def convert_to_base64(file_path):

    pil_image = Image.open(file_path)

    buffered = BytesIO()
    pil_image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return img_str

file_path = "/Users/imding1211/Pictures/wallpaperflare.com_wallpaper.jpg"
image_b64 = convert_to_base64(file_path)

from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama

llm = ChatOllama(model="gemma3:4b", temperature=0)


def prompt_func(data):
    text = data["text"]
    image = data["image"]

    image_part = {
        "type": "image_url",
        "image_url": f"data:image/jpeg;base64,{image}",
    }

    content_parts = []

    text_part = {"type": "text", "text": text}

    content_parts.append(image_part)
    content_parts.append(text_part)

    return [HumanMessage(content=content_parts)]


from langchain_core.output_parsers import StrOutputParser

chain = prompt_func | llm 

query_chain = chain.invoke(
    {"text": "What is in the image?", "image": image_b64}
)

print(query_chain.content)