import logging
from typing import Any

from langfuse_cli.client.langfuse_client import get_langfuse_client

logger = logging.getLogger(__name__)


class DatasetNotFoundError(Exception):
    """Raised when the requested dataset is not found in Langfuse."""


def fetch_dataset(dataset_name: str) -> Any:
    if not dataset_name:
        logger.error("Dataset name is required.")
        raise ValueError("Dataset name must not be empty.")

    try:
        client = get_langfuse_client()
        dataset = client.get_dataset(dataset_name)

        if not dataset:
            logger.error(f"Dataset '{dataset_name}' not found.")
            raise DatasetNotFoundError(f"Dataset '{dataset_name}' does not exist.")

        logger.debug(f"Dataset '{dataset_name}' successfully fetched.")
        return dataset

    except DatasetNotFoundError:
        raise
    except Exception as e:
        logger.exception(f"Error while fetching dataset '{dataset_name}': {e}")
        raise RuntimeError(f"Failed to fetch dataset '{dataset_name}'") from e
