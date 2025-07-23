"""
CLI for submitting a 'job' consisting of:
  - kernel file
  - data file
  - optional JSON metadata

Writes a structured folder locally, then streams it to S3.
"""
import json
import tempfile
import uuid
import pathlib
import shutil
import click

from .s3_client import upload_job_dir


@click.command()
@click.option("--kernel", "kernel_path", required=True, type=click.Path(exists=True))
@click.option("--data",   "data_path",   required=True, type=click.Path(exists=True))
@click.option("--meta",   "meta_json",   default="{}",  help="JSON string with metadata")
def main(kernel_path: str, data_path: str, meta_json: str) -> None:
    job_id = str(uuid.uuid4())
    tmp    = pathlib.Path(tempfile.mkdtemp())
    try:
        # Copy artefacts
        shutil.copy(kernel_path, tmp / "kernel")
        shutil.copy(data_path,   tmp / "input")

        # Write metadata
        meta = json.loads(meta_json)
        meta.update({"job_id": job_id})
        (tmp / "metadata.json").write_text(json.dumps(meta, indent=2))

        upload_job_dir(tmp, job_id)
        click.echo(f"Job {job_id} uploaded to S3 bucket.")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()