from __future__ import annotations
from abc import ABC, abstractmethod
from pathlib import Path


class Writer(ABC):
    """Common interface for any storage backend."""

    @abstractmethod
    def write(self, local_path: str | Path, key_prefix: str | None = None) -> str:
        """
        Copy -or- upload the job directory.

        Parameters
        ----------
        local_path : str | Path
            Folder that contains *kernel/* and *data/*.
        key_prefix : str | None
            Job-ID to prepend on the destination.  If None a UUID is generated.

        Returns
        -------
        str
            Fully-qualified destination URI
            (e.g., 'jobs/3f7a…' or 's3://bucket/3f7a…').
        """
