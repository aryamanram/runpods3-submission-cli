import os
import uuid
from datetime import datetime

JOBS_DIR = os.path.join(os.path.dirname(__file__), '..', 'jobs')
os.makedirs(JOBS_DIR, exist_ok=True)

def write_job(kernel_path: str, data_path: str) -> str:
    with open(kernel_path, 'r') as kf:
        kernel_code = kf.read()
    with open(data_path, 'r') as df:
        data_content = df.read()

    job_id = str(uuid.uuid4())
    job_file_path = os.path.join(JOBS_DIR, f"{job_id}.job")

    with open(job_file_path, 'w') as jf:
        jf.write(f"# Job ID: {job_id}\n")
        jf.write(f"# Timestamp: {datetime.now()}\n\n")
        jf.write("=== Kernel ===\n")
        jf.write(kernel_code + "\n\n")
        jf.write("=== Data ===\n")
        jf.write(data_content + "\n")

    return job_file_path
