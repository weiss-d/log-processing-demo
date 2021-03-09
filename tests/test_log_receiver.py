import pytest

from log_processing_demo import log_receiver


def test_initialize_log_receiver_class():
    receiver = log_receiver.LogReceiver("http://www.dsdev.tech/logs/")
    assert isinstance(receiver, log_receiver.LogReceiver)


def test_get_unsorted_log_list(mock_requests_get, fake_log_list):
    receiver = log_receiver.LogReceiver("http://www.dsdev.tech/logs/")
    assert receiver("20210123") == fake_log_list


def test_get_sorted_log_list(mock_requests_get, fake_log_list_sorted):
    receiver = log_receiver.LogReceiver("http://www.dsdev.tech/logs/")
    assert receiver("20210123", sort_by_time=True) == fake_log_list_sorted


def test_get_response_for_incorrect_date(mock_requests_get_incorrect_date):
    receiver = log_receiver.LogReceiver("http://www.dsdev.tech/logs/")
    with pytest.raises(ValueError) as error:
        receiver("2021")
    assert "created_day: does not match format" in str(error.value)


def test_requests_error_handling(mock_requests_get_error):
    receiver = log_receiver.LogReceiver("http://www.dsdev.tech/logs/")
    with pytest.raises(log_receiver.RequestError) as error:
        receiver("2021")
    assert "Test error message." in str(error.value)
