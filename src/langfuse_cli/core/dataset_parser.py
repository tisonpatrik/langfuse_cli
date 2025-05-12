from typing import Any

from langfuse_cli.models.datasets import DatasetItem, DatasetMetadata, LangfuseDataset


def parse_raw_items(raw_items: list[Any]) -> list[DatasetItem]:
    parsed = []
    for item in raw_items:
        item_data = {
            "question": item.input,
            "expected_output": item.expected_output,
            "workspaces": item.metadata.get("workspaces")
            if isinstance(item.metadata, dict)
            else None,
        }
        parsed.append(DatasetItem(**item_data))
    return parsed


def fetch_dataset(langfuse_client, dataset_name: str) -> LangfuseDataset:
    raw = langfuse_client.get_dataset(dataset_name)

    if not isinstance(raw.metadata, dict):
        raise ValueError(f"Dataset {raw.name} has invalid metadata")

    metadata = DatasetMetadata(
        name=raw.metadata["name"],
        use_case=raw.metadata["use_case"],
        critical=raw.metadata.get("critical", False),
    )

    items = parse_raw_items(raw.items)

    return LangfuseDataset(
        name=raw.name,
        description=raw.description,
        metadata=metadata,
        items=items,
    )
