import json
import logging
from pathlib import Path

import yaml

from langfuse_cli.models.datasets import DatasetItem, LangfuseDataset

logger = logging.getLogger(__name__)


def save_item_to_file(
    item: DatasetItem, filename: str, output_dir_template: str
) -> bool:
    try:
        path = Path(output_dir_template)
        path.mkdir(parents=True, exist_ok=True)

        file_path = path / filename
        with file_path.open("w", encoding="utf-8") as f:
            json.dump(item.model_dump(), f, indent=2, ensure_ascii=False)

        return True

    except OSError as e:
        logger.error(f"❌ Failed to create directory or write file '{filename}': {e}")
        return False
    except Exception:
        logger.exception(f"❌ Unexpected error while saving item '{filename}'")
        return False


def save_dataset_config_to_file(
    dataset: LangfuseDataset, filename: str, output_dir_template: str
) -> bool:
    try:
        path = Path(output_dir_template)
        path.mkdir(parents=True, exist_ok=True)

        file_path = path / filename
        with file_path.open("w", encoding="utf-8") as f:
            yaml.dump(dataset.model_dump(), f, indent=2, allow_unicode=True)

        return True

    except OSError as e:
        logger.error(f"❌ Failed to create directory or write file '{filename}': {e}")
        return False
