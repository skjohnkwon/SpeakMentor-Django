from django.conf import settings
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

def schedule_clean_audio_files():
    print("[APSCHEDULER] CLEANING MEDIA FILES")
    media_dir = "media"
    media_dir = os.path.join(settings.BASE_DIR, media_dir)

    for dir in os.listdir(media_dir):
        dir_path = os.path.join(media_dir, dir)
        if os.path.isdir(dir_path):
            for file in os.listdir(dir_path):
                file_path = os.path.join(dir_path, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            os.rmdir(dir_path)

def schedule_clean_threads():
    print("[APSCHEDULER] CLEANING THREADS")
    assistantId = os.getenv('OPENAI_ASSISTANT_ID_CHATBOT')
    client = OpenAI(api_key=os.getenv('OPENAI_SECRET_KEY'))
    response = client.beta.threads.list(assistant_id=assistantId)
    while response.has_more:
        for thread in response.data:
            client.beta.threads.delete(assistant_id=assistantId, id=thread.id)
            print(f"[APSCHEDULER] Deleted thread {thread.id}")
        response = client.beta.threads.list(assistant_id=assistantId)