from mealslip.worker import run_worker
from mealslip.config import settings
import logging
import os

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(settings.LOG_FILE), logging.StreamHandler()]
)

if __name__ == "__main__":
    run_worker()