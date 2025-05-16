import logging

from langfuse import Langfuse
from langfuse.api.resources.commons.errors.not_found_error import NotFoundError

from langfuse_cli.core.dataset_parser import fetch_dataset
from langfuse_cli.core.models.datasets import (
    DatasetItem,
    LangfuseDataset,
    LangfuseDatasetConfig,
)
from langfuse_cli.utils.file_writer import (
    save_dataset_config_to_file,
    save_item_to_file,
)

logger = logging.getLogger(__name__)


def export_item(
    item: DatasetItem,
    index: int,
    dataset_name: str,
) -> None:
    filename = f"{dataset_name}_{index}.json"
    target_dir = f"datasets/{dataset_name}"
    success = save_item_to_file(item, filename, target_dir)
    if not success:
        logger.warning(f"Item {index} from dataset '{dataset_name}' was not saved.")


def create_dataset_config(dataset: LangfuseDataset) -> None:
    filename = f"{dataset.name}.yaml"
    target_dir = "datasets/configs"
    config = LangfuseDatasetConfig(
        name=dataset.name, description=dataset.description, metadata=dataset.metadata
    )
    success = save_dataset_config_to_file(config, filename, target_dir)
    if not success:
        logger.warning(f"Dataset '{dataset.name}' was not saved.")


def store_dataset(
    datasets_target_dir: str, langfuse_client: Langfuse, dataset_name: str
) -> None:
    try:
        dataset = fetch_dataset(langfuse_client, dataset_name)
        create_dataset_config(dataset)
        for idx, item in enumerate(dataset.items):
            export_item(item, idx, dataset_name)

        logger.info(f"✅ Processed dataset: {dataset_name}")

    except NotFoundError:
        logger.error(f"❌ Dataset '{dataset_name}' not found in Langfuse.")
    except ValueError as ve:
        logger.warning(f"⚠️ Skipping dataset '{dataset_name}': {ve}")
    except Exception:
        logger.exception(
            f"❌ Unexpected error during processing of dataset '{dataset_name}'"
        )
