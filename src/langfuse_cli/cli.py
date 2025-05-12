import argparse
import sys

from langfuse_cli.api.down_handler import handle_generate_command
from langfuse_cli.api.up_handler import handle_up_command
from langfuse_cli.middleware.logger import setup_logging


def run() -> int:
    setup_logging(debug="--debug" in sys.argv)

    parser = argparse.ArgumentParser(
        description="Simple CLI tool with up/down commands."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-d", "--down", action="store_true", help="Run the 'down' command."
    )
    group.add_argument("-u", "--up", action="store_true", help="Run the 'up' command.")

    args = parser.parse_args()

    if args.down:
        return handle_generate_command()
    elif args.up:
        return handle_up_command()

    return 1
