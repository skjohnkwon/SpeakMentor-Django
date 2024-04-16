import openai
import os
import requests
import json
from rest_framework.response import Response

def generate_list(words):
    client = openai.Client()

    OPENAI_SECRET_KEY = os.getenv('OPENAI_SECRET_KEY')
    OPENAI_ENDPOINT = os.getenv('OPENAI_ENDPOINT')
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_SECRET_KEY}",
    }

    prompt = f"Give a concise articulation tip on how to improve the fluency of this sentence \"{content}\". Make it optimized for speaking not writing. One sentence only."
    message = [{"role": "user", "content": prompt}]
    data = {
        "model": 'gpt-4-0125-preview',
        "messages": message,
        "temperature": 1,
    }
    response = requests.post(OPENAI_ENDPOINT, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        suggestion = response.json()["choices"][0]["message"]["content"]
        return suggestion
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")