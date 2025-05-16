import logging
import os
from pathlib import Path

from langfuse_cli.services.upload_service import upload_dataset

logger = logging.getLogger(__name__)


def get_dataset_names() -> list[Path]:
    config_dir = "datasets/configs"
    config_files = os.listdir(config_dir)
    if not config_files:
        raise ValueError("No config files found in datasets/configs directory.")

    return [Path(config_dir) / file for file in config_files]


def handle_up_command() -> int:
    try:
        dataset_names = get_dataset_names()
        for dataset_name in dataset_names:
            upload_dataset(
                dataset_name,
            )

    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except Exception:
        logger.exception("Unexpected error during dataset generation")
        return 1

    return 0
