from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import schedule_clean

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(schedule_clean, 'interval', hours=6)
    scheduler.start()
    print("[APSCHEDULER] BCS Started")