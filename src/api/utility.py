import openai
import os
from rest_framework.response import Response

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
