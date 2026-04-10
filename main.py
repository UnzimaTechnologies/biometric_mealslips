import logging
import logging.config
import os
from mealslip.config import settings
from mealslip.worker import run_worker

# Logging setup
log_dir = os.path.dirname(settings.LOG_FILE)
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(settings.LOG_FILE),
        logging.StreamHandler()
    ]
)

if __name__ == "__main__":
    run_worker()