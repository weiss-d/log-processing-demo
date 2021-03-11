"""
Entry point for command line use.
"""

import argparse
import logging
from pathlib import Path

from log_processing_demo import database, log_receiver

# Set up logging format
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    datefmt="%y-%m-%d %H:%M:%S",
)

# Commands and arguments handling

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(title="commands", dest="command")

# -- Command for fetching log messages from URL and putting them to the DB
parser_fetch = subparsers.add_parser("fetch")
parser_fetch.add_argument("base_url", type=str, help="Base LOG API URL.")
parser_fetch.add_argument("date_path", type=str, help="LOG date in format YYYYMMDD")
parser_fetch.add_argument(
    "db_file",
    nargs="?",
    type=Path,
    help="Database file. Default is 'database.db'.",
    default=Path("database.db"),
)

# -- Command to view log messages from the DB in JSON format
parser_show = subparsers.add_parser("show")
parser_show.add_argument(
    "date", type=str, help="Date of LOG messages. Format: YYYY-MM-DD"
)
parser_show.add_argument(
    "db_file",
    nargs="?",
    type=Path,
    help="Database file. Default is 'database.db'.",
    default=Path("database.db"),
)
parser_show.add_argument(
    "-i", "--interval", type=str, help="Time interval. Format: HH:MM:SS-HH:MM:SS"
)

args = parser.parse_args()

# Processing a command

if args.command == "fetch":
    get_logs = log_receiver.LogReceiver(args.base_url)
    db = database.Database(args.db_file)

    db.update(get_logs(args.date_path))
elif args.command == "show":
    db = database.Database(args.db_file)
    time_interval = tuple(args.interval.split("-")) if args.interval else None

    print(db.read(args.date, time_interval))
