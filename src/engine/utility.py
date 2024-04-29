import requests
import json
from pels.env import config
import json
import os
import re
import secrets
import subprocess
from openai import OpenAI
import openai

from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup as bs
import azure.cognitiveservices.speech as speechsdk
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.core.exceptions import MultipleObjectsReturned
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import Word

############################################[MISC FUNCTIONS]

def make_openAI_request(prompt,model,temperature):
    OPENAI_SECRET_KEY = config("OPENAI_SECRET_KEY",default='none')
    OPENAI_ENDPOINT = config("OPENAI_ENDPOINT",default='none')
    message =[{"role": "user", "content" : prompt}]

    headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_SECRET_KEY}",
        }

    data = {
            "model": model,
            "messages": message,
            "temperature": temperature,
        }

    response = requests.post(OPENAI_ENDPOINT, headers=headers, data=json.dumps(data))

    if response.status_code == 200:      
         return response.json()
    else:
            raise Exception(f"Error {response.status_code}: {response.text}")
    
def webscrapeHowManySyllables(word) -> list[str] | None:
    
    response = requests.get(f'https://www.howmanysyllables.com/syllables/{word}')
    soup = bs(response.text, 'html.parser')
    if "How to pronounce" in soup.text:
        result = soup.find('p', id='SyllableContentContainer').findAll('span')[-1].text.split('-')
    else:
        result = None
    return result

def webscrapeYouGlish(word) -> list[str] | None:

    link = f"https://youglish.com/pronounce/{word}/english?"
    response = requests.get(link)
    soup = bs(response.content, "html.parser")
    try:
        text = soup.findAll('ul', {'class': 'transcript'})[0].findAll('li')[-1].text
        processed = re.findall(r'"(.*?)"', text)
        result = [match.lower() for match in processed]
    except IndexError:
        result = None
    return result

def webscrapeMerriam(word):
    url = f"https://www.merriam-webster.com/dictionary/{word}"
    page = requests.get(url)
    soup = bs(page.content, "html.parser")
    # find class 'a' with class = play-pron-v2 text-decoration-none prons-entry-list-item d-inline badge mw-badge-gray-300
    ipa_pron = soup.find("a", class_="play-pron-v2 text-decoration-none prons-entry-list-item d-inline badge mw-badge-gray-300")
    if ipa_pron:
        text = ipa_pron.text
        syllables = text.replace("\xa0","").split("-")
        # remove all punctuation
        syllables = [s.translate(str.maketrans('', '', '.,ˌˈ()')) for s in syllables]
        return convert_to_laymans_openai(syllables, word)
    else:
        return None
    
def convert_to_laymans_openai(syllables, word):
    client = OpenAI(api_key=os.getenv('OPENAI_SECRET_KEY'))
    # Convert the list of syllables to a string
    list_syllables = ', '.join(syllables)
    # Create a completion
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "system", 
                "content": f"Convert the syllables {list_syllables} to simplified layman's pronunciation for the inflected form or morphological variant of the word {word}. DO not include any punctuation, explanation, discussion, comments, or use any IPA symbols. Provide the syllables separated by commas without any punctuation, explanation, discussion, or comments. Maintain syllable count if possible."},
        ]
    )
    # Extract the text from the completion object
    words = response.choices[0].message.content
    #print(words)
    # Split the words by commas
    word_list = words.split(',')
    # Return the list of words
    return [word.strip().lower() for word in word_list]

def generate_word_feedback(request):

    scores = request.get('scores')
    laymans = request.get('laymans')
    word = request.get('word')

    #print(scores, laymans, word)
    
    OPENAI_SECRET_KEY = os.getenv('OPENAI_SECRET_KEY')
    OPENAI_ENDPOINT = os.getenv('OPENAI_ENDPOINT')
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_SECRET_KEY}",
    }

    print('generate_word_feedback')
    score_and_laymans_joined = []
    feedbacks = []
    #print(scores, laymans, word)
    for i, x in enumerate(laymans):
        score_and_laymans_joined.append({"phrase": x, "score": scores[i].get('score')})
        if scores[i].get('score') <= 90:
            prompt = f"For '{x}' in '{word}', give a concise articulation tip. One sentence only."
            message = [{"role": "user", "content": prompt}]
            data = {
                "model": 'gpt-4-0125-preview',
                "messages": message,
                "temperature": 1,
            }
            response = requests.post(OPENAI_ENDPOINT, headers=headers, data=json.dumps(data))
            if response.status_code == 200:
                suggestion = response.json()["choices"][0]["message"]["content"]
                feedbacks.append({"phrase": x, "suggestion": suggestion})
                # score_and_laymans_joined[i]["articulation_tip"] = articulation_tip
            else:
                raise Exception(f"Error {response.status_code}: {response.text}")
            
    print(score_and_laymans_joined, feedbacks)
    return_data = {
        "laymans": score_and_laymans_joined,
        "feedbacks": feedbacks
    }
    
    return return_data

def generate_sentence_feedback(sentence):
    
    OPENAI_SECRET_KEY = os.getenv('OPENAI_SECRET_KEY')
    OPENAI_ENDPOINT = os.getenv('OPENAI_ENDPOINT')
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_SECRET_KEY}",
    }

    print('generate_word_feedback')
    prompt = f"Give a tip to improve fluency for this sentence: \"{sentence}\" One sentence only."
    message = [{"role": "user", "content": prompt}]
    data = {
        "model": 'gpt-4-0125-preview',
        "messages": message,
        "temperature": 1,
    }
    response = requests.post(OPENAI_ENDPOINT, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        suggestion = response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")
            
    print(suggestion)
    
    return suggestion

############################################[AUDIO PROCESSING FUNCTIONS]

def process_audio_files(request):
    
    mp3_dir = os.path.join('media', 'mp3')
    wav_dir = os.path.join('media', 'wav')
    os.makedirs(mp3_dir, exist_ok=True)
    os.makedirs(wav_dir, exist_ok=True)

    audio_blob = request.FILES['audio']

    # Generate a 5 character random token
    token = secrets.token_hex(3)  # Generates a 6 character long token, as each byte is 2 characters

    # Derive original and new filenames without extension
    base_filename = os.path.splitext(audio_blob.name)[0] + '_' + token

    # Append the token and file extensions to filenames
    original_mp3_name = f'{base_filename}.mp3'
    converted_wav_name = f'{base_filename}.wav'

    # Define paths
    path_original_mp3 = os.path.join(mp3_dir, original_mp3_name)
    path_converted_wav = os.path.join(wav_dir, converted_wav_name)

    # Save the original audio blob in MP3 format
    with default_storage.open(path_original_mp3, 'wb+') as destination:
        destination.write(audio_blob.read())

    # Convert the audio to WAV format using FFmpeg
    command = [
        'ffmpeg',
        '-i', default_storage.path(path_original_mp3),
        '-acodec', 'pcm_s16le',  # Convert to WAV format
        '-ac', '1',  # Mono channel
        '-ar', '16000',  # 16 kHz sample rate
        default_storage.path(path_converted_wav)
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    return path_converted_wav

def create_speechsdk_configuration(request, path_converted_wav, process_type):

    if (process_type == 'word'):
        granularity = speechsdk.PronunciationAssessmentGranularity.Phoneme
    else:
        granularity = speechsdk.PronunciationAssessmentGranularity.Word

    # if (process_type == 'chatbot'):
    #     speech_config = speechsdk.SpeechConfig(subscription=os.getenv('SPEECH_KEY'), region=os.getenv('SPEECH_REGION'))
    #     speech_config.speech_recognition_language="en-US"
    #     return speechsdk.SpeechRecognizer(speech_config=speech_config)

    speech_config = speechsdk.SpeechConfig(subscription=os.getenv('SPEECH_KEY'), region=os.getenv('SPEECH_REGION'))
    speech_config.speech_recognition_language="en-US"

    full_path = os.path.join(path_converted_wav)

    # audio config
    audio_config = speechsdk.audio.AudioConfig(filename = full_path)

    word = request.data.get('word', "")

    # Pronunciation config
    pronunciation_config = speechsdk.PronunciationAssessmentConfig( 
        reference_text=f"{word}",
        grading_system=speechsdk.PronunciationAssessmentGradingSystem.HundredMark,
        granularity=granularity,
        enable_miscue=False)
    
    return_config = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    pronunciation_config.apply_to(return_config)
    return return_config

############################################[SENTENCE PROCESSING FUNCTIONS]

def process_sentence(request):
    print(request.data)
    path_converted_wav = process_audio_files(request)
    speech_recognizer = create_speechsdk_configuration(request, path_converted_wav, 'sentence')
    speech_recognition_result = speech_recognizer.recognize_once_async().get()
    pronunciation_assessment_result_json = speech_recognition_result.properties.get(speechsdk.PropertyId.SpeechServiceResponse_JsonResult)
    result_json = json.loads(pronunciation_assessment_result_json)

    user_message = result_json.get("DisplayText")
    fluency_score = result_json.get("NBest", [])[0].get("PronunciationAssessment", {}).get("FluencyScore")

    if fluency_score < 95:
        fluency_feedback = generate_sentence_feedback(user_message)
        return Response(data={"result_json": result_json, "feedback": fluency_feedback}, status=status.HTTP_200_OK)
    else:
        funny_comments = [
            "You're basically a rockstar without the guitar!",
            "You nailed it better than a carpenter!",
            "Is there an app to download your skills? You did GREAT!",
            "You must have been a Boy Scout because you’ve earned your merit badge with this one!",
            "Wow, you’re on fire! Should I call the fire department?",
            "You’ve hit the bullseye better than Robin Hood!",
            "Are you a wizard? Because that was magical!",
            "If there was a 'Making it Look Easy' award, you’d win hands down!",
            "Did you eat extra smarties today? Because that was brilliant!"
        ]
        # pick random funny comment
        fluency_feedback = secrets.choice(funny_comments)
        return Response(data={"result_json": result_json, "feedback": fluency_feedback}, status=status.HTTP_200_OK)

############################################[WORD PROCESSING FUNCTIONS]

def process_word(request):
    print(request.user)
    path_converted_wav = process_audio_files(request)
    speech_recognizer = create_speechsdk_configuration(request, path_converted_wav, 'word')
    speech_recognition_result = speech_recognizer.recognize_once_async().get()
    pronunciation_assessment_result_json = speech_recognition_result.properties.get(speechsdk.PropertyId.SpeechServiceResponse_JsonResult)
    result_json = json.loads(pronunciation_assessment_result_json)
    scores = []
    for x in result_json.get("NBest", [])[0].get("Words", [])[0].get("Syllables", []):
        syllable = x.get("Syllable")
        score = x.get("PronunciationAssessment", {}).get("AccuracyScore")
        syllable = syllable.replace("x", "")
        scores.append({"phrase": syllable, "score": score})
    try:
        word = Word.objects.get(word=request.data.get('word'))
    except MultipleObjectsReturned:
        words = Word.objects.filter(word=request.data.get('word'))
        word = words.first()
        words.exclude(pk=word.pk).delete()
    laymans = word.laymans
    feedback_request = {
        "scores": scores,
        "laymans": laymans,
        "word": word
    }
    feedback = generate_word_feedback(feedback_request)

    return Response(data=feedback, status=status.HTTP_200_OK)

############################################[ASSESSMENT PROCESSING FUNCTIONS]

def process_assessment(request):
    print(request.data)
    return Response(data={"message": "not implemented yet lel"}, status=status.HTTP_200_OK)

############################################[CHATBOT PROCESSING FUNCTIONS]

def init_chatbot(client: OpenAI):

    print("initializing chatbot thread")

    thread = client.beta.threads.create()

    thread_id = thread.id
    #assistant_id = os.getenv('OPENAI_ASSISTANT_ID_CHATBOT')
    
    # Automatically generate the first chatbot message
    initial_message = "Hello! How can I help you?"
    # Create the message in the thread with the specified role
    client.beta.threads.messages.create(
            thread_id=thread_id,
            role="assistant",  # This now depends on the sender_role argument
            content=initial_message
        )
    
    return thread_id

def generate_message_feedback(content):

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

def add_message(message_content, sender_role, client: OpenAI, thread_id):

    print("adding message: ", message_content)

    try:
        # Create the message in the thread with the specified role
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role=sender_role,
            content=message_content
        )

        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread_id,
            assistant_id=os.getenv('OPENAI_ASSISTANT_ID_CHATBOT'),
            instructions="Continue to help the user. All responses should be no more than 50 words."
            )
        
        if (run.status == "completed"):
            print("run completed")
            messages = client.beta.threads.messages.list(
                thread_id=thread_id
            )
            return messages.data[0].content[0].text.value

    except Exception as e:
        # Handle errors (e.g., API failure, network issues)
        print(f"An error occurred: {str(e)}")
        return "An error occurred while adding the message."

def process_chatbot(request):
    #print(request.data)
    path_converted_wav = process_audio_files(request)
    speech_recognizer = create_speechsdk_configuration(request, path_converted_wav, 'chatbot')
    speech_recognition_result = speech_recognizer.recognize_once_async().get()
    pronunciation_assessment_result_json = speech_recognition_result.properties.get(speechsdk.PropertyId.SpeechServiceResponse_JsonResult)
    result_json = json.loads(pronunciation_assessment_result_json)

    user_message = result_json.get("DisplayText")
    fluency_score = result_json.get("NBest", [])[0].get("PronunciationAssessment", {}).get("FluencyScore")

    fluency_feedback = None
    if fluency_score < 95:
        print("generating feedback...")
        fluency_feedback = generate_message_feedback(user_message)

    client = OpenAI(api_key=os.getenv('OPENAI_SECRET_KEY'))

    thread_id = request.data.get('thread_id', None)
    if thread_id == 'undefined' or thread_id == '' or thread_id == 'null':
        print("thread_id not found. creating new thread...")
        thread_id = init_chatbot(client)
        # request.session['thread_id'] = thread_id
        # request.session.modified = True
        # request.session.save()

    #print("sessionid: ", request.session.session_key)
    print("thread_id: ", thread_id)

    chatbot_response = add_message(user_message, "user", client, thread_id)

    print("user message: ", user_message)
    print("fluency score: ", fluency_score)

    return Response(data={
        "user_message": user_message,
        "chatbot_response": chatbot_response,
        "feedback": fluency_feedback,
        "result_json": result_json,
        "thread_id": thread_id
        }, status=status.HTTP_200_OK)
