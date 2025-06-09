import openai
import base64
import os
from app.config import settings

openai.api_key = settings.OPENAI_API_KEY

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        image_bytes = img_file.read()
        base64_image = base64.b64encode(image_bytes).decode("utf-8")

        ext = image_path.lower().split(".")[-1]
        if ext == "png":
            mime_type = "image/png"
        elif ext in ["jpg", "jpeg"]:
            mime_type = "image/jpeg"
        else:
            raise ValueError("Unsupported file type. Use PNG or JPEG.")

        return f"data:{mime_type};base64,{base64_image}"

def extract_text_from_image(image_path):
    try:
        image_data_url = encode_image_to_base64(image_path)

        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extract and organize the text from this image using Markdown formatting."},
                        {"type": "image_url", "image_url": {"url": image_data_url}}
                    ]
                }
            ],
            max_tokens=2000
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"
