import logging

from langfuse_cli.client.langfuse_client import get_langfuse_client
from langfuse_cli.config import Config
from langfuse_cli.services.fetch_data_service import fetch_dataset
from langfuse_cli.services.store_service import store_dataset
from langfuse_cli.services.validation_service import validate_dataset
from langfuse_cli.utils.file_eraser import clean_datasets_dir

logger = logging.getLogger(__name__)


def get_dataset_names(langfuse_client) -> list[str]:
    datasets = langfuse_client.client.datasets.list().data
    return [ds.name for ds in datasets]


def handle_generate_command(config: Config) -> int:
    try:
        clean_datasets_dir(config.datasets_target_dir)
        langfuse_client = get_langfuse_client()

        dataset_names = get_dataset_names(langfuse_client)

        if not dataset_names:
            logger.info("No datasets found in Langfuse.")
            return 0

        for dataset_name in dataset_names:
            dataset = fetch_dataset(dataset_name)
            validate_dataset(dataset_name, dataset)
            store_dataset(config.datasets_target_dir, dataset, dataset_name)

    except Exception:
        logger.exception("Unexpected error during dataset generation")
        return 1

    return 0
