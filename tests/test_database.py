import pytest  # noqa 401

from log_processing_demo import database


def test_connect_to_db():
    db = database.Database("tests/test_database.db")
    assert isinstance(db, database.Database)


def test_update_and_read_data_for_a_day(tmp_db_path, fake_log_list_sorted):
    db = database.Database(tmp_db_path)
    db.update(fake_log_list_sorted)

    assert db.read("2021-01-23") == fake_log_list_sorted


def test_update_data_and_read_for_an_interval(tmp_db_path, fake_log_list_sorted):
    db = database.Database(tmp_db_path)
    db.update(fake_log_list_sorted)

    assert db.read("2021-01-23", ("00:00:00", "14:00:00")) == fake_log_list_sorted[:-1]


def test_flush_current_date(tmp_db_path, fake_log_list_sorted):
    db = database.Database(tmp_db_path)

    db.update(fake_log_list_sorted)
    assert db.read("2021-01-23") == fake_log_list_sorted

    db.flush(from_date="2021-01-23")
    assert db.read("2021-01-23") == []


def test_flush_everything(tmp_db_path, fake_log_for_two_dates):
    db = database.Database(tmp_db_path)
    db.update(fake_log_for_two_dates)

    db.flush()
    assert db.read("2021-01-23") == [] and db.read("2021-01-24") == []
