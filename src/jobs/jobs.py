from django.conf import settings
import os

def schedule_clean():
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