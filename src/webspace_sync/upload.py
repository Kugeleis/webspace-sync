import argparse
import os
import sys
from pathlib import Path
from ftplib import FTP_TLS

from box import Box


def load_secrets(path: str = "config/secrets.yaml") -> Box:
    """
    Loads and returns the secrets from a YAML file.
    """
    if not os.path.exists(path):
        print(f"Error: Secrets file not found at {path}", file=sys.stderr)
        print(
            "Please create it using config/secrets-example.yaml as a template.",
            file=sys.stderr,
        )
        sys.exit(1)
    try:
        return Box.from_yaml(filename=path)
    except Exception as e:
        print(f"Failed to load secrets from {path}: {e}", file=sys.stderr)
        sys.exit(1)


def ensure_remote_dir(ftp: FTP_TLS, remote_dir: str) -> None:
    """
    Recursively creates directories on the remote server (mkdir -p).
    """
    parts = [p for p in remote_dir.split("/") if p]
    for part in parts:
        try:
            ftp.cwd(part)
        except Exception:
            ftp.mkd(part)
            ftp.cwd(part)


def upload_to_webspace(
    file_path: Path, secrets: Box, remote_dir: str = "data/raw"
) -> None:
    """
    Uploads a file to Webspace using native ftplib (FTP_TLS).
    """
    if not file_path.exists():
        print(f"Error: File to upload not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    ftp_conf = secrets.webspace.ftp
    host = ftp_conf.host
    user = ftp_conf.username
    password = ftp_conf.password

    print(f"Connecting to {host} via FTP_TLS...")
    try:
        with FTP_TLS() as ftp:
            ftp.connect(host)
            ftp.login(user, password)
            ftp.prot_p()  # Switch to secure data connection

            print(f"Ensuring remote directory: {remote_dir}")
            ensure_remote_dir(ftp, remote_dir)

            print(f"Uploading {file_path.name}...")
            with open(file_path, "rb") as f:
                ftp.storbinary(f"STOR {file_path.name}", f)

        print(f"Successfully uploaded {file_path.name} to {host}/{remote_dir}")
    except Exception as e:
        print(f"Upload failed: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Upload BoxMatrix output to a remote server"
    )
    parser.add_argument(
        "--file",
        "-f",
        default="output/boxen.json",
        help="Path to the file to upload (default: output/boxen.json)",
    )
    parser.add_argument(
        "--secrets",
        "-s",
        default="config/secrets.yaml",
        help="Path to the secrets YAML file (default: config/secrets.yaml)",
    )
    parser.add_argument(
        "--remote-dir",
        "-d",
        default="data/raw",
        help="Remote directory to upload to (default: data/raw)",
    )
    args = parser.parse_args()

    secrets = load_secrets(args.secrets)
    upload_to_webspace(Path(args.file), secrets, args.remote_dir)


if __name__ == "__main__":
    main()
