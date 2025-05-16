from pathlib import Path

import orjson
from yaml import safe_load

from langfuse_cli.core.models.datasets import DatasetItem, LangfuseDatasetConfig


def get_dataset_config(dataset_name: Path) -> LangfuseDatasetConfig:
    try:
        with open(dataset_name, "r") as f:
            config_dict = safe_load(f)
            return LangfuseDatasetConfig(**config_dict)
    except Exception:
        raise ValueError(f"Failed to load dataset config from {dataset_name}")


def get_dataset_items(data_dir: Path) -> list[DatasetItem]:
    items = []
    for json_file in sorted(data_dir.glob("*.json")):
        with open(json_file, "r", encoding="utf-8") as f:
            data = orjson.loads(f.read())
            items.append(DatasetItem(**data))

    return items


def read_yaml(file_path: str) -> dict:
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            file_content = safe_load(f)
            return file_content
        except Exception:
            raise ValueError(f"Failed to load config from {file_path}")
