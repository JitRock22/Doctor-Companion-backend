#pipenv shell
#python brain.py


import os
from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")


#Convert image to required format for Groq API
import base64


def encode_img(filepath):
    with open(filepath, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


#Setup Multimodel LLM

from groq import Groq
def analyze_img_with_query(query,model, encoded_img):
   
    client=Groq(api_key=GROQ_API_KEY)
    messages=[
        {
            "role": "user",
            "content":[
                {
                    "type":"text",
                    "text":query,
                },
                {
                    "type":"image_url",
                    "image_url":{
                        "url": f"data:image/jpeg;base64,{encoded_img}",
                    }
                }
            ]
        }
        ]

    chat_completion=client.chat.completions.create(
        messages=messages,
        model=model,
    )

    return chat_completion.choices[0].message.content