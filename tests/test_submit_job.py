from moto import mock_s3
import boto3
import pathlib
import subprocess
import json
import os

THIS_DIR = pathlib.Path(__file__).parent
ROOT     = THIS_DIR.parent
SRC      = ROOT / "src"

@mock_s3
def test_cli_upload(tmp_path, monkeypatch):
    # Arrange – isolate fake S3
    monkeypatch.setenv("AWS_REGION", "us-east-1")
    monkeypatch.setenv("S3_ENDPOINT_URL", "")  # moto intercepts
    monkeypatch.setenv("JOB_BUCKET", "job-artifacts")

    # Fake artefacts
    kernel = tmp_path / "k.cu"
    data   = tmp_path / "d.npy"
    kernel.write_text("__global__ void foo(){}")
    data.write_text("123")

    # Act – run CLI
    subprocess.check_call(
        [
            "python",
            "-m",
            "src.submit_job",
            "--kernel",
            str(kernel),
            "--data",
            str(data),
        ],
        cwd=ROOT,
    )

    # Assert – object exists in mock S3
    s3 = boto3.client("s3", region_name="us-east-1")
    objs = s3.list_objects_v2(Bucket="job-artifacts")["Contents"]
    keys = [o["Key"] for o in objs]
    assert any(k.endswith("kernel") for k in keys)
    assert any(k.endswith("input") for k in keys)
    assert any(k.endswith("metadata.json") for k in keys)