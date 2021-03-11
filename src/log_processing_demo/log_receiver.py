"""
Module for receiving LOGs via API.
"""
from datetime import datetime
from os import path
from typing import Dict, List, Optional, Union

import requests

from log_processing_demo.sort import sort

LOG_LIST_NAME = "logs"
ERROR_NAME = "error"
LOG_DATE_NAME = "created_at"


class RequestError(Exception):
    """Exception for wrapping all possible exceptions of 'requests' module."""

    pass


class LogReceiver:
    """Class for receiving LOGs via API.
    See methods docstrings.
    """

    def __init__(self, base_url: str):
        """Constructor remembers a base API URL.

        Parameters
        ----------
        base_url : str
            Base API URL.
        """
        self.base_url: str = base_url

    def __call__(
        self, date_string: str, sort_by_time: Optional[bool] = False
    ) -> List[Dict[str, Union[datetime, str]]]:
        """Call an instance of class to retreive a list of LOG messages for desired date.

        Parameters
        ----------
        date_string : str
            Date to get LOG messages for. Format: YYMMDD
        sort_by_time : Optional[bool]
            Whether or not the result should be sorted by record creation time.

        Returns
        -------
        List[Dict[str, Union[datetime, str]]]
            Either sorted or unsorted list of LOG records.

        Raises
        ------
        RequestError
            Re-rised for any 'requests' module exception.
        ValueError
            Rised when API returns an error message.

        """
        try:
            response = requests.get(path.join(self.base_url, date_string))
            response.raise_for_status()
        except Exception as error:
            raise RequestError(str(error))

        data = response.json()
        if data[ERROR_NAME]:
            raise ValueError(data[ERROR_NAME])

        log_list = data[LOG_LIST_NAME]
        for element in log_list:
            element[LOG_DATE_NAME] = datetime.fromisoformat(element[LOG_DATE_NAME])

        if sort_by_time:

            def key(element):
                return element[LOG_DATE_NAME]

            sort(log_list, key)

        return log_list
