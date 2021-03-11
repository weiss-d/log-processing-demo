import logging
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, db_uri: str) -> None:
        try:
            self.connection: sqlite3.Connection = sqlite3.connect(
                db_uri, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
            )
            self.connection.row_factory = sqlite3.Row
            self.cursor: sqlite3.Cursor = self.connection.cursor()
            logger.info("Successfuly connected to database at %s", db_uri)
        except Exception as error:
            logger.error("Database connection error: %s", str(error))
            raise

    def update(self, message_list: List[Dict[str, Union[datetime, str]]]) -> None:
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS log_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at timestamp NOT NULL,
                user_id TEXT NOT NULL,
                first_name TEXT,
                second_name TEXT,
                message TEXT
            );
            """
        )
        self.connection.commit()

        for element in message_list:
            self.cursor.execute(
                """
                INSERT INTO 'log_messages'
                    ('created_at', 'user_id', 'first_name', 'second_name', 'message')
                VALUES (?, ?, ?, ?, ?);
                """,
                (
                    element["created_at"],
                    element["user_id"],
                    element["first_name"],
                    element["second_name"],
                    element["message"],
                ),
            )
        self.connection.commit()

    def read(
        self, date: str, time_interval: Optional[Tuple[str]] = None
    ) -> List[Dict[str, Union[datetime, str]]]:
        if time_interval:
            time_boundaries: Tuple[datetime] = (
                datetime.fromisoformat(f"{date}T{time_interval[0]}"),
                datetime.fromisoformat(f"{date}T{time_interval[1]}"),
            )
        else:
            time_boundaries: Tuple[datetime] = (
                datetime.fromisoformat(f"{date}"),
                datetime.fromisoformat(f"{date}") + timedelta(days=1),
            )

        self.cursor.execute(
            """
            SELECT created_at, user_id, first_name, second_name, message
            FROM log_messages
            WHERE created_at > ? AND created_at < ?
            ORDER BY created_at;
            """,
            time_boundaries,
        )

        return [dict(item) for item in self.cursor.fetchall()]
