from waitress import serve
from receiver.app import app
from mealslip.config import settings
import logging

def run_receiver():
    logging.getLogger().setLevel(settings.LOG_LEVEL)
    print(f"[HikEventReceiver] Starting on http://0.0.0.0:5000/hik-event")
    serve(app, host='0.0.0.0', port=5000, threads=10)