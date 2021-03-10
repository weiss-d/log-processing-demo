import pytest  # noqa 401

from log_processing_demo import database


def test_connect_to_db():
    db = database.Database("tests/test_database.db")
    assert isinstance(db, database.Database)


def test_update_and_read_data(tmp_path, fake_log_list_sorted):
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()

    db = database.Database((test_dir / "test_database.db").as_posix())

    db.update(fake_log_list_sorted)
    result = db.read("2021-01-23")

    assert result == fake_log_list_sorted
