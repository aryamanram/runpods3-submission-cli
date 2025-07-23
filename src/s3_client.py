"""
Wrapper around boto3 for bucket creation + uploads.
"""

import pathlib
import boto3
from botocore.exceptions import ClientError
from .config import AWS_REGION, S3_BUCKET, S3_ENDPOINT_URL


_session = boto3.session.Session(region_name=AWS_REGION)
_s3      = _session.resource("s3", endpoint_url=S3_ENDPOINT_URL)


def _ensure_bucket() -> None:
    try:
        _s3.meta.client.head_bucket(Bucket=S3_BUCKET)
    except ClientError:
        _s3.create_bucket(
            Bucket=S3_BUCKET,
            CreateBucketConfiguration={"LocationConstraint": AWS_REGION},
        )


def upload_job_dir(local_dir: pathlib.Path, job_id: str) -> None:
    """
    Recursively upload every file in *local_dir* to
    s3://S3_BUCKET/{job_id}/...
    """
    _ensure_bucket()
    bucket = _s3.Bucket(S3_BUCKET)

    for path in local_dir.rglob("*"):
        if path.is_file():
            key = f"{job_id}/{path.relative_to(local_dir)}"
            bucket.upload_file(Filename=str(path), Key=key)