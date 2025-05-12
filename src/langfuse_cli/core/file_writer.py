import logging
from pathlib import Path

import orjson
import yaml

from langfuse_cli.models.datasets import DatasetItem, LangfuseDatasetConfig

logger = logging.getLogger(__name__)


def save_item_to_file(
    item: DatasetItem, filename: str, output_dir_template: str
) -> bool:
    try:
        path = Path(output_dir_template)
        path.mkdir(parents=True, exist_ok=True)

        file_path = path / filename
        json_bytes = orjson.dumps(
            item.model_dump(),
            option=orjson.OPT_INDENT_2
            | orjson.OPT_NON_STR_KEYS
            | orjson.OPT_SERIALIZE_DATACLASS,
        )  ##  TODO: no specific reasons, for those options.. validate me pls

        with file_path.open("wb") as f:
            f.write(json_bytes)

        return True

    except OSError as e:
        logger.error(f"❌ Failed to create directory or write file '{filename}': {e}")
        return False
    except Exception:
        logger.exception(f"❌ Unexpected error while saving item '{filename}'")
        return False


def save_dataset_config_to_file(
    dataset: LangfuseDatasetConfig, filename: str, output_dir_template: str
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
