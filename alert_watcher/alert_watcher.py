import os
import time
import requests

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
ERROR_THRESHOLD = float(os.getenv("ERROR_RATE_THRESHOLD", 2))
WINDOW_SIZE = int(os.getenv("WINDOW_SIZE", 200))
COOLDOWN = int(os.getenv("ALERT_COOLDOWN_SEC", 300))

last_pool = None
request_window = []
last_alert_time = {"failover": 0, "error_rate": 0}


def send_slack_alert(message):
    requests.post(SLACK_WEBHOOK_URL, json={"text": message})

def parse_log_line(line):
    parts = {}
    for item in line.split():
        if '=' in item:
            key, value = item.split('=', 1)
            parts[key] = value
    return parts


def check_failover(current_pool):
    global last_pool, last_alert_time

    if last_pool and last_pool != current_pool:
        if time.time() - last_alert_time["failover"] > COOLDOWN:
            send_slack_alert(f"Failover detected: {last_pool} → {current_pool}")
            last_alert_time["failover"] = time.time()

    last_pool = current_pool


def check_error_rate():
    global request_window, last_alert_time

    if len(request_window) >= WINDOW_SIZE:
        errors = sum(1 for status in request_window if status >= 500)
        error_rate = (errors / len(request_window)) * 100

        if error_rate > ERROR_THRESHOLD:
            if time.time() - last_alert_time["error_rate"] > COOLDOWN:
                send_slack_alert(f"High error rate: {error_rate:.1f}% (threshold: {ERROR_THRESHOLD}%)")
                last_alert_time["error_rate"] = time.time()


def tail_logs():
    with open('var/log/nginx/access.log', 'r') as f:
        f.seek(0, 2)

        while True:
            line = f.readline()

            if line:
                data = parse_log_line(line)
                pool = data.get('pool')
                status = int(data.get('status', 0))

                if pool:
                    check_failover(pool)

                request_window.append(status)
                if len(request_window) > WINDOW_SIZE:
                    request_window.pop(0)

                check_error_rate()
            else:
                time.sleep(0.1)


tail_logs()

