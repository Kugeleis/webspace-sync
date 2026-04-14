import pytest
from unittest.mock import patch, MagicMock
from webspace_sync.client import WebspaceClient


@pytest.fixture
def mock_ftp_target():
    with patch("webspace_sync.client.FTPTarget") as mock:
        yield mock


@pytest.fixture
def mock_fs_target():
    with patch("webspace_sync.client.FsTarget") as mock:
        yield mock


@pytest.fixture
def mock_upload_sync():
    with patch("webspace_sync.client.UploadSynchronizer") as mock:
        yield mock


@pytest.fixture
def mock_download_sync():
    with patch("webspace_sync.client.DownloadSynchronizer") as mock:
        yield mock


@pytest.fixture
def mock_bidir_sync():
    with patch("webspace_sync.client.BiDirSynchronizer") as mock:
        yield mock


def test_client_ls(mock_ftp_target):
    mock_target_instance = mock_ftp_target.return_value
    mock_entry = MagicMock()
    mock_entry.name = "file1.txt"
    mock_target_instance.read_dir.return_value = [mock_entry]

    client = WebspaceClient("host", "user", "pass")
    files = client.ls("some_dir")

    assert files == ["file1.txt"]
    mock_ftp_target.assert_called_with(
        "some_dir", "host", username="user", password="pass", tls=True
    )
    mock_target_instance.open.assert_called_once()
    mock_target_instance.read_dir.assert_called_once()
    mock_target_instance.close.assert_called_once()


def test_client_upload_file(
    mock_ftp_target, mock_fs_target, mock_upload_sync, tmp_path
):
    local_file = tmp_path / "test.txt"
    local_file.write_text("hello")

    client = WebspaceClient("host", "user", "pass")
    client.upload(local_file, "remote/dir")

    mock_fs_target.assert_called_once_with(str(tmp_path))
    mock_ftp_target.assert_called_once_with(
        "remote/dir", "host", username="user", password="pass", tls=True
    )
    mock_upload_sync.assert_called_once()
    mock_upload_sync.return_value.run.assert_called_once()


def test_client_push(mock_ftp_target, mock_fs_target, mock_upload_sync, tmp_path):
    local_dir = tmp_path / "local"
    local_dir.mkdir()

    client = WebspaceClient("host", "user", "pass")
    client.push(local_dir, "remote")

    mock_fs_target.assert_called_once_with(str(local_dir))
    mock_ftp_target.assert_called_once_with(
        "remote", "host", username="user", password="pass", tls=True
    )
    mock_upload_sync.assert_called_once()


def test_client_pull(mock_ftp_target, mock_fs_target, mock_download_sync, tmp_path):
    local_dir = tmp_path / "local"
    local_dir.mkdir()

    client = WebspaceClient("host", "user", "pass")
    client.pull("remote", local_dir)

    mock_fs_target.assert_called_once_with(str(local_dir))
    mock_ftp_target.assert_called_once_with(
        "remote", "host", username="user", password="pass", tls=True
    )
    mock_download_sync.assert_called_once()


def test_client_sync(mock_ftp_target, mock_fs_target, mock_bidir_sync, tmp_path):
    local_dir = tmp_path / "local"
    local_dir.mkdir()

    client = WebspaceClient("host", "user", "pass")
    client.sync(local_dir, "remote")

    mock_fs_target.assert_called_once_with(str(local_dir))
    mock_ftp_target.assert_called_once_with(
        "remote", "host", username="user", password="pass", tls=True
    )
    mock_bidir_sync.assert_called_once()
