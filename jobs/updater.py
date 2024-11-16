from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import schedule_api_call_fill, schedule_api_call_weight

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(schedule_api_call_fill, 'interval', minutes=1)
    scheduler.add_job(schedule_api_call_weight, 'interval', minutes=1)
    scheduler.start()