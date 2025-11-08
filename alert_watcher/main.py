import os
import time
import requests
from dotenv import load_dotenv
from collections import deque

load_dotenv()

LOG_FILE ="/var/log/nginx/access.log"
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
ERROR_RATE_THRESHOLD = float(os.getenv("ERROR_RATE_THRESHOLD", 2))
WINDOW_SIZE = int(os.getenv("WINDOW_SIZE", 200))
ALERT_COOLDOWN_SEC = int(os.getenv("ALERT_COOLDOWN_SEC", 300))

recent_statuses = deque(maxlen=WINDOW_SIZE)
last_pool = None
last_alert_time = 0


def post_to_slack(message):
    payload = {"text": message}
    try:
        requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=5)
    except Exception as e:
        print(f"Slack post failed: {e}")


def calculate_error_rate():
    if not recent_statuses:
        return 0
    errors = sum(1 for s in recent_statuses if s.startswith("5"))
    return (errors / len(recent_statuses)) * 100


def parse_log_line(line):
    parts = line.split()
    pool = None
    status = None
    for part in parts:
        if part.startswith("pool="):
            pool = part.split("=")[1]
        elif part.startswith("status="):
            status = part.split("=")[1]
    return pool, status


def tail_log(file_path):
    with open(file_path, "r") as f:
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue
            yield line


def main():
    global last_pool, last_alert_time
    print("Watcher started...")

    for line in tail_log(LOG_FILE):
        pool, status = parse_log_line(line)
        if not pool or not status:
            continue

        recent_statuses.append(status)

        # Failover detection
        if last_pool and pool != last_pool:
            now = time.time()
            if now - last_alert_time > ALERT_COOLDOWN_SEC:
                post_to_slack(f"⚠️ Failover detected: {last_pool} → {pool}")
                last_alert_time = now
        last_pool = pool

        # Error rate detection
        error_rate = calculate_error_rate()
        if error_rate > ERROR_RATE_THRESHOLD:
            now = time.time()
            if now - last_alert_time > ALERT_COOLDOWN_SEC:
                post_to_slack(f"❗ High error rate: {error_rate:.2f}% over last {len(recent_statuses)} requests")
                last_alert_time = now


if __name__ == "__main__":
    main()

