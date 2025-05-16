import argparse
import sys

from langfuse_cli.api.down_handler import handle_generate_command
from langfuse_cli.api.up_handler import handle_up_command
from langfuse_cli.config import Config
from langfuse_cli.utils.file_reader import read_yaml
from langfuse_cli.middleware.logger import setup_logging


def get_config() -> Config:
    try:
        config = read_yaml("config.yaml")
        return Config(**config)
    except Exception:
        raise ValueError("Failed to load config from config.yaml")


def run() -> int:
    setup_logging(debug="--debug" in sys.argv)

    config = get_config()

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
        return handle_generate_command(config)
    elif args.up:
        return handle_up_command()

    return 1
