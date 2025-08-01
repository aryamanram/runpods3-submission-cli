from __future__ import annotations

import os
import uuid
from pathlib import Path

import boto3
from botocore.client import Config as _BotoConfig

from .base import Writer


class S3Writer(Writer):
    """
    Uploads the entire job directory to an S3-compatible endpoint
    (RunPod’s is 100 % AWS-S3-API compliant).
    """

    def __init__(
        self,
        bucket: str,
        endpoint_url: str | None = None,
        region_name: str | None = None,
        multipart_threshold_mb: int = 128,
    ):
        session = boto3.session.Session()
        # Slightly higher multipart threshold keeps small jobs simple:
        transfer_cfg = _BotoConfig(
            s3={"addressing_style": "virtual"},
            retries={"max_attempts": 10, "mode": "standard"},
        )
        self._s3 = session.resource(
            "s3",
            endpoint_url=endpoint_url,
            region_name=region_name,
            config=transfer_cfg,
        )
        self._bucket = self._s3.Bucket(bucket)
        self._multipart_threshold = multipart_threshold_mb * 1024 * 1024

    # --------------------------------------------------------------------- #
    def write(self, local_path: str | Path, key_prefix: str | None = None) -> str:
        local_path = Path(local_path).resolve()
        job_id = key_prefix or uuid.uuid4().hex

        for file_path in local_path.rglob("*"):
            if file_path.is_file():
                rel_key = f"{job_id}/{file_path.relative_to(local_path).as_posix()}"
                extra_args = {}
                if file_path.stat().st_size > self._multipart_threshold:
                    # enable multipart for larger files
                    extra_args["Config"] = boto3.s3.transfer.TransferConfig(
                        multipart_threshold=self._multipart_threshold
                    )
                self._bucket.upload_file(
                    Filename=str(file_path),
                    Key=rel_key,
                    ExtraArgs=extra_args or None,
                )

        return f"s3://{self._bucket.name}/{job_id}"
