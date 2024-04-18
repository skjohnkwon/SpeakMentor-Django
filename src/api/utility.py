from openai import OpenAI
import os
from rest_framework.response import Response

def generate_list(words):

    # You are an assistant that generates a list of ONLY REAL words in a RFC8259 compliant JSON response. AVOID single syllable words if possible.
    # Do not include any explanations, only provide a RFC8259 compliant JSON response following this format without deviation.

    # [{
    #   "words": []
    # }]

    client = OpenAI(api_key=os.getenv('OPENAI_SECRET_KEY'))
    thread_id = os.getenv('OPENAI_THREAD_ID_LISTGEN')
    assistant_id = os.getenv('OPENAI_ASSISTANT_ID_LISTGEN')

    words_as_string = ", ".join(words)

    # use assistant to generate list
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=words_as_string
    )

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions="Continue to follow instructions."
    )
    
    if (run.status == "completed"):
        print("run completed")
        messages = client.beta.threads.messages.list(
            thread_id=thread_id
        )
        print(messages.data[0].content[0].text.value)