import json
import logging
from pathlib import Path

from langfuse_cli.models.datasets import DatasetItem

logger = logging.getLogger(__name__)


def save_item_to_file(
    workspace: str, use_case: str, item: DatasetItem, filename: str, output_dir_template
) -> bool:
    try:
        output_dir = output_dir_template.format(
            fixture=workspace, workspace=workspace, use_case=use_case
        )
        path = Path(output_dir)
        path.mkdir(parents=True, exist_ok=True)

        file_path = path / filename
        with file_path.open("w", encoding="utf-8") as f:
            json.dump(item.model_dump(), f, indent=2, ensure_ascii=False)

        return True

    except OSError as e:
        logger.error(f"❌ Failed to create directory or write file '{filename}': {e}")
    except Exception:
        logger.exception(f"❌ Unexpected error while saving item '{filename}'")

    return False
