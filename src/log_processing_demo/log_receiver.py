from datetime import datetime
from os import path
from typing import Dict, List, Optional, Union

import requests

from log_processing_demo.sort import sort

LOG_LIST_NAME = "logs"
ERROR_NAME = "error"
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"
LOG_DATE_NAME = "created_at"


class LogReceiver:
    def __init__(self, base_url: str):
        self.base_url: str = base_url

    def __call__(
        self, date_string: str, sort_by_time: Optional[bool] = False
    ) -> List[Dict[str, Union[datetime, str]]]:
        with requests.get(path.join(self.base_url, date_string)) as response:
            data = response.json()

            if data[ERROR_NAME]:
                raise ValueError(data[ERROR_NAME])

            log_list = data[LOG_LIST_NAME]

            for element in log_list:
                element[LOG_DATE_NAME] = datetime.strptime(
                    element[LOG_DATE_NAME], DATE_FORMAT
                )

            if sort_by_time:

                def key(element):
                    return element[LOG_DATE_NAME]

                sort(log_list, key)

            return log_list
