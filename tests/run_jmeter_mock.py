import argparse
import threading
import time
import csv
import requests

CSV_HEADERS = [
    "timeStamp", "elapsed", "label", "responseCode", "responseMessage",
    "threadName", "dataType", "success", "failureMessage", "bytes",
    "sentBytes", "grpThreads", "allThreads", "URL", "Latency", "IdleTime", "Connect"
]

parser = argparse.ArgumentParser(description="FHIR load test simulator (JMeter-compatible CSV)")
parser.add_argument("--threads", type=int, default=500, help="Number of concurrent threads")
args = parser.parse_args()

concurrent_threads = args.threads
ramp_up = 30   # seconds
duration = 45  # seconds of sustained load

results = []
results_lock = threading.Lock()
active_threads = 0
active_threads_lock = threading.Lock()

def record_result(timestamp, elapsed, label, code, msg, t_name, success, r_bytes, latency, connect):
    with results_lock:
        results.append([
            timestamp, elapsed, label, code, msg, t_name, "text", str(success).lower(),
            "", r_bytes, 0, active_threads, active_threads,
            f"http://localhost:8000{label}", latency, 0, connect
        ])

def worker(thread_id):
    global active_threads
    with active_threads_lock:
        active_threads += 1

    session = requests.Session()
    thread_name = f"Clinician Users 1-{thread_id}"
    start_time_all = time.time()

    while time.time() - start_time_all < duration:
        t0 = time.time()
        try:
            auth_res = session.post(
                "http://localhost:8000/auth/token",
                data={"username": "clinician", "password": "supersecure"}
            )
            t1 = time.time()
            elapsed_auth = int((t1 - t0) * 1000)
            record_result(
                int(t0 * 1000), elapsed_auth, "/auth/token",
                auth_res.status_code, auth_res.reason, thread_name,
                auth_res.status_code == 200, len(auth_res.content),
                elapsed_auth, 0
            )

            token = auth_res.json().get("access_token")
            if token:
                headers = {"Authorization": f"Bearer {token}"}
                t2 = time.time()
                obs_res = session.get("http://localhost:8000/fhir/Observation", headers=headers)
                t3 = time.time()
                elapsed_obs = int((t3 - t2) * 1000)
                record_result(
                    int(t2 * 1000), elapsed_obs, "/fhir/Observation",
                    obs_res.status_code, obs_res.reason, thread_name,
                    obs_res.status_code == 200, len(obs_res.content),
                    elapsed_obs, 0
                )
        except Exception:
            pass

    with active_threads_lock:
        active_threads -= 1


threads = []
for i in range(concurrent_threads):
    time.sleep(ramp_up / concurrent_threads)
    t = threading.Thread(target=worker, args=(i + 1,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

output_file = f"results_{concurrent_threads}threads.csv"
with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(CSV_HEADERS)
    writer.writerows(results)

print(f"Load test complete: {len(results)} samples -> {output_file}")
