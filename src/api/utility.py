import openai
import os
from rest_framework.response import Response
from wonderwords import RandomWord

def generate_list():
    # # Initialize the OpenAI client with your API key
    # client = openai.OpenAI(api_key=os.getenv('OPENAI_SECRET_KEY'))

    # # Create a completion
    # response = client.chat.completions.create(
    #     model="gpt-4-turbo",
    #     messages=[
    #         {"role": "system", "content": "Generate a list of ONLY FIVE REAL words separated by commas. Generate a list of five words from scratch. Words should minimum 3 syllables. Do not give any comments or feedback."},
    #     ]
    # )

    # print(response)

    # # Extract the text from the completion object
    # words = response.choices[0].message.content

    # print(words)
    # # Split the words by commas
    # word_list = words.replace(".", "").split(',')

    # # Return the list of words
    # return [word.strip().lower() for word in word_list]
    rw = RandomWord()
    list = rw.random_words(5, word_min_length=10, word_max_length=15, include_parts_of_speech=["noun", "adjective"])
    #for each in list replace all hyphens with nothing
    list = [each.replace("-","") for each in list]
    return list
