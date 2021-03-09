from datetime import datetime

import pytest

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"

################################################################################
# Data fixtures
################################################################################


@pytest.fixture
def fake_log_list():
    return [
        {
            "created_at": datetime.strptime("2021-01-23T00:48:18", DATE_FORMAT),
            "first_name": "Малика",
            "message": "It is an army bred for a single purpose: To destroy the world of Men.     They will be here by nightfall. I have told your names to the Entmoot......and we have agreed......you are not      Orcs.,      It grows so cold.",
            "second_name": "Одинцова",
            "user_id": "315195",
        },
        {
            "created_at": datetime.strptime("2021-01-23T16:36:57", DATE_FORMAT),
            "first_name": "Элла",
            "message": "    Well, I'm back.  Leave now......and never come back. To make his war.The last war that will coverall the world in Shadow.",
            "second_name": "Кононова",
            "user_id": "102095",
        },
        {
            "created_at": datetime.strptime("2021-01-23T13:21:30", DATE_FORMAT),
            "first_name": "Неонила",
            "message": "Yes, precious. False.They will cheat you, hurt you, lie!   Oh no, I'm not hungry, leastways not for lembas bread.   Just where do you     think you're off to?",
            "second_name": "Боброва",
            "user_id": "670144",
        },
        {
            "created_at": datetime.strptime("2021-01-23T08:18:27", DATE_FORMAT),
            "first_name": "Анатолий",
            "message": "I have left instruction. , The people are to follow your rule in     my stead.     Take up my seat in the Golden Hall. Long may you defend Edoras, if the     battle goes ill.   Then it is forfeit. Release them.,      Shall I describe it to you? Or would you like me to find you a box?",
            "second_name": "Потапов",
            "user_id": "283098",
        },
    ]


@pytest.fixture
def fake_log_list_sorted():
    return [
        {
            "created_at": datetime.strptime("2021-01-23T00:48:18", DATE_FORMAT),
            "first_name": "Малика",
            "message": "It is an army bred for a single purpose: To destroy the world of Men.     They will be here by nightfall. I have told your names to the Entmoot......and we have agreed......you are not      Orcs.,      It grows so cold.",
            "second_name": "Одинцова",
            "user_id": "315195",
        },
        {
            "created_at": datetime.strptime("2021-01-23T08:18:27", DATE_FORMAT),
            "first_name": "Анатолий",
            "message": "I have left instruction. , The people are to follow your rule in     my stead.     Take up my seat in the Golden Hall. Long may you defend Edoras, if the     battle goes ill.   Then it is forfeit. Release them.,      Shall I describe it to you? Or would you like me to find you a box?",
            "second_name": "Потапов",
            "user_id": "283098",
        },
        {
            "created_at": datetime.strptime("2021-01-23T13:21:30", DATE_FORMAT),
            "first_name": "Неонила",
            "message": "Yes, precious. False.They will cheat you, hurt you, lie!   Oh no, I'm not hungry, leastways not for lembas bread.   Just where do you     think you're off to?",
            "second_name": "Боброва",
            "user_id": "670144",
        },
        {
            "created_at": datetime.strptime("2021-01-23T16:36:57", DATE_FORMAT),
            "first_name": "Элла",
            "message": "    Well, I'm back.  Leave now......and never come back. To make his war.The last war that will coverall the world in Shadow.",
            "second_name": "Кононова",
            "user_id": "102095",
        },
    ]


@pytest.fixture
def fake_api_response_dict():
    return {
        "error": "",
        "logs": [
            {
                "created_at": "2021-01-23T00:48:18",
                "first_name": "Малика",
                "message": "It is an army bred for a single purpose: To destroy the world of Men.     They will be here by nightfall. I have told your names to the Entmoot......and we have agreed......you are not      Orcs.,      It grows so cold.",
                "second_name": "Одинцова",
                "user_id": "315195",
            },
            {
                "created_at": "2021-01-23T16:36:57",
                "first_name": "Элла",
                "message": "    Well, I'm back.  Leave now......and never come back. To make his war.The last war that will coverall the world in Shadow.",
                "second_name": "Кононова",
                "user_id": "102095",
            },
            {
                "created_at": "2021-01-23T13:21:30",
                "first_name": "Неонила",
                "message": "Yes, precious. False.They will cheat you, hurt you, lie!   Oh no, I'm not hungry, leastways not for lembas bread.   Just where do you     think you're off to?",
                "second_name": "Боброва",
                "user_id": "670144",
            },
            {
                "created_at": "2021-01-23T08:18:27",
                "first_name": "Анатолий",
                "message": "I have left instruction. , The people are to follow your rule in     my stead.     Take up my seat in the Golden Hall. Long may you defend Edoras, if the     battle goes ill.   Then it is forfeit. Release them.,      Shall I describe it to you? Or would you like me to find you a box?",
                "second_name": "Потапов",
                "user_id": "283098",
            },
        ],
    }


@pytest.fixture
def fake_api_error_dict():
    return {
        "error": "created_day: does not match format 20200105 (year - 2021, month - 01, day - 05)"
    }


################################################################################
# Mock fixtures
################################################################################


@pytest.fixture
def mock_requests_get(mocker, fake_api_response_dict):
    mock = mocker.patch("requests.get")
    mock.return_value.json.return_value = fake_api_response_dict
    return mock


@pytest.fixture
def mock_requests_get_incorrect_date(mocker, fake_api_error_dict):
    mock = mocker.patch("requests.get")
    mock.return_value.json.return_value = fake_api_error_dict
    return mock


@pytest.fixture
def mock_requests_get_error(mocker):
    def error_function():
        raise ValueError("Test error message.")

    mock = mocker.patch("requests.get")
    mock.return_value.raise_for_status = error_function
    return mock
