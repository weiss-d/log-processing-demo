"""
LogUpdater abstract class
"""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Union

from log_processing_demo.log_item import LogItem


class LogUpdater(ABC):
    """Abstract class for LOG storage operations."""

    @abstractmethod
    def update(self, message_list: List[LogItem]) -> None:
        """Update the storage with logs fetched by LogReceiver.

        Parameters
        ----------
        message_list : List[LogItem]
            Output of call to LogReceiver object.

        Returns
        -------
        None

        """
        pass

    @abstractmethod
    def read(
        self, log_date: str, time_interval: Optional[Tuple[str, str]] = None
    ) -> List[Dict[str, Union[datetime, str]]]:
        """Read log messages for desired date from storage, optionally filtering by time.

        Parameters
        ----------
        date : str
            LOG date. Format: YYYY-MM-DD
        time_interval : Optional[Tuple[str]]
            Tuple of desired time boundaries. Time format: HH:MM:SS

        Returns
        -------
        List[Dict[str, Union[datetime, str]]]
            Structure is identical to LogReceiver output.

        """
        pass

    @abstractmethod
    def flush(self, from_date: Optional[str] = None) -> None:
        """Remove LOG messages from storage. Optionally for a particular date.

        Parameters
        ----------
        from_date : Optional[str]
            From this date and earlier all messages will be erased.

        Returns
        -------
        None

        """
        pass
