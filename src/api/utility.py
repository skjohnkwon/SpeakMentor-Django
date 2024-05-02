import openai
import os
from rest_framework.response import Response
from wonderwords import RandomWord

def generate_list():
    rw = RandomWord()
    list = rw.random_words(5, word_min_length=10, word_max_length=15, include_parts_of_speech=["noun", "adjective"], regex='^\w+[^s]$')
    list = [each.replace("-","") for each in list]
    # regex search for "sation" and replace with "zation"
    list = [each.replace("sation", "zation") for each in list]
    return list
