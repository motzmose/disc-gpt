import os
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

if os.getenv("LOCAL_DEV"):
    client = OpenAI(base_url=os.getenv("LOCAL_DEV_BASE_URL")+os.getenv("LOCAL_DEV_ENDPOINT_PREFIX"), api_key=os.getenv("LOCAL_DEV_API_KEY"))
    model=os.getenv("LOCAL_DEV_MODEL")
else:
    client = OpenAI()
    model=os.getenv("OPENAI_MODEL")

def send_to_chatGPT(messages, model=model):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=os.getenv("MAX_TOKENS"),
        n=1,
        stop=None,
        temperature=os.getenv("TEMPERATURE"),
    )
    
    message = response.choices[0].message.content
    messages.append(response.choices[0].message)
    return message