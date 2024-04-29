import openai
import os
from rest_framework.response import Response

# def generate_list():
#     client = OpenAI(api_key=os.getenv('OPENAI_SECRET_KEY'))
#     assistant_id = os.getenv('OPENAI_ASSISTANT_ID_LISTGEN')
#     # use assistant to generate list
#     thread_id = client.beta.threads.create().id
#     client.beta.threads.messages.create(
#         thread_id=thread_id,
#         role="user",
#         content=""
#     )
#     run = client.beta.threads.runs.create_and_poll(
#         thread_id=thread_id,
#         assistant_id=assistant_id,
#         instructions="You are an assistant that generates a list of ONLY FIVE REAL words separated by commas. The user will provide you with a list of words (could also be a single word). You should generate a list of only five words from the user's list. If no words are provided, you should generate a list of five words from scratch. Words should be hard to pronounce."
#     )
#     if (run.status == "completed"):
#         print("run completed")
#         messages = client.beta.threads.messages.list(thread_id=thread_id)
#         client.beta.threads.delete(thread_id)
#         return messages.data[0].content[0].text.value.replace(" ", "").split(",")

def generate_list():
    # Initialize the OpenAI client with your API key
    client = openai.OpenAI(api_key=os.getenv('OPENAI_SECRET_KEY'))

    # Create a completion
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "Generate a list of ONLY FIVE REAL words separated by commas. Generate a list of five words from scratch. Words should minimum 3 syllables. Do not give any comments or feedback."},
        ]
    )

    # Extract the text from the completion object
    words = response.choices[0].message.content

    print(words)
    # Split the words by commas
    word_list = words.split(',')

    # Return the list of words
    return [word.strip().lower() for word in word_list]
