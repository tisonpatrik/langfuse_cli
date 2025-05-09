import argparse
import sys

from langfuse_cli.api.handler import handle_generate_command
from langfuse_cli.middleware.logger import setup_logging


def register_generate_command(subparsers):
    parser = subparsers.add_parser("generate", help="Generate datasets from Langfuse")
    parser.add_argument(
        "--workspaces", nargs="*", help="Specific workspace(s) to process"
    )
    parser.add_argument(
        "--use-cases", nargs="*", help="Specific use-case(s) to process"
    )
    parser.add_argument(
        "--critical", action="store_true", help="Process critical datasets"
    )

    parser.add_argument("--datasets", nargs="*", help="Specific dataset(s) to process")

    parser.set_defaults(handler=handle_generate_command)

    return parser


def run() -> int:
    setup_logging(debug="--debug" in sys.argv)
    parser = argparse.ArgumentParser(description="Dataset processing CLI tool.")
    subparsers = parser.add_subparsers(dest="command")
    generate_parser = register_generate_command(subparsers)
    args, unknown = parser.parse_known_args()

    if not args.command:
        # No subcommand given -> lets run 'generate' command manually
        generate_args = generate_parser.parse_args(unknown)

        return handle_generate_command(generate_args)

    if hasattr(args, "handler"):
        return args.handler(args)
    else:
        parser.print_help()
        return 1
