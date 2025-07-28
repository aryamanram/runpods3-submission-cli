import argparse
from core.writer import write_job

def run():
    parser = argparse.ArgumentParser(description="Job Submission CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Define submit-job command
    submit_parser = subparsers.add_parser("submit-job", help="Submit a new job")
    submit_parser.add_argument("--kernel", required=True, help="Path to the kernel file")
    submit_parser.add_argument("--data", required=True, help="Path to the data file")

    # Parse CLI args
    args = parser.parse_args()

    if args.command == "submit-job":
        submit_job(args)

def submit_job(args):
    job_dir = write_job(args.kernel, args.data)
    print(f"Job submitted! Files saved in: {job_dir}")
