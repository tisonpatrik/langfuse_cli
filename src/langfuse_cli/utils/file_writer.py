import logging
from pathlib import Path

import orjson
import yaml

logger = logging.getLogger(__name__)


def save_to_json(item: dict, filename: str, output_dir: str) -> bool:
    path = Path(output_dir)
    file_path = path / filename
    try:
        path.mkdir(parents=True, exist_ok=True)

        json_bytes = orjson.dumps(
            item,
            option=orjson.OPT_INDENT_2,
            default=lambda obj: str(obj),
        )
        file_path.write_bytes(json_bytes)
        return True
    except Exception as e:
        logger.error(f"Failed to save {file_path}: {e}")
        return False


def save_to_yaml(schema: dict, filename: str, output_dir_template: str) -> bool:
    try:
        path = Path(output_dir_template)
        path.mkdir(parents=True, exist_ok=True)

        file_path = path / filename
        with file_path.open("w", encoding="utf-8") as f:
            yaml.dump(schema, f, indent=2, allow_unicode=True)

        return True

    except OSError as e:
        logger.error(f"Failed to create directory or write file '{filename}': {e}")
        return False
