import os
import uuid
import shutil
from datetime import datetime

JOBS_DIR = os.path.join(os.path.dirname(__file__), '..', 'jobs')
os.makedirs(JOBS_DIR, exist_ok=True)

def write_job(kernel_path: str, data_path: str) -> str:
    
    # Generate a unique ID for the job
    job_id = str(uuid.uuid4())
    
    # Create a subdirectory for this job
    job_dir = os.path.join(JOBS_DIR, job_id)
    os.makedirs(job_dir, exist_ok=True)

    # Move kernel and data into the job folder
    kernel_dest = os.path.join(job_dir, os.path.basename(kernel_path))
    data_dest = os.path.join(job_dir, os.path.basename(data_path))
    shutil.move(kernel_path, kernel_dest)
    shutil.move(data_path, data_dest)

    # Create a metadata file with job details
    metadata_file = os.path.join(job_dir, "metadata.txt")
    with open(metadata_file, 'w') as mf:
        mf.write(f"Job ID: {job_id}\n")
        mf.write(f"Timestamp: {datetime.now()}\n")
        mf.write(f"Kernel File: {os.path.basename(kernel_dest)}\n")
        mf.write(f"Data File: {os.path.basename(data_dest)}\n")

    return job_dir