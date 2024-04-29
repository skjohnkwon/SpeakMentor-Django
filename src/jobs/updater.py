from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import schedule_clean_audio_files

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(schedule_clean_audio_files, 'interval', hours=24)
    scheduler.start()
    print("[APSCHEDULER] BCS Started")