import subprocess
import threading
import time
from dotenv import load_dotenv
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

load_dotenv()

logger = get_logger(__name__)

def run_backend():
    try:
        logger.info("Starting Backend")
        subprocess.run(["uvicorn", "app.backend.api:app", "--host", "0.0.0.0", "--port", "9999"], check=True)
    except Exception as e:
        logger.error(f"Failed to start backend. Error: {e}")
        raise CustomException("Failed to start backend")

def run_frontend():
    try:
        logger.info("Starting Frontend")
        subprocess.run(["streamlit", "run", "app/frontend/ui.py"], check=True)
    except Exception as e:
        logger.error(f"Failed to start frontend. Error: {e}")
        raise CustomException("Failed to start frontend")
    
if __name__=="__main__":
    try:
        logger.info("Starting Application")
        threading.Thread(target=run_backend).start()
        time.sleep(3)
        run_frontend()
    except Exception as e:
        logger.error(f"Failed to start application. Error: {e}")
        raise CustomException("Failed to start application")
