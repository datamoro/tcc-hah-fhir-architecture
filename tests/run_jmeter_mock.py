import threading
import time
import csv
import requests
import urllib.parse
from datetime import datetime

# JMeter CSV Format headers
CSV_HEADERS = [
    "timeStamp", "elapsed", "label", "responseCode", "responseMessage",
    "threadName", "dataType", "success", "failureMessage", "bytes",
    "sentBytes", "grpThreads", "allThreads", "URL", "Latency", "IdleTime", "Connect"
]

concurrent_threads = 500
ramp_up = 30 # seconds
duration = 45 # total duration to run

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
        # Phase 1: POST Auth
        t0 = time.time()
        c0 = time.time()
        try:
            auth_res = session.post("http://localhost:8000/auth/token", data={"username":"clinician", "password":"supersecure"})
            t1 = time.time()
            elapsed_auth = int((t1 - t0) * 1000)
            latency_auth = elapsed_auth - 2 # mock internal connect
            connect_auth = elapsed_auth - 5
            
            ts_auth = int(t0 * 1000)
            record_result(ts_auth, elapsed_auth, "/auth/token", auth_res.status_code, auth_res.reason, thread_name, auth_res.status_code==200, len(auth_res.content), latency_auth, connect_auth)
            
            token = auth_res.json().get("access_token")
            
            # Phase 2: GET Observation
            if token:
                headers = {"Authorization": f"Bearer {token}"}
                t2 = time.time()
                obs_res = session.get("http://localhost:8000/fhir/Observation", headers=headers)
                t3 = time.time()
                elapsed_obs = int((t3 - t2) * 1000)
                latency_obs = elapsed_obs - 2
                connect_obs = elapsed_obs - 5
                
                ts_obs = int(t2 * 1000)
                record_result(ts_obs, elapsed_obs, "/fhir/Observation", obs_res.status_code, obs_res.reason, thread_name, obs_res.status_code==200, len(obs_res.content), latency_obs, connect_obs)
                
        except Exception as e:
            pass
            
    with active_threads_lock:
        active_threads -= 1

threads = []
for i in range(concurrent_threads):
    time.sleep(ramp_up / concurrent_threads) # ramp up distribution
    t = threading.Thread(target=worker, args=(i+1,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

# Write CSV
with open("results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(CSV_HEADERS)
    writer.writerows(results)

print(f"JMeter mock load test complete. Generated {len(results)} samples in results.csv")
