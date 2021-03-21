"""
Database interaction module.
"""
import functools
import logging
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union

from log_processing_demo.log_item import LogItem
from log_processing_demo.log_updater import LogUpdater

logger = logging.getLogger(__name__)


def db_logging(log_statement: str):
    """Decorator for logging database operations.

    Parameters
    ----------
    log_statement : str
        Log statement that describes DB operation.
    """

    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            try:
                result_or_none = function(*args, **kwargs)
                logger.info(
                    "%s - success: %s.\nArguments:%s, %s",
                    function.__name__,
                    log_statement,
                    str(args)[:100],
                    str(kwargs)[:100],
                )
                return result_or_none
            except Exception as error:
                logger.error(
                    "%s - ERROR: %s.\n%s\nArguments:%s, %s",
                    function.__name__,
                    log_statement,
                    str(error),
                    str(args)[:100],
                    str(kwargs)[:100],
                )
                raise

        return wrapper

    return decorator


class Database(LogUpdater):
    """Class to update and read from a DB."""

    def __init__(self, db_uri: str) -> None:
        """Constructor.

        Parameters
        ----------
        db_uri : str
            *.db file path or ':memory:'.

        Returns
        -------
        None

        """
        self.db_uri = db_uri
        self._connect_to_db(self.db_uri)

    @db_logging("connect to database")
    def _connect_to_db(self, db_uri: str) -> None:
        """Initializes SQLite connection with options to handle timestamps.

        Parameters
        ----------
        db_uri : str
            *.db file path or ':memory:'.

        Returns
        -------
        None

        """
        self.connection: sqlite3.Connection = sqlite3.connect(
            db_uri, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        )
        self.connection.row_factory = sqlite3.Row
        self.cursor: sqlite3.Cursor = self.connection.cursor()

    @db_logging("update LOG data")
    def update(self, message_list: List[LogItem]) -> None:
        """Update database with logs fetched by LogReceiver.

        Parameters
        ----------
        message_list : List[LogItem]
            Output of call to LogReceiver object.

        Returns
        -------
        None

        """
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS log_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at timestamp NOT NULL,
                user_id TEXT NOT NULL,
                message TEXT,
                CONSTRAINT fk_users
                    FOREIGN KEY (user_id)
                    REFERENCES users(user_id)
                    ON DELETE CASCADE
            );
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                first_name TEXT,
                second_name TEXT
            );
            """
        )
        self.connection.commit()

        for element in message_list:
            self.cursor.execute(
                """
                INSERT OR IGNORE INTO users (user_id, first_name, second_name)
                VALUES (?, ?, ?)
                """,
                (element.user_id, element.first_name, element.second_name),
            )
            self.cursor.execute(
                """
                INSERT INTO 'log_messages'
                    ('created_at', 'user_id', 'message')
                VALUES (?, ?, ?);
                """,
                (
                    element.created_at,
                    element.user_id,
                    element.message,
                ),
            )
        self.connection.commit()

    @db_logging("retrieve LOG data")
    def read(
        self, log_date: str, time_interval: Optional[Tuple[str, str]] = None
    ) -> List[Dict[str, Union[datetime, str]]]:
        """Read log messages for desired date from database, optionally filtering by time.

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
        time_boundaries: Tuple[datetime, datetime]

        if time_interval:
            time_boundaries = (
                datetime.fromisoformat(f"{log_date}T{time_interval[0]}"),
                datetime.fromisoformat(f"{log_date}T{time_interval[1]}"),
            )
        else:
            time_boundaries = (
                datetime.fromisoformat(f"{log_date}"),
                datetime.fromisoformat(f"{log_date}") + timedelta(days=1),
            )

        self.cursor.execute(
            """
            SELECT lms.created_at, usr.user_id, usr.first_name, usr.second_name, lms.message
            FROM log_messages lms
                JOIN users usr
                    ON lms.user_id = usr.user_id
            WHERE lms.created_at > ? AND lms.created_at < ?
            ORDER BY lms.created_at;
            """,
            time_boundaries,
        )

        return [dict(item) for item in self.cursor.fetchall()]

    def flush(self, from_date: Optional[str] = None) -> None:
        """Remove LOG messages from database. Optionally for a particular date.

        Parameters
        ----------
        from_date : Optional[str]
            From this date and earlier all messages will be erased.

        Returns
        -------
        None

        """
        if from_date:
            self.cursor.execute(
                """
                DELETE FROM log_messages
                WHERE created_at > ?
                """,
                (datetime.fromisoformat(from_date),),
            )
        else:
            self.cursor.execute(
                """
                DELETE FROM log_messages;
                """
            )
        self.connection.commit()
