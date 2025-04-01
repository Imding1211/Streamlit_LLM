image_part = {
    "type": "image_url",
    "image_url": f"data:image/jpeg;base64,",
}

content_parts = []

text_part = {"type": "text", "text": ""}

content_parts.append(image_part)
content_parts.append(text_part)

print(content_parts)