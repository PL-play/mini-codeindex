import hashlib
import os

from mini_code_index.db import _collection_name_for_root


def test_collection_name_hashes_absolute_path() -> None:
    root_dir = "/tmp/vectorcode_test_project"
    full = os.path.abspath(os.path.expanduser(root_dir))
    expected = hashlib.sha256(full.encode("utf-8")).hexdigest()[:63]
    assert _collection_name_for_root(root_dir) == expected


def test_collection_name_is_stable() -> None:
    root_dir = "/tmp/vectorcode_test_project"
    assert _collection_name_for_root(root_dir) == _collection_name_for_root(root_dir)
