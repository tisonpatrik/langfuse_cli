import logging

from langfuse.api.resources.commons.errors.not_found_error import NotFoundError

from langfuse_cli.utils.file_writer import (
    save_to_json,
    save_to_yaml,
)

logger = logging.getLogger(__name__)


def export_item(
    item: dict,
    index: int,
    dataset_name: str,
    datasets_target_dir: str,
) -> None:
    filename = f"{dataset_name}_{index}.json"
    target_dir = f"{datasets_target_dir}/{dataset_name}"
    success = save_to_json(item, filename, target_dir)
    if not success:
        logger.warning(f"Item {index} from dataset '{dataset_name}' was not saved.")


def create_dataset_config(
    dataset_name: str, datasets_target_dir: str, dataset: dict
) -> None:
    filename = f"{dataset_name}.yaml"
    target_dir = f"{datasets_target_dir}/configs"
    schema = {
        "name": getattr(dataset, "name", dataset_name),
        "description": getattr(dataset, "description", ""),
        "metadata": getattr(dataset, "metadata", {}),
    }
    success = save_to_yaml(schema, filename, target_dir)
    if not success:
        logger.warning(f"Dataset '{dataset['name']}' was not saved.")


def store_dataset(datasets_target_dir: str, dataset: dict, dataset_name: str) -> None:
    try:
        create_dataset_config(dataset_name, datasets_target_dir, dataset)
        items = getattr(dataset, "items", [])
        for idx, item in enumerate(items):
            export_item(item, idx, dataset_name, datasets_target_dir)

        logger.info(f"Processed dataset: {dataset_name}")

    except NotFoundError:
        logger.error(f"Dataset '{dataset_name}' not found in Langfuse.")
    except ValueError as ve:
        logger.warning(f"Skipping dataset '{dataset_name}': {ve}")
    except Exception:
        logger.exception(
            f"Unexpected error during processing of dataset '{dataset_name}'"
        )
