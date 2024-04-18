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

def schedule_clean_assistants():
    print("[APSCHEDULER] CLEANING ASSISTANTS")
    client = OpenAI(api_key=os.getenv('OPENAI_SECRET_KEY'))
    assistants = client.best.assistants.list()
    for assistant in assistants:
        print(f"[APSCHEDULER] Deleting assistant {assistant['id']}")
        response = client.beta.assistants.delete(assistant['id'])
        print("[APSCHEDULER] ",  response)