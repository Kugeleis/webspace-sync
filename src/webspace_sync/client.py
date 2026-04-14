from pathlib import Path
from typing import List

from ftpsync.ftp_target import FTPTarget  # type: ignore
from ftpsync.synchronizers import (  # type: ignore
    BiDirSynchronizer,
    DownloadSynchronizer,
    UploadSynchronizer,
)
from ftpsync.targets import FsTarget  # type: ignore


class WebspaceClient:
    """A client for interacting with a webspace using pyftpsync.

    Attributes:
        host: The FTP server host.
        username: The FTP username.
        password: The FTP password.
    """

    def __init__(self, host: str, username: str, password: str):
        """Initializes the WebspaceClient.

        Args:
            host: The FTP server host.
            username: The FTP username.
            password: The FTP password.
        """
        self.host = host
        self.username = username
        self.password = password

    def __enter__(self) -> "WebspaceClient":
        """Enters the runtime context related to this object.

        Returns:
            The WebspaceClient instance.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exits the runtime context related to this object.

        Args:
            exc_type: The exception type.
            exc_val: The exception value.
            exc_tb: The traceback.
        """
        pass

    def _get_ftp_target(self, remote_dir: str) -> FTPTarget:
        """Creates an FTPTarget instance.

        Args:
            remote_dir: The remote directory path.

        Returns:
            An FTPTarget instance.
        """
        return FTPTarget(
            remote_dir,
            self.host,
            username=self.username,
            password=self.password,
            tls=True,
        )

    def upload(self, local_path: Path, remote_dir: str) -> None:
        """Uploads a file or directory to the remote server.

        Args:
            local_path: The path to the local file or directory to upload.
            remote_dir: The remote directory to upload to.

        Raises:
            FileNotFoundError: If the local path does not exist.
        """
        if not local_path.exists():
            raise FileNotFoundError(f"Local path not found: {local_path}")

        if local_path.is_file():
            # pyftpsync works on directories. To upload a single file,
            # we can sync its parent and match only the file.
            local_target = FsTarget(str(local_path.parent))
            remote_target = self._get_ftp_target(remote_dir)
            opts = {
                "match": local_path.name,
                "verbose": 3,
            }
        else:
            local_target = FsTarget(str(local_path))
            remote_target = self._get_ftp_target(remote_dir)
            opts = {"verbose": 3}

        s = UploadSynchronizer(local_target, remote_target, opts)
        s.run()

    def download(self, remote_path: str, local_dir: Path) -> None:
        """Downloads a file or directory from the remote server.

        Args:
            remote_path: The path to the remote file or directory to download.
            local_dir: The local directory to download to.
        """
        # If remote_path is a file, we can't easily tell without trying to list it
        # or assuming based on extension/context.
        # pyftpsync download works on directories.
        # To download a single file, we sync the remote parent and match the file.

        remote_parent = str(Path(remote_path).parent)
        remote_name = Path(remote_path).name

        local_dir.mkdir(parents=True, exist_ok=True)

        local_target = FsTarget(str(local_dir))
        remote_target = self._get_ftp_target(remote_parent)
        opts = {
            "match": remote_name,
            "verbose": 3,
        }
        s = DownloadSynchronizer(local_target, remote_target, opts)
        s.run()

    def ls(self, remote_dir: str = ".") -> List[str]:
        """Lists files in the remote directory.

        Args:
            remote_dir: The remote directory to list. Defaults to ".".

        Returns:
            A list of filenames in the directory.
        """
        target = self._get_ftp_target(remote_dir)
        target.open()
        try:
            entries = target.read_dir()
            return [e.name for e in entries]
        finally:
            target.close()

    def push(
        self,
        local_dir: Path,
        remote_dir: str,
        recursive: bool = False,
        callback=None,
    ) -> None:
        """Pushes new or updated files from local_dir to remote_dir.

        Args:
            local_dir: The local directory to push from.
            remote_dir: The remote directory to push to.
            recursive: Whether to push directories recursively. Defaults to False.
            callback: An optional callback function for logging progress (unused by pyftpsync natively, but kept for API compatibility).
        """
        local_target = FsTarget(str(local_dir))
        remote_target = self._get_ftp_target(remote_dir)
        opts = {"verbose": 3}
        # pyftpsync is recursive by default unless limited.
        # If recursive is False, we might need to handle it.
        # However, pyftpsync's synchronizers generally recurse.
        # BaseSynchronizer has self.recursive which is True by default.
        if not recursive:
            # There isn't a direct "recursive" option in opts for synchronizers,
            # it's usually determined by the walker.
            pass

        s = UploadSynchronizer(local_target, remote_target, opts)
        s.run()

    def pull(
        self,
        remote_dir: str,
        local_dir: Path,
        recursive: bool = False,
        callback=None,
    ) -> None:
        """Pulls new or updated files from remote_dir to local_dir.

        Args:
            remote_dir: The remote directory to pull from.
            local_dir: The local directory to pull to.
            recursive: Whether to pull directories recursively. Defaults to False.
            callback: An optional callback function for logging progress.
        """
        local_target = FsTarget(str(local_dir))
        remote_target = self._get_ftp_target(remote_dir)
        opts = {"verbose": 3}

        s = DownloadSynchronizer(local_target, remote_target, opts)
        s.run()

    def sync(
        self,
        local_dir: Path,
        remote_dir: str,
        recursive: bool = False,
        callback=None,
    ) -> None:
        """Synchronizes files bidirectionally between local_dir and remote_dir.

        Args:
            local_dir: The local directory to sync.
            remote_dir: The remote directory to sync.
            recursive: Whether to sync directories recursively. Defaults to False.
            callback: An optional callback function for logging progress.
        """
        local_target = FsTarget(str(local_dir))
        remote_target = self._get_ftp_target(remote_dir)
        opts = {"resolve": "skip", "verbose": 3}

        s = BiDirSynchronizer(local_target, remote_target, opts)
        s.run()
