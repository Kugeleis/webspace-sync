from webspace_sync.client import sanitize_remote_path


def test_sanitize_remote_path_absolute():
    assert sanitize_remote_path("/foo/bar") == "/foo/bar"
    assert sanitize_remote_path("/foo/bar/") == "/foo/bar"
    assert sanitize_remote_path("/") == "/"


def test_sanitize_remote_path_relative():
    assert sanitize_remote_path("foo/bar") == "/foo/bar"
    assert sanitize_remote_path("foo/bar/") == "/foo/bar"
    assert sanitize_remote_path("file.txt") == "/file.txt"


def test_sanitize_remote_path_empty():
    assert sanitize_remote_path("") == "/"
    assert sanitize_remote_path("   ") == "/"


def test_sanitize_remote_path_normalization():
    assert sanitize_remote_path("/foo//bar") == "/foo/bar"
    assert sanitize_remote_path("///foo") == "/foo"
    assert sanitize_remote_path("//foo") == "/foo"
    assert sanitize_remote_path("/foo/./bar") == "/foo/bar"
    assert sanitize_remote_path("/foo/../bar") == "/bar"
    assert sanitize_remote_path("../foo") == "/foo"
