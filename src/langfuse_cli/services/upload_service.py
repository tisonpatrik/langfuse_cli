import logging
from pathlib import Path

from langfuse_cli.client.langfuse_client import get_langfuse_client
from langfuse_cli.utils.file_reader import get_dataset_config, get_dataset_items

logger = logging.getLogger(__name__)


def upload_dataset(dataset_name: Path) -> None:
    client = get_langfuse_client()
    config = get_dataset_config(dataset_name)
    client.create_dataset(
        name=config.name, description=config.description, metadata=config.metadata
    )
    dataset_folder = dataset_name.stem
    data_dir = Path("datasets") / dataset_folder
    items = get_dataset_items(data_dir)
    for item in items:
        client.create_dataset_item(
            dataset_name=config.name,
            input=item.question,
            expected_output=item.expected_output,
            metadata=item.workspaces,
        )
        logger.info(f"Processed item: {item.question}")

    logger.info(f"Processed dataset: {dataset_name}")
