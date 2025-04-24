import os
import logging
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


from anomaly_features import get_message_length, get_log_level, extract_ip, IPCache
from config_loader import load_config
from log_reader import parse_log_line
from ai_model import LogAnomalyDetector
from db_writer import AnomalyDatabase
from utils import get_log_level  # Returns: INFO, WARNING, ERROR, CRITICAL

from feature_pipeline import extract_features, fit_vectorizer

from db_writer import export_anomalies_to_csv



#  Config & Paths
config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../config/settings.yaml"))
config = load_config(config_path)
#log_file_path = os.path.abspath(config["log_file_path"])
db_path = os.path.abspath(config["database"]["path"])

# Logger Setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "anomalies.log")
log_format = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
log_file_path = os.path.abspath(os.path.join(BASE_DIR, config["log_file_path"]))

file_handler = logging.FileHandler(LOG_FILE)
file_handler.setFormatter(log_format)
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_format)
console_handler.setLevel(logging.INFO)

logger = logging.getLogger("monitor_logger")
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

#print("Looking for log at:", config["log_file_path"])
#print("Absolute path:", log_file_path)

#  File Event Handler
class LogFileHandler(FileSystemEventHandler):
    def __init__(self, log_path, model, db, logger):
        self.log_path = log_path
        self.model = model
        self.db = db
        self.logger = logger
        self.position = 0
        self.ip_cache = IPCache()

    def on_modified(self, event):
        if os.path.abspath(event.src_path) != self.log_path:
            return

        with open(self.log_path, "r") as f:
            f.seek(self.position)
            new_lines = f.readlines()
            self.position = f.tell()

        for line in new_lines:
            timestamp, level, message = parse_log_line(line)
            if message and level and timestamp:

                ip = extract_ip(message)
                ip_count = self.ip_cache.update_and_get_count(ip)

                # === FEATURE PIPELINE ===
                features = extract_features([message])
                msg_length = int(features["length"][0][0])
                msg_entropy = float(features["entropy"][0][0])

                # === DEBUG PRINT ===
                print(f"[FEATURES] len={msg_length}, entropy={msg_entropy:.2f}, ip={ip}, ip_count={ip_count}")

                # === ANOMALY DETECTION ===
                preds, scores = self.model.predict([message])
                if preds[0] == -1:
                    score = float(scores[0])
                    severity = get_log_level(score)
                    log_msg = f"Anomaly Detected | IP: {ip} | Score: {score:.2f} | Msg Len: {msg_length} | Count: {ip_count} | Message: {message}"
                    self.logger.log(getattr(logging, severity), log_msg)
                    self.db.insert_anomaly(timestamp, level, message, score)


#  Monitor Starter =
def start_monitoring():
    if not os.path.exists(log_file_path):
        raise FileNotFoundError(f"Log file not found at: {log_file_path}")

    db = AnomalyDatabase(db_path)
    model = LogAnomalyDetector(
        contamination=config["model"]["contamination"],
        random_state=config["model"]["random_state"]
    )

    with open(log_file_path, "r") as f:
        training_messages = [parse_log_line(line)[2] for _, line in zip(range(500), f)]
    fit_vectorizer(training_messages)

    with open(log_file_path, "r") as f:
        training_data = [parse_log_line(line)[2] for _, line in zip(range(500), f)]
    model.fit(training_data)

    event_handler = LogFileHandler(log_file_path, model, db, logger)
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

# Export latest anomalies (can be moved to a button or CLI later)
csv_output = os.path.join(BASE_DIR, "anomaly_export.csv")
export_anomalies_to_csv(db_path, csv_output)
print(f"[EXPORT] Anomalies exported to: {csv_output}")
