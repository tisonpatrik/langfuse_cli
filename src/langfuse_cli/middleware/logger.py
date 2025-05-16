import logging

from rich.logging import RichHandler


def setup_logging(debug: bool = False) -> None:
    """Configure logging with Rich."""
    level = logging.DEBUG if debug else logging.INFO

    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            RichHandler(
                rich_tracebacks=True,
                tracebacks_show_locals=True,
                show_path=False,
                markup=False,
            )
        ],
    )
