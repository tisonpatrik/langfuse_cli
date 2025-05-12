from pathlib import Path

from langfuse_cli.client.langfuse_client import get_langfuse_client
from langfuse_cli.core.file_reader import get_dataset_config, get_dataset_items


def upload_dataset(dataset_name: Path) -> None:
    client = get_langfuse_client()
    config = get_dataset_config(dataset_name)
    client.create_dataset(
        name=config.name, description=config.description, metadata=config.metadata
    )
    dataset_folder = dataset_name.stem
    data_dir = Path("datasets") / dataset_folder
    items = get_dataset_items(data_dir)
