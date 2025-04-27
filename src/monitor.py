import os
import logging
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from anomaly_features import get_message_length, extract_ip, IPCache
from config_loader import load_config
from log_reader import parse_log_line
from ai_model import LogAnomalyDetector
from db_writer import AnomalyDatabase
from utils import get_log_level
from feature_pipeline import extract_features, fit_vectorizer


from datetime import datetime


# Config ve Path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(BASE_DIR, "config", "settings.yaml")
config = load_config(config_path)

db_path = os.path.abspath(os.path.join(BASE_DIR, config["database"]["path"]))
log_file_path = os.path.abspath(os.path.join(BASE_DIR, config["log_file_path"]))

# Logger Ayarı
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

ANOMALY_LOG_PATH = os.path.join(LOG_DIR, "anomalies.log")

logger = logging.getLogger("monitor_logger")
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")

file_handler = logging.FileHandler(ANOMALY_LOG_PATH)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Log File Event Handler
class LogFileHandler(FileSystemEventHandler):
    def __init__(self, model, db, logger):
        self.model = model
        self.db = db
        self.logger = logger
        self.position = 0
        self.ip_cache = IPCache()

    def on_modified(self, event):
        if os.path.abspath(event.src_path) != log_file_path:
            return

        with open(log_file_path, "r") as f:
            f.seek(self.position)
            new_lines = f.readlines()
            self.position = f.tell()

        for line in new_lines:
            timestamp, level, message = parse_log_line(line)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if not all([timestamp, level, message]):
                continue

            ip = extract_ip(message)
            ip_count = self.ip_cache.update_and_get_count(ip)

            features = extract_features([message])
            msg_length = int(features["length"][0][0])
            msg_entropy = float(features["entropy"][0][0])

            print(f"[FEATURES] len={msg_length}, entropy={msg_entropy:.2f}, ip={ip}, ip_count={ip_count}")

            preds, scores = self.model.predict([message])
            if preds[0] == -1:
                score = float(scores[0])
                severity = get_log_level(score)

                log_message = f"Anomaly Detected | IP: {ip} | Score: {score:.2f} | Msg Len: {msg_length} | Count: {ip_count} | Message: {message}"
                self.logger.log(getattr(logging, severity), log_message)

                self.db.insert_anomaly(timestamp, level, message, score)


print("[DEBUG] Watching file:", log_file_path)
print(f"[DEBUG] Using database file at: {db_path}")

# Monitoring starter
def start_monitoring():
    if not os.path.exists(log_file_path):
        raise FileNotFoundError(f"Log file not found at {log_file_path}")


    print("[DEBUG] Connecting to database...")
    db = AnomalyDatabase(db_path)

    print("[DEBUG] Connected to database.")

    model = LogAnomalyDetector(
        contamination=config["model"]["contamination"],
        random_state=config["model"]["random_state"]
    )

    # first 500 log
    with open(log_file_path, "r") as f:
        training_messages = [parse_log_line(line)[2] for _, line in zip(range(500), f)]
    fit_vectorizer(training_messages)
    model.fit(training_messages)



    # Observer start
    event_handler = LogFileHandler(model, db, logger)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(log_file_path), recursive=False)


    observer.start()


    logger.info("Monitoring started... Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    db.close()

if __name__ == "__main__":
    start_monitoring()
